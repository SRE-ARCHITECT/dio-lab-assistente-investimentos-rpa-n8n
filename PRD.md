# 📄 PRD.md - Documento de Requisitos de Produto (Product Requirements Document)

## 1. Identificação do Projeto
- **Título**: Assistente Inteligente de Investimentos com RPA e IA Generativa
- **Contexto**: Formação Santander DIO - Automação de Processos com n8n e Python
- **Público-Alvo**: Clientes correntistas e assessores de investimento bancários

---

## 2. Visão do Produto e Problema de Negócio
Instituições financeiras frequentemente possuem dados de clientes distribuídos em interfaces legadas e enfrentam morosidade no cruzamento manual entre o perfil de risco do investidor (Suitability) e a carteira de produtos recomendados.

Este produto automatiza a jornada de assessoria patrimonial ponta a ponta:
1. **Captura sem intervenção humana (RPA)**.
2. **Classificação e elegibilidade instantânea (n8n)**.
3. **Comunicação humanizada e estratégica gerada por IA**.

---

## 3. Requisitos Funcionais (RF)

| ID | Requisito | Descrição |
|---|---|---|
| **RF01** | Extração Web | O robô Python deve raspar a tabela `#clientes` contendo Nome, Email, Saldo e Perfil. |
| **RF02** | Tratamento de Dados | Sanitizar valores monetários formatados em moeda brasileira (`R$ 12.500,00` -> `12500.00`). |
| **RF03** | Ingestão via Webhook | O workflow n8n deve expor endpoint HTTP POST `/webhook/clientes` para receber os dados do RPA. |
| **RF04** | Importação de Portfólio | Consumir a base de investimentos via HTTP GET a partir do arquivo CSV. |
| **RF05** | Motor de Recomendação | Filtrar produtos estritamente aderentes ao perfil (`Conservador`, `Moderado`, `Arrojado`) cujo valor mínimo seja compatível com o saldo do investidor. |
| **RF06** | Síntese por IA Generativa | Gerar texto explicativo personalizado destacando segurança, rentabilidade e adequação ao momento de vida do cliente. |
| **RF07** | Fallback Resiliente | Assegurar que mesmo sem credencial de IA, o sistema gere a recomendação baseada em regras dinâmicas. |
| **RF08** | Template de E-mail | Gerar corpo de e-mail HTML executivo pronto para disparo via Gmail. |

---

## 4. Requisitos Não Funcionais (RNF)

- **RNF01 - Portabilidade**: Executável tanto em ambientes locais (Python 3.10+) quanto na nuvem (Google Colab).
- **RNF02 - Facilidade de Importação**: O fluxo do n8n deve ser 100% importável via copiar/colar (`Ctrl+C` / `Ctrl+V`).
- **RNF03 - Observabilidade**: Mensagens de log em padrão ISO para auditoria de cada requisição.
- **RNF04 - Privacidade**: Nenhuma credencial de API ou chave privada deve ser versionada em código aberto.
