# Problema de Conexão com Supabase

## Diagnóstico
O sistema detectou que a instância do Supabase configurada não está acessível. Isso geralmente acontece quando:

1. **Instância gratuita expirou** - As instâncias gratuitas do Supabase têm limite de tempo
2. **Instância foi pausada/desativada** - Por inatividade ou problemas de cobrança
3. **URL/DATABASE_URL incorreta** - A string de conexão pode ter mudado

## Solução

### 1. Verificar Status da Instância
1. Acesse [supabase.com](https://supabase.com)
2. Faça login na sua conta
3. Verifique se a instância `nflmvptqgicabovfmnos` ainda existe
4. Se estiver pausada, reative-a

### 2. Criar Nova Instância (se necessário)
1. No dashboard do Supabase, clique em "New Project"
2. Configure um novo banco PostgreSQL
3. Copie a nova `DATABASE_URL` do painel de configurações
4. Atualize o arquivo `.env` com a nova URL

### 3. Atualizar Configuração
Edite o arquivo `.env` e substitua a `DATABASE_URL`:

```env
DATABASE_URL=postgresql://postgres:[SENHA]@[NOVO_HOST]:5432/postgres
```

### 4. Testar Conexão
Após atualizar a configuração, reinicie o backend:

```bash
python backend_server.py
```

## Status Atual
- ✅ Backend server inicia corretamente
- ✅ Tratamento de erros implementado
- ❌ Agente RAG indisponível (banco offline)
- ❌ Frontend não consegue fazer queries

O sistema continuará funcionando assim que a conexão com o banco for restaurada.