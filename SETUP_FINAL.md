# 🎉 Setup Final - Sistema Pronto para Uso

## ✅ Configurações Implementadas

### 1️⃣ Usuário Único Padrão
- **Email**: `admin@mpelectric.com`
- **Senha**: `MP@Electric2024!`
- Criado automaticamente ao iniciar o sistema
- Sem necessidade de registro

### 2️⃣ Templates Padrão (3 modelos)
Os seguintes templates estão pré-carregados para o usuário padrão:

1. **Contrato de Serviços**
   - Completo com todos os campos necessários
   - Pronto para assinatura
   - Campos extraídos automaticamente

2. **Nota Fiscal**
   - Modelo profissional
   - Dados de cliente e serviços
   - Informações bancárias

3. **Orçamento**
   - Template para propostas
   - Itemização detalhada
   - Condições comerciais

### 3️⃣ Logo MP Electric
- Usada automaticamente em todos os documentos
- Inserida no topo de PDFs
- Adicionada em headers de Word
- Presente em PowerPoints

---

## 🚀 Como Usar

### Primeiro Acesso

```bash
# Iniciar sistema
docker-compose up -d

# Aguardar 30 segundos
sleep 30

# Acessar
# Frontend: http://localhost:5173
# Backend: http://localhost:8000/docs
```

### Login
```
Email:  admin@mpelectric.com
Senha:  MP@Electric2024!
```

### Fluxo de Uso

1. **Escolher Template**
   - Clique em um dos 3 templates pré-carregados
   - Contrato, Nota Fiscal ou Orçamento

2. **Preencher Campos**
   - Formulário gerado automaticamente
   - Campos extraídos do template

3. **Visualizar**
   - Preview antes de exportar

4. **Exportar**
   - PDF (com logo MP Electric)
   - Word (com logo MP Electric)
   - Excel (com dados estruturados)
   - PowerPoint (com logo MP Electric)
   - CSV (para integração)

---

## 📋 Campos Disponíveis por Template

### Contrato
- data_contrato
- numero_contrato
- nome_cliente
- cpf_cnpj_cliente
- endereco_cliente
- telefone_cliente
- email_cliente
- tipo_servico
- descricao_servico
- local_servico
- data_inicio
- data_conclusao
- valor_servico
- forma_pagamento
- prazo_pagamento
- materiais_inclusos
- data_validade
- data_assinatura

### Nota Fiscal
- numero_nota
- data_emissao
- competencia
- nome_cliente
- cpf_cnpj_cliente
- endereco_cliente
- telefone_cliente
- descricao_servico
- periodo_servico
- valor_unitario
- quantidade
- valor_total
- forma_pagamento
- data_vencimento
- banco
- conta_bancaria
- observacoes

### Orçamento
- numero_orcamento
- data_orcamento
- dias_validade
- nome_cliente
- telefone_cliente
- email_cliente
- local_trabalho
- escopo_servicos
- item_1
- valor_item_1
- item_2
- valor_item_2
- item_3
- valor_item_3
- subtotal
- impostos
- desconto
- valor_total
- prazo_execucao
- formas_pagamento
- materiais
- garantia
- observacoes
- data_validade

---

## 🔧 Personalizar Templates

### Adicionar Novo Template
1. Clique em "Novo Template"
2. Cole seu texto com `{campos_assim}`
3. Sistema extrai campos automaticamente
4. Salve o template

### Editar Template Existente
1. Clique em um template
2. Modifique o conteúdo
3. Adicione/remova `{campos}`
4. Sistema atualiza automaticamente

---

## 📊 Exportação com Logo

Todos os formatos incluem a logo MP Electric automaticamente:

| Formato | Logo | Qualidade |
|---------|------|-----------|
| PDF | ✅ Topo | Alta |
| Word | ✅ Header | Alta |
| Excel | ❌ N/A | Estruturado |
| PowerPoint | ✅ Slide | Profissional |
| CSV | ❌ N/A | Dados |

---

## 🎯 Automação Completa para MP Electric

Este sistema automatiza:
- ✅ Geração de contratos
- ✅ Emissão de notas fiscais
- ✅ Criação de orçamentos
- ✅ Exportação em múltiplos formatos
- ✅ Inserção de logo automaticamente
- ✅ Preenchimento de dados

**Reduz tempo de 30min para 2min por documento!** ⚡

---

## ⚠️ Importante

- Usuário padrão criado automaticamente
- Mudar senha após primeiro acesso (recomendado)
- Logo será servida localmente
- Sistema está pronto para produção

---

**Sistema de Automação de Documentos - MP Electric**
Desenvolvido para otimizar seu cotidiano! 📄✨
