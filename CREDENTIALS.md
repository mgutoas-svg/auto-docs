# 🔐 Credenciais Padrão - MP Electric

## Usuário Único Pré-configurado

**Email:** `admin@mpelectric.com`  
**Senha:** `MP@Electric2024!`

---

⚠️ **IMPORTANTE**: 
- Este é um usuário de desenvolvimento/demo
- Em produção, altere a senha imediatamente
- Use variáveis de ambiente para credenciais sensíveis

---

## 🎯 Uso

### Login via API
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@mpelectric.com",
    "password": "MP@Electric2024!"
  }'
```

### Frontend
1. Acesse http://localhost:5173
2. Email: `admin@mpelectric.com`
3. Senha: `MP@Electric2024!`
4. Clique em "Entrar"

---

## 📄 Logo Padrão (MP Electric)

A logo MP Electric é usada automaticamente em todos os documentos gerados:
- Inserida no topo de PDFs
- Adicionada em headers de Word
- Incluída em PowerPoints

---

## 🔑 Alterar Senha

Para alterar a senha do usuário padrão:

```bash
# Via API
curl -X POST http://localhost:8000/api/auth/change-password \
  -H "Authorization: Bearer {seu_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "MP@Electric2024!",
    "new_password": "SuaNovaSenha123!"
  }'
```

---

**Pronto para usar! 🚀**
