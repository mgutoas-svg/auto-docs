"""Seed data - usuário padrão e templates iniciais"""

from sqlalchemy.orm import Session
from app.models import User, DocumentTemplate
from app.security import hash_password
from app.services.field_extractor import FieldExtractor
from app.seeds.templates import DEFAULT_CONTRACT_TEMPLATE, DEFAULT_INVOICE_TEMPLATE, DEFAULT_BUDGET_TEMPLATE


def seed_default_user(db: Session):
    """Criar usuário padrão se não existir"""
    existing_user = db.query(User).filter(User.email == "admin@mpelectric.com").first()

    if existing_user:
        print("✓ Usuário padrão já existe")
        return existing_user

    default_user = User(
        email="admin@mpelectric.com",
        hashed_password=hash_password("MP@Electric2024!"),
        name="MP Electric - Admin"
    )

    db.add(default_user)
    db.commit()
    db.refresh(default_user)

    print(f"✓ Usuário padrão criado: {default_user.email}")
    return default_user


def seed_default_templates(db: Session, user_id: str):
    """Criar templates padrão para o usuário"""

    templates_data = [
        {
            "name": "Contrato de Serviços",
            "description": "Modelo padrão de contrato para prestação de serviços elétricos",
            "content": DEFAULT_CONTRACT_TEMPLATE
        },
        {
            "name": "Nota Fiscal",
            "description": "Modelo de nota fiscal para serviços prestados",
            "content": DEFAULT_INVOICE_TEMPLATE
        },
        {
            "name": "Orçamento",
            "description": "Modelo de orçamento para propostas de serviços",
            "content": DEFAULT_BUDGET_TEMPLATE
        }
    ]

    for template_data in templates_data:
        existing = db.query(DocumentTemplate).filter(
            DocumentTemplate.user_id == user_id,
            DocumentTemplate.name == template_data["name"]
        ).first()

        if existing:
            print(f"✓ Template '{template_data['name']}' já existe")
            continue

        fields = FieldExtractor.extract_fields(template_data["content"])

        new_template = DocumentTemplate(
            user_id=user_id,
            name=template_data["name"],
            description=template_data["description"],
            content=template_data["content"],
            fields=fields,
            is_active=True
        )

        db.add(new_template)
        db.commit()

        print(f"✓ Template '{template_data['name']}' criado com {len(fields)} campos")


def seed_all(db: Session):
    """Executar todos os seeds"""
    user = seed_default_user(db)
    seed_default_templates(db, user.id)
