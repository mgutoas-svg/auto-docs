# ⚡ Quick Start - 5 minutos

## Opção 1: Docker (Recomendado)

```bash
docker-compose up -d
# Aguarde 30 segundos
# Frontend: http://localhost:5173
# Backend: http://localhost:8000/docs
```

## Opção 2: Manual

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Database
```bash
# Criar banco PostgreSQL
psql -U postgres
CREATE DATABASE doc_automation;
\i database/schema.sql
```

---

## 📋 Próximos Passos

1. **Criar Template**: Cole um texto com `{campos_assim}`
2. **Gerar Documento**: Preencha os campos
3. **Exportar**: Escolha formato (PDF, Excel, Word, PowerPoint, CSV)
4. **Pronto!** 🎉

---

## 🧪 Testes

```bash
cd backend
pytest tests/
```

---

## 📚 Docs Completos

- `README.md` - Overview geral
- `ARCHITECTURE_PLAN.md` - Arquitetura
- `docs/DEPLOYMENT.md` - Deploy

---

**Desenvolvido para **automação de documentos do seu cotidiano! 📄✨**
