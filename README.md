# 📄 Sistema de Automação de Documentos

Sistema completo de geração de documentos personalizados com suporte para múltiplos formatos de exportação.

## ✨ Funcionalidades

- ✅ Criar templates de documentos com campos dinâmicos
- ✅ Gerar documentos preenchendo campos automáticamente
- ✅ Exportar em múltiplos formatos: **PDF, Excel, Word, CSV, PowerPoint**
- ✅ Inserir logo da empresa automaticamente
- ✅ Versioning de documentos
- ✅ Persistência em Supabase
- ✅ Autenticação JWT
- ✅ Testes automatizados
- ✅ Pronto para produção

## 🏗️ Stack Tecnológico

- **Backend**: Python FastAPI
- **Frontend**: React 18 + TypeScript
- **Database**: PostgreSQL (Supabase)
- **Deploy**: Vercel (frontend) + Render (backend)

## 📂 Estrutura

```
doc-automation/
├── backend/
│   ├── app/
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic validation
│   │   ├── main.py          # FastAPI app
│   │   ├── security.py      # JWT auth
│   │   ├── routes/
│   │   │   └── api.py       # All endpoints
│   │   └── services/
│   │       ├── field_extractor.py
│   │       └── export_service.py
│   ├── tests/
│   │   └── test_field_extractor.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
│
├── database/
│   └── schema.sql
│
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Com Docker (Recomendado)

```bash
# Clone
git clone seu-repo
cd doc-automation

# Inicie
docker-compose up -d

# Acesse
# Frontend: http://localhost:5173
# Backend: http://localhost:8000/docs
```

### Manual (Linux/Mac)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Edite .env com DATABASE_URL
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## 📊 API Endpoints

### Auth
```
POST   /api/auth/register      - Registrar
POST   /api/auth/login         - Login
GET    /api/auth/me            - Perfil
```

### Templates
```
GET    /api/templates          - Listar
POST   /api/templates          - Criar
GET    /api/templates/{id}     - Obter
PUT    /api/templates/{id}     - Atualizar
DELETE /api/templates/{id}     - Deletar
```

### Documents
```
GET    /api/documents          - Listar
POST   /api/documents          - Gerar
GET    /api/documents/{id}     - Obter
PUT    /api/documents/{id}     - Atualizar
DELETE /api/documents/{id}     - Deletar
```

### Exports
```
POST   /api/exports/{id}/{format}  - Exportar (pdf, docx, xlsx, csv, pptx)
```

### Logos
```
POST   /api/logos/upload       - Upload
GET    /api/logos              - Listar
DELETE /api/logos/{id}         - Deletar
```

## 🧪 Testes

```bash
cd backend
pytest tests/
```

## 📝 Sintaxe de Templates

Use `{nome_campo}` para definir campos dinâmicos:

```
Documento de Contrato

Contratante: {nome_contratante}
Data: {data_inicio}
Valor: {valor}

O presente contrato...
```

O sistema extrai automaticamente os campos e cria um formulário para preenchimento.

## 🔒 Segurança

- JWT authentication
- Validação rigorosa de entrada
- CORS configurável
- Dados sensíveis não são logados

## 🌐 Deployment

### Frontend (Vercel)
```bash
vercel --prod
```

### Backend (Render)
1. Conecte seu repositório
2. Configure variáveis de ambiente
3. Deploy automático

## 📚 Documentação Completa

- `docs/ARCHITECTURE.md` - Arquitetura detalhada
- `docs/API_DOCS.md` - Documentação de API
- `docs/DEPLOYMENT.md` - Guia de deployment

## 📄 Licença

MIT

## 🤝 Contribuindo

Abra uma issue ou PR com melhorias!

---

**Pronto para usar! 🚀**
