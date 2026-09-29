from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app import models, schemas
from app.security import (
    get_current_user, authenticate_user, create_access_token,
    hash_password, verify_password
)
from app.services.field_extractor import FieldExtractor
from app.services.export_service import ExportService
from fastapi.responses import StreamingResponse, FileResponse
import io
import os

router = APIRouter(prefix="/api", tags=["api"])


# ============= AUTH =============
@router.post("/auth/register", response_model=schemas.TokenResponse)
async def register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    """Registrar novo usuário"""
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    new_user = models.User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        name=user_data.name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.id})

    return {
        "access_token": access_token,
        "user": schemas.UserResponse.from_orm(new_user)
    }


@router.post("/auth/login", response_model=schemas.TokenResponse)
async def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login do usuário"""
    user = db.query(models.User).filter(models.User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    access_token = create_access_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "user": schemas.UserResponse.from_orm(user)
    }


@router.get("/auth/me", response_model=schemas.UserResponse)
async def get_me(current_user: models.User = Depends(get_current_user)):
    """Obter informações do usuário autenticado"""
    return schemas.UserResponse.from_orm(current_user)


# ============= TEMPLATES =============
@router.get("/templates", response_model=list[schemas.TemplateResponse])
async def list_templates(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar templates do usuário"""
    templates = db.query(models.DocumentTemplate).filter(
        models.DocumentTemplate.user_id == current_user.id,
        models.DocumentTemplate.is_active == True
    ).all()
    return [schemas.TemplateResponse.from_orm(t) for t in templates]


