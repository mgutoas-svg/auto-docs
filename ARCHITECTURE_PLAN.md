# 🏗️ Plano de Arquitetura - Sistema de Automação de Documentos

## 1. Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                  Frontend (React + TypeScript)                  │
│                      Running on Vercel                          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS / REST API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                           │
│                   Running on Render/Vercel                      │
│  - Template Management    - Document Generation                 │
│  - Logo Upload/Storage    - Export Engine (PDF, Excel, etc)     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Supabase (PostgreSQL)                          │
│         Persistent Storage + File Storage (Logos, Docs)         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Schema do Banco de Dados

### Tabelas Principais

```sql
-- Usuários (gerenciado por Supabase Auth)
users
├── id (UUID, PK)
├── email
├── name
└── created_at

-- Modelos de Documentos
document_templates
├── id (UUID, PK)
├── user_id (FK → users)
├── name (texto)
├── description (texto)
├── content (texto com placeholders {campo_nome})
├── fields (JSON) → lista de campos identificados
├── logo_id (FK → files) [opcional]
├── created_at
├── updated_at
└── is_active (booleano)

-- Campos Dinâmicos Mapeados
template_fields
├── id (UUID, PK)
├── template_id (FK → document_templates)
├── field_name (texto)
├── field_type (enum: text, date, number, email, etc)
├── is_required (booleano)
├── order (inteiro)
└── placeholder_pattern ({field_name})

-- Documentos Gerados
generated_documents
├── id (UUID, PK)
├── user_id (FK → users)
├── template_id (FK → document_templates)
├── title (texto)
├── content (JSONB com dados preenchidos)
├── data_filled (JSON dos valores)
├── created_at
├── updated_at
└── version (inteiro)

-- Arquivos (Logos, PDFs, etc)
files
├── id (UUID, PK)
├── user_id (FK → users)
├── filename (texto)
├── file_type (enum: logo, document, export)
├── mime_type (texto)
├── size (inteiro)
├── storage_path (S3/Supabase path)
├── uploaded_at
└── expires_at [opcional]

-- Exportações Geradas
exports
├── id (UUID, PK)
├── document_id (FK → generated_documents)
├── format (enum: pdf, xlsx, csv, docx, pptx)
├── file_id (FK → files)
├── created_at
└── download_count (inteiro)

-- Versões de Documentos
document_versions
├── id (UUID, PK)
├── document_id (FK → generated_documents)
├── version_number (inteiro)
├── content (JSONB)
├── created_at
├── created_by (user_id)
└── change_summary (texto)
```

---

## 3. API Endpoints

### Authentication
```
POST   /api/auth/register          - Registrar novo usuário
POST   /api/auth/login             - Login
POST   /api/auth/logout            - Logout
GET    /api/auth/me                - Perfil do usuário
```

### Document Templates
```
GET    /api/templates              - Listar templates do usuário
POST   /api/templates              - Criar novo template
GET    /api/templates/{id}         - Obter template específico
PUT    /api/templates/{id}         - Atualizar template
DELETE /api/templates/{id}         - Deletar template
POST   /api/templates/{id}/analyze - Analisar e extrair campos
```

### Document Generation
```
POST   /api/documents              - Gerar novo documento
GET    /api/documents              - Listar documentos do usuário
GET    /api/documents/{id}         - Obter documento específico
PUT    /api/documents/{id}         - Atualizar documento
DELETE /api/documents/{id}         - Deletar documento
POST   /api/documents/{id}/preview - Preview antes de exportar
```

### Exports
```
POST   /api/exports/{id}/pdf       - Exportar para PDF
POST   /api/exports/{id}/xlsx      - Exportar para Excel
POST   /api/exports/{id}/csv       - Exportar para CSV
POST   /api/exports/{id}/docx      - Exportar para Word
POST   /api/exports/{id}/pptx      - Exportar para PowerPoint
GET    /api/exports/{id}/download  - Download do arquivo
```

### Logos
```
POST   /api/logos/upload           - Upload de logo
GET    /api/logos                  - Listar logos
DELETE /api/logos/{id}             - Deletar logo
```

### Document Versions
```
GET    /api/documents/{id}/versions       - Listar versões
POST   /api/documents/{id}/versions       - Criar versão
GET    /api/documents/{id}/versions/{v}   - Obter versão específica
```

---

## 4. Estrutura de Pastas

