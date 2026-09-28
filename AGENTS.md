# 🤖 AGENTS.md - Guia de Contexto e Diretrizes para Agentes de IA

## 1. Escopo e Diretrizes
Este repositório contém a implementação do desafio **"Criando um Processo de RPA com N8N e Python"** (Assistente de Investimentos com RPA e IA Generativa) da formação Santander na DIO.

Ao manter ou expandir este repositório, os agentes de IA devem obedecer às seguintes diretrizes:

1. **Linguagem & Comunicação**: Todo conteúdo, comentários de código e saídas para o usuário devem ser estritamente em **português do Brasil**.
2. **Edição Cirúrgica**: Nunca reescrever arquivos completos sem necessidade; aplicar alterações pontuais.
3. **Segurança de Segredos**: Nunca expor chaves de API do Google Gemini, OpenAI ou credenciais OAuth do Gmail em arquivos de código ou `.json`.
4. **Compatibilidade com n8n**: O arquivo `n8n/workflow.json` deve manter nós com posições consistentes e formato válido para importação direta via clipboard no n8n.

---

## 2. Estrutura dos Nós n8n
- **Webhook - Ingest RPA**: Endpoint POST que recebe `{ "clientes": [...] }`.
- **Split Out Clientes**: Desmembra a lista para execução paralela por cliente.
- **HTTP - Buscar Investimentos CSV**: Download dinâmico de `docs/data.csv`.
- **Code - Parse CSV Investimentos**: Transforma texto CSV delimitado por vírgula em array de objetos JSON.
- **Code - Cruzar Perfil e Investimentos**: Mapeia compatibilidade de risco e liquidez.
- **AI Agent - Consultor de Investimentos**: Prompt com personas especializadas (Certificação CEA/CFP).
- **Briefing Email & Fallback MVP**: Proteção contra falha de IA e gerador do HTML corporativo.
- **Gmail / Respond to Webhook**: Nós de entrega e retorno de status.

---

## 3. Comandos Úteis

### Execução do Script Python Localmente
```bash
python rpa/extrair_clientes.py http://localhost:5678/webhook/clientes
```

### Validação de Sintaxe Python
```bash
python -m py_compile rpa/extrair_clientes.py
```