@router.post("/templates", response_model=schemas.TemplateResponse)
async def create_template(
    template_data: schemas.TemplateCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Criar novo template de documento"""
    # Extrair campos do conteúdo
    fields = FieldExtractor.extract_fields(template_data.content)

    new_template = models.DocumentTemplate(
        user_id=current_user.id,
        name=template_data.name,
        description=template_data.description,
        content=template_data.content,
        fields=fields,
        logo_id=template_data.logo_id
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)

    return schemas.TemplateResponse.from_orm(new_template)


@router.get("/templates/{template_id}", response_model=schemas.TemplateResponse)
async def get_template(
    template_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter template específico"""
    template = db.query(models.DocumentTemplate).filter(
        models.DocumentTemplate.id == template_id,
        models.DocumentTemplate.user_id == current_user.id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")

    return schemas.TemplateResponse.from_orm(template)


@router.put("/templates/{template_id}", response_model=schemas.TemplateResponse)
async def update_template(
    template_id: str,
    template_data: schemas.TemplateUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualizar template"""
    template = db.query(models.DocumentTemplate).filter(
        models.DocumentTemplate.id == template_id,
        models.DocumentTemplate.user_id == current_user.id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")

    update_data = template_data.dict(exclude_unset=True)

    # Re-extrair campos se conteúdo foi atualizado
    if "content" in update_data:
        update_data["fields"] = FieldExtractor.extract_fields(update_data["content"])

    for field, value in update_data.items():
        setattr(template, field, value)

    db.commit()
    db.refresh(template)

    return schemas.TemplateResponse.from_orm(template)


@router.delete("/templates/{template_id}")
async def delete_template(
    template_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletar template"""
    template = db.query(models.DocumentTemplate).filter(
        models.DocumentTemplate.id == template_id,
        models.DocumentTemplate.user_id == current_user.id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")

    template.is_active = False
    db.commit()

    return {"message": "Template deletado com sucesso"}


# ============= DOCUMENTS =============
@router.get("/documents", response_model=list[schemas.DocumentResponse])
async def list_documents(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar documentos do usuário"""
    documents = db.query(models.GeneratedDocument).filter(
        models.GeneratedDocument.user_id == current_user.id
    ).order_by(models.GeneratedDocument.created_at.desc()).all()
    return [schemas.DocumentResponse.from_orm(d) for d in documents]


@router.post("/documents", response_model=schemas.DocumentResponse)
async def create_document(
    doc_data: schemas.DocumentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Gerar novo documento"""
    # Obter template
    template = db.query(models.DocumentTemplate).filter(
        models.DocumentTemplate.id == doc_data.template_id,
        models.DocumentTemplate.user_id == current_user.id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")

    # Validar campos
    is_valid, error_msg = FieldExtractor.validate_fields(template.content, doc_data.data_filled)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # Substituir campos no conteúdo
    filled_content = FieldExtractor.replace_fields(template.content, doc_data.data_filled)

    new_document = models.GeneratedDocument(
        user_id=current_user.id,
        template_id=template.id,
        title=doc_data.title,
        content=filled_content,
        data_filled=doc_data.data_filled
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return schemas.DocumentResponse.from_orm(new_document)


@router.get("/documents/{document_id}", response_model=schemas.DocumentResponse)
async def get_document(
    document_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter documento específico"""
    document = db.query(models.GeneratedDocument).filter(
        models.GeneratedDocument.id == document_id,
        models.GeneratedDocument.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    return schemas.DocumentResponse.from_orm(document)


@router.put("/documents/{document_id}", response_model=schemas.DocumentResponse)
async def update_document(
    document_id: str,
    doc_data: schemas.DocumentUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualizar documento"""
    document = db.query(models.GeneratedDocument).filter(
        models.GeneratedDocument.id == document_id,
        models.GeneratedDocument.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    update_data = doc_data.dict(exclude_unset=True)

    # Se data_filled foi atualizada, regenerar content
    if "data_filled" in update_data:
        template = document.template
        filled_content = FieldExtractor.replace_fields(template.content, update_data["data_filled"])
        update_data["content"] = filled_content
        document.version += 1

    for field, value in update_data.items():
        setattr(document, field, value)

    db.commit()
    db.refresh(document)

    return schemas.DocumentResponse.from_orm(document)


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletar documento"""
    document = db.query(models.GeneratedDocument).filter(
        models.GeneratedDocument.id == document_id,
        models.GeneratedDocument.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    db.delete(document)
    db.commit()

    return {"message": "Documento deletado com sucesso"}


@router.get("/documents/{document_id}/preview", response_model=schemas.DocumentPreviewResponse)
async def preview_document(
    document_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Preview do documento antes de exportar"""
    document = db.query(models.GeneratedDocument).filter(
        models.GeneratedDocument.id == document_id,
        models.GeneratedDocument.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    return schemas.DocumentPreviewResponse.from_orm(document)


# ============= EXPORTS =============
@router.post("/exports/{document_id}/{export_format}")
async def export_document(
    document_id: str,
    export_format: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Exportar documento em formato específico"""
    document = db.query(models.GeneratedDocument).filter(
        models.GeneratedDocument.id == document_id,
        models.GeneratedDocument.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    # Obter caminho da logo se existir
    logo_path = None
    if document.template.logo_id:
        logo_file = db.query(models.File).filter(
            models.File.id == document.template.logo_id
        ).first()
        if logo_file:
            logo_path = logo_file.storage_path

    try:
        buffer, mime_type = ExportService.export(
            format=export_format,
            title=document.title,
            content=document.content,
            logo_path=logo_path,
            data_filled=document.data_filled
        )

        # Salvar referência de export no banco
        new_export = models.Export(
            document_id=document.id,
            format=export_format,
            file_id="temp"  # Idealmente salvaria em storage
        )
        db.add(new_export)
        db.commit()

        # Retornar arquivo
        filename = f"{document.title}.{export_format}"
        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type=mime_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============= LOGOS =============
@router.post("/logos/upload")
async def upload_logo(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload de logo da empresa"""
    # Validar tipo de arquivo
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Apenas imagens são aceitas")

    # Ler arquivo
    contents = await file.read()

    # Salvar arquivo
    storage_path = f"logos/{current_user.id}/{file.filename}"

    new_file = models.File(
        user_id=current_user.id,
        filename=file.filename,
        file_type="logo",
        mime_type=file.content_type,
        size=len(contents),
        storage_path=storage_path
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return schemas.FileResponse.from_orm(new_file)


@router.get("/logos")
async def list_logos(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar logos do usuário"""
    files = db.query(models.File).filter(
        models.File.user_id == current_user.id,
        models.File.file_type == "logo"
    ).all()
    return [schemas.FileResponse.from_orm(f) for f in files]


@router.delete("/logos/{file_id}")
async def delete_logo(
    file_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletar logo"""
    file = db.query(models.File).filter(
        models.File.id == file_id,
        models.File.user_id == current_user.id,
        models.File.file_type == "logo"
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="Logo não encontrada")

    db.delete(file)
    db.commit()

    return {"message": "Logo deletada com sucesso"}


@router.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}
