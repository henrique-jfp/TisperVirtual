# TradeComigo - Plataforma Inteligente para Futebol Brasileiro

## 🚀 Visão Geral
Sistema fullstack para análise, consulta e automação de dados de futebol brasileiro. Integra RAG (Retrieval-Augmented Generation), LLMs, Supabase/PostgreSQL, frontend Next.js e backend Flask/FastAPI. Permite queries naturais, estatísticas, histórico de jogos e integração com APIs externas.

---

## 🏗️ Estrutura do Projeto
```
├── backend_server.py         # API Flask principal (Text-to-SQL, RAG)
├── coleta/                   # Módulos de coleta, processamento e agentes RAG
│   ├── rag_agent.py          # Agente LLM para queries SQL
│   ├── banco_dados.py        # Utilitários de banco
│   └── ...                   # Ferramentas de scraping e processamento
├── db/                       # Scripts SQL, DDL, migrações
│   └── create_tables.sql     # Schema do banco
├── dados/                    # Dados brutos, ingestão
├── tools/                    # Scripts utilitários, diagnósticos, automações
├── tests/                    # Testes unitários/integrados (Pytest, Vitest)
├── frontend_next/            # Frontend Next.js (React, Tailwind)
│   ├── app/                  # Páginas e rotas
│   ├── components/           # Componentes UI
│   └── lib/                  # API client, utils
├── static/                   # Arquivos estáticos, CSS
├── .env                      # Configuração de ambiente (chaves, URLs)
├── requirements.txt          # Dependências Python
├── SUPABASE_FIX.md           # Guia de troubleshooting Supabase
└── README.md                 # Documentação principal
```

---

## 🛠️ Tecnologias
- **Backend:** Flask, FastAPI, LangChain, Supabase, PostgreSQL
- **Frontend:** Next.js, React, TailwindCSS
- **LLM:** Groq (Llama3-8b), LangChain-Groq
- **RAG:** Text-to-SQL, custom prompts, few-shot learning
- **Infra:** Supabase, Docker (opcional), PowerShell scripts
- **Testes:** Pytest, Vitest, Supertest

---

## 🔄 Fluxo de Dados
1. Usuário faz pergunta (frontend)
2. Frontend envia para `/ask` (backend Flask)
3. Agente RAG processa, converte para SQL
4. Consulta Supabase/PostgreSQL
5. Resposta formatada e enviada ao frontend

---

## ▶️ Como Executar
### 1. Instalar Dependências
```bash
pip install -r requirements.txt
cd frontend_next && npm install
```
### 2. Configurar `.env`
- Chaves de API (Groq, Supabase)
- URL do banco
### 3. Iniciar Backend
```bash
python backend_server.py
```
### 4. Iniciar Frontend
```bash
cd frontend_next
npm run dev
```

---

## 🧪 Testes
- Todos os testes estão em `tests/`
- Para rodar:
```bash
pytest tests/
```

---

## 🔒 Segurança
- Inputs sanitizados
- Queries parametrizadas
- Nunca expõe stack trace ao usuário
- Variáveis sensíveis no `.env`

---

## 🩺 Troubleshooting
- Veja `SUPABASE_FIX.md` para problemas de banco
- Logs detalhados no backend
- Mensagens de erro informativas para frontend

---

## 🤝 Contribuição
- Siga Clean Architecture
- Testes obrigatórios para PRs
- Documente novas rotas e módulos

---

## 📬 Contato & Suporte
- Para dúvidas técnicas, abra uma issue
- Para bugs, envie stack trace e contexto

---

## 📄 Licença
MIT

---

## 📚 Referências
- [LangChain Docs](https://python.langchain.com/)
- [Supabase Docs](https://supabase.com/docs)
- [Groq API](https://groq.com/)
- [Next.js](https://nextjs.org/)

---

> Projeto desenhado para escalar, seguro e fácil de manter. Ideal para automação, análise e queries inteligentes sobre futebol brasileiro.