from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


# Auth
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Templates
class TemplateFieldSchema(BaseModel):
    name: str
    field_type: str = "text"  # text, date, number, email, etc
    required: bool = True


class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    content: str
    logo_id: Optional[str] = None


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    logo_id: Optional[str] = None


class TemplateResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    content: str
    fields: Optional[List[TemplateFieldSchema]]
    logo_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Documents
class DocumentCreate(BaseModel):
    template_id: str
    title: str
    data_filled: Dict[str, Any]


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    data_filled: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    id: str
    template_id: str
    title: str
    content: str
    data_filled: Dict[str, Any]
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentPreviewResponse(BaseModel):
    id: str
    title: str
    content: str
    data_filled: Dict[str, Any]


# Exports
class ExportRequest(BaseModel):
    format: str = Field(..., pattern="^(pdf|xlsx|csv|docx|pptx)$")


class ExportResponse(BaseModel):
    id: str
    document_id: str
    format: str
    download_url: str
    created_at: datetime


# Files/Logos
class FileResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    mime_type: str
    size: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


# Versions
class DocumentVersionResponse(BaseModel):
    id: str
    version_number: int
    content: str
    data_filled: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
