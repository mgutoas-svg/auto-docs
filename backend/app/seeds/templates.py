"""Templates padrão para MP Electric"""

DEFAULT_CONTRACT_TEMPLATE = """CONTRATO DE PRESTAÇÃO DE SERVIÇOS

MP ELECTRIC - Serviços Elétricos

---

DADOS DO CONTRATO

Data do Contrato: {data_contrato}
Contrato Nº: {numero_contrato}

CONTRATANTE (Cliente)
Nome/Empresa: {nome_cliente}
CPF/CNPJ: {cpf_cnpj_cliente}
Endereço: {endereco_cliente}
Telefone: {telefone_cliente}
Email: {email_cliente}

CONTRATADA
MP ELECTRIC
Serviços Elétricos Especializados
CNPJ: XX.XXX.XXX/0001-XX

---

DESCRIÇÃO DOS SERVIÇOS

Tipo de Serviço: {tipo_servico}
Descrição Detalhada: {descricao_servico}
Local do Serviço: {local_servico}
Data Prevista de Início: {data_inicio}
Data Prevista de Conclusão: {data_conclusao}

---

CONDIÇÕES COMERCIAIS

Valor do Serviço: R$ {valor_servico}
Forma de Pagamento: {forma_pagamento}
Prazo de Pagamento: {prazo_pagamento}
Materiais Inclusos: {materiais_inclusos}

---

RESPONSABILIDADES

A MP ELECTRIC compromete-se a:
- Executar os serviços com qualidade e segurança
- Utilizar profissionais qualificados
- Respeitar os prazos estabelecidos
- Seguir normas técnicas e de segurança

O CLIENTE compromete-se a:
- Fornecer acesso aos locais de trabalho
- Realizar pagamentos conforme acordado
- Fornecer informações necessárias

---

VALIDADE DO CONTRATO

Este contrato tem validade a partir de {data_contrato} até a conclusão dos serviços ou até {data_validade}.

---

Assinado digitalmente em {data_assinatura}

_____________________________
Representante MP ELECTRIC

_____________________________
Cliente/Contratante
"""

DEFAULT_INVOICE_TEMPLATE = """NOTA FISCAL DE SERVIÇOS

MP ELECTRIC
Serviços Elétricos

---

DADOS DA NOTA

Número da Nota: {numero_nota}
Data de Emissão: {data_emissao}
Competência: {competencia}

CLIENTE
Nome/Empresa: {nome_cliente}
CPF/CNPJ: {cpf_cnpj_cliente}
Endereço: {endereco_cliente}
Telefone: {telefone_cliente}

---

DESCRIÇÃO DOS SERVIÇOS PRESTADOS

Serviço: {descricao_servico}
Período: {periodo_servico}
Valor Unitário: R$ {valor_unitario}
Quantidade: {quantidade}

Valor Total: R$ {valor_total}

---

CONDIÇÕES DE PAGAMENTO

Forma de Pagamento: {forma_pagamento}
Data de Vencimento: {data_vencimento}
Banco: {banco}
Conta: {conta_bancaria}

---

OBSERVAÇÕES

{observacoes}

---

Documento emitido em {data_emissao}
"""

DEFAULT_BUDGET_TEMPLATE = """ORÇAMENTO

MP ELECTRIC
Serviços de Engenharia Elétrica

---

DADOS DO ORÇAMENTO

Orçamento Nº: {numero_orcamento}
Data: {data_orcamento}
Validade: {dias_validade} dias

CLIENTE
Nome/Empresa: {nome_cliente}
Telefone: {telefone_cliente}
Email: {email_cliente}
Local: {local_trabalho}

---

ESCOPO DOS SERVIÇOS

{escopo_servicos}

---

DESCRIÇÃO DETALHADA

Item 1: {item_1}
Valor: R$ {valor_item_1}

Item 2: {item_2}
Valor: R$ {valor_item_2}

Item 3: {item_3}
Valor: R$ {valor_item_3}

---

RESUMO FINANCEIRO

Subtotal: R$ {subtotal}
Impostos: R$ {impostos}
Desconto: R$ {desconto}

VALOR TOTAL: R$ {valor_total}

---

CONDIÇÕES COMERCIAIS

Prazo de Execução: {prazo_execucao}
Validade do Orçamento: {dias_validade} dias
Formas de Pagamento: {formas_pagamento}
Materiais: {materiais}
Garantia: {garantia}

---

OBSERVAÇÕES

{observacoes}

---

Orçamento válido até {data_validade}
Preparado por: MP Electric
"""