```
doc-automation/
│
├── 📁 backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # Entry point FastAPI
│   │   ├── config.py                  # Configurações
│   │   ├── database.py                # Conexão Supabase
│   │   │
│   │   ├── models.py                  # SQLAlchemy models
│   │   ├── schemas.py                 # Pydantic schemas
│   │   ├── security.py                # Autenticação JWT
│   │   │
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── templates.py
│   │   │   ├── documents.py
│   │   │   ├── exports.py
│   │   │   ├── logos.py
│   │   │   └── versions.py
│   │   │
│   │   ├── services/
│   │   │   ├── template_service.py    # Lógica de templates
│   │   │   ├── document_service.py    # Lógica de documentos
│   │   │   ├── export_service.py      # Exportação multi-format
│   │   │   ├── field_extractor.py     # Extração de campos
│   │   │   └── logo_service.py        # Gestão de logos
│   │   │
│   │   ├── utils/
│   │   │   ├── pdf_generator.py       # Geração PDF
│   │   │   ├── excel_generator.py     # Geração Excel
│   │   │   ├── csv_generator.py       # Geração CSV
│   │   │   ├── docx_generator.py      # Geração Word
│   │   │   ├── pptx_generator.py      # Geração PowerPoint
│   │   │   └── field_parser.py        # Parse de {campos}
│   │   │
│   │   └── middleware/
│   │       └── error_handler.py
│   │
│   ├── tests/
│   │   ├── test_templates.py
│   │   ├── test_documents.py
│   │   ├── test_exports.py
│   │   └── test_field_extractor.py
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── 📁 frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── TemplateEditorPage.tsx  # Criar/editar templates
│   │   │   ├── DocumentGeneratorPage.tsx  # Gerar docs
│   │   │   ├── ExportPage.tsx          # Exportação
│   │   │   └── SettingsPage.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── Layout.tsx
│   │   │   ├── TemplateEditor.tsx      # Editor visual
│   │   │   ├── FormBuilder.tsx         # Gera form dos campos
│   │   │   ├── DocumentPreview.tsx
│   │   │   ├── ExportOptions.tsx
│   │   │   └── LogoUploader.tsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useTemplates.ts
│   │   │   ├── useDocuments.ts
│   │   │   └── useExport.ts
│   │   │
│   │   ├── store/
│   │   │   ├── authStore.ts
│   │   │   └── documentStore.ts
│   │   │
│   │   └── services/
│   │       └── api.ts
│   │
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── 📁 database/
│   └── schema.sql
│
├── 📁 docs/
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── API_DOCS.md
│
├── .gitignore
├── README.md
└── QUICK_START.md
```

---

## 5. Fluxo de Dados Principal

### Fluxo 1: Criar Template
```
User → Frontend (Paste text) 
  → Backend POST /api/templates
  → Field Extractor (identifica {campos})
  → Save in DB (template + fields)
  → Return template with fields
  → Frontend exibe campos encontrados
```

### Fluxo 2: Gerar Documento
```
User → Frontend (seleciona template)
  → FormBuilder gera form com campos
  → User preenche valores
  → Frontend POST /api/documents
  → Backend valida dados
  → Backend substitui {campos} pelos valores
  → Salva documento em DB
  → Return documento preenchido
```

### Fluxo 3: Exportar
```
User → Frontend (seleciona formato)
  → Frontend POST /api/exports/{id}/{format}
  → Backend carrega documento + template
  → ExportService chama gerador específico
  → Se houver logo, insere no documento
  → Salva arquivo em Supabase Storage
  → Return URL de download
  → Frontend redireciona para download
```

---

## 6. Stack de Dependências

### Backend
```python
fastapi==0.104.1
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
python-docx==0.8.11      # Word
openpyxl==3.10.10        # Excel
reportlab==4.0.9         # PDF
python-pptx==0.6.21      # PowerPoint
pillow==10.1.0           # Processamento de imagens (logos)
python-multipart==0.0.6  # Upload de arquivos
```

### Frontend
```typescript
react==18.2.0
typescript==5.3.3
react-router-dom==6.20.0
zustand==4.4.0          # State management
axios==1.6.0            # HTTP
tailwindcss==3.3.0      # Estilos
```

---

## 7. Casos de Teste Críticos

```
✓ Criar template com múltiplos campos
✓ Extrair campos corretamente de {campo_nome}
✓ Validar campos obrigatórios
✓ Gerar documento com dados preenchidos
✓ Substituição correta de placeholders
✓ Exportar para PDF com logo
✓ Exportar para Excel com formatação
✓ Download de arquivo gerado
✓ Versioning de documentos
✓ Erro handling (campos inválidos, upload falho, etc)
```

---

## 8. Considerações de Segurança

- **Autenticação:** JWT com Supabase Auth
- **Autorização:** Usuário só pode acessar seus templates/docs
- **Upload de arquivos:** Validar tipo, tamanho (max 5MB para logos)
- **Sanitização:** Limpar entrada de usuário para evitar injection
- **Rate limiting:** API com rate limit para evitar abuso
- **Dados sensíveis:** Não logar dados de documentos

---

## 9. Deploy Checklist

- [ ] Variáveis de ambiente configuradas
- [ ] Schema SQL executado no Supabase
- [ ] Backend deployado (Render/Vercel)
- [ ] Frontend deployado (Vercel)
- [ ] CORS configurado
- [ ] Bucket S3/Supabase Storage para files
- [ ] Testes passando
- [ ] Documentação completa

---

## 10. MVP Funcional (Fase 1)

**Escopo mínimo viável:**
1. Criar template com texto + campos manuais
2. Gerar documento (preencher campos)
3. Exportar para PDF
4. Listar templates e documentos

**Não incluído inicialmente:**
- Versioning completo
- OCR automático
- Múltiplos logos
- Assinatura digital

---

**Próximo:** Implementar Backend → Frontend → Testes → Deploy

*Última atualização: 2026-09-29*
