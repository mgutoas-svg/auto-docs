# 🚀 Guia de Deployment - Sistema Pronto para Produção

## ✅ Código no GitHub

**Repositório**: https://github.com/mgutoas-svg/auto-docs  
**Branch**: main  
**Status**: ✅ Pronto para deploy

---

## 📊 Arquitetura de Deploy

```
GitHub (auto-docs)
    ↓
Vercel (Frontend React)
    ↓
Render/Fly (Backend FastAPI)
    ↓
Supabase (PostgreSQL)
```

---

## 🔐 CREDENCIAIS DE ACESSO

### Usuário Padrão do Sistema
```
Email:  admin@mpelectric.com
Senha:  MP@Electric2024!
```

⚠️ **Importante**: Altere a senha após primeiro acesso em produção

---

## 📋 Passo 1: Criar Projeto Supabase

### 1.1 Ir para Supabase
1. Acesse: https://supabase.com
2. Clique em "New Project"
3. Ou se já tem conta: https://app.supabase.com

### 1.2 Configurar Projeto
- **Project Name**: `auto-docs`
- **Database Password**: Gere uma senha forte
- **Region**: Escolha a mais próxima (ex: us-east-1 ou sa-east-1)
- Clique em "Create new project"

### 1.3 Aguardar Criação
- Leva cerca de 2-3 minutos
- Você receberá email de confirmação

### 1.4 Obter Credenciais
Depois da criação, vá em **Settings → API**:

```
SUPABASE_URL = https://[seu-projeto].supabase.co
SUPABASE_KEY = [sua-chave-publica]
DATABASE_URL = postgresql://[user]:[password]@[host]:[5432]/postgres
```

### 1.5 Executar Schema
1. Vá em **SQL Editor**
2. Clique em **"New Query"**
3. Cole todo o conteúdo de `database/schema.sql`
4. Clique em **"Run"**
5. Pronto! Tabelas criadas ✅

---

## 🖥️ Passo 2: Deploy Backend (Render)

### 2.1 Ir para Render
1. Acesse: https://render.com
2. Clique em "Sign up" (ou "Sign in")
3. Conecte com GitHub

### 2.2 Criar Web Service
1. Clique em **"New +" → "Web Service"**
2. Selecione seu repositório `auto-docs`
3. Configure:
   - **Name**: `auto-docs-backend`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Root Directory**: `./backend`

### 2.3 Adicionar Variáveis de Ambiente
Clique em **"Environment"** e adicione:

```
DATABASE_URL=postgresql://[user]:[password]@[host]:5432/[database]
SECRET_KEY=gere-uma-chave-aleatoria-de-32-caracteres
CORS_ORIGINS=https://seu-frontend.vercel.app
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
DEBUG=false
```

### 2.4 Deploy
1. Clique em **"Create Web Service"**
2. Render faz deploy automaticamente
3. Aguarde 5-10 minutos
4. Copie a URL: `https://auto-docs-backend.onrender.com`

✅ **Backend pronto!**

---

## 🎨 Passo 3: Deploy Frontend (Vercel)

### 3.1 Ir para Vercel
1. Acesse: https://vercel.com
2. Clique em **"Sign Up"** (ou "Sign In")
3. Conecte com GitHub

### 3.2 Importar Projeto
1. Clique em **"Add New..." → "Project"**
2. Selecione `auto-docs`
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `./frontend`

### 3.3 Adicionar Variáveis de Ambiente
Clique em **"Environment Variables"** e adicione:

```
VITE_API_URL=https://auto-docs-backend.onrender.com
VITE_SUPABASE_URL=https://[seu-projeto].supabase.co
VITE_SUPABASE_ANON_KEY=[sua-chave-publica]
```

### 3.4 Deploy
1. Clique em **"Deploy"**
2. Vercel faz build e deploy
3. Aguarde 2-3 minutos
4. Copie a URL: `https://auto-docs.vercel.app`

✅ **Frontend pronto!**

---

## 🔗 LINKS DE ACESSO FINAL

### Sistema Pronto para Usar

**Frontend (Vercel)**
```
Link: https://auto-docs.vercel.app
Email: admin@mpelectric.com
Senha: MP@Electric2024!
```

**Backend API (Render)**
```
Link: https://auto-docs-backend.onrender.com
Docs: https://auto-docs-backend.onrender.com/docs
```

**Database (Supabase)**
```
Dashboard: https://app.supabase.com
Projeto: auto-docs
```

---

## ✅ Checklist Final

- [ ] Código em GitHub: ✅ https://github.com/mgutoas-svg/auto-docs
- [ ] Supabase criado e schema executado
- [ ] Backend deployado no Render
- [ ] Frontend deployado no Vercel
- [ ] Variáveis de ambiente configuradas
- [ ] CORS configurado
- [ ] Testado login com admin@mpelectric.com
- [ ] Logo MP Electric funcionando
- [ ] Exportação funcionando (PDF, Excel, etc)

---

## 🧪 Teste Rápido

1. Acesse: https://auto-docs.vercel.app
2. Login com:
   - Email: `admin@mpelectric.com`
   - Senha: `MP@Electric2024!`
3. Clique em "Contrato de Serviços"
4. Preencha alguns campos
5. Clique em "Exportar PDF"
6. Pronto! 📄✨

---

## 🆘 Troubleshooting

### API não responde
- Verificar variáveis no Render
- Aguardar cold start (primeira requisição pode levar 30s)

### Login não funciona
- Verificar DATABASE_URL no Render
- Resetar schema no Supabase

### Frontend lento
- Verificar VITE_API_URL no Vercel
- Limpar cache do navegador

---

## 📞 Suporte

Todos os links e credenciais estão acima.
Sistema pronto para produção!

🎉 **Seu sistema de automação de documentos está ao vivo!**
