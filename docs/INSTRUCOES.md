# Guia de Operação: Motor de Extração de Dados

Este guia descreve o processo para configurar e executar o motor de extração de dados. O sistema foi projetado para ser genérico: a lógica de extração é separada da configuração do alvo. Você pode definir novos sites e dados para extrair **sem alterar o código Python**, apenas editando o arquivo `config.yaml`.

## 1. Arquitetura

O sistema é modular e orientado a configuração:

- **`config.yaml`**: O cérebro da operação. Aqui você define *o que* e *como* extrair. Cada "alvo" neste arquivo representa um site ou uma seção de um site a ser processado.
- **`main.py`**: O motor. Ele lê o `config.yaml`, entende qual alvo você quer executar (via argumento de linha de comando) e orquestra os outros módulos para executar a tarefa. **É o único arquivo que você precisa executar.**
- **`navegador.py`**: Controla o browser (Playwright).
- **`captura_xhr.py`**: Intercepta e salva o tráfego de rede relevante.
- **`processador.py`**: Normaliza os dados brutos capturados.
- **`banco_dados.py`**: Persiste os dados processados em um banco de dados.

## 2. Configuração do Ambiente

### Passo 2.1: Instalar Dependências

Certifique-se de que o Python 3.8+ está instalado.

```bash
# Instala as bibliotecas Python necessárias
pip install -r requirements.txt

# Instala o navegador que o Playwright irá controlar
playwright install chromium
```

### Passo 2.2: Configurar o Banco de Dados

O sistema usa por padrão um banco local SQLite para execução em servidores domésticos (Termux). Se desejar, é possível apontar para um Postgres remoto substituindo a URL de conexão.

1.  **Configuração local (recomendada):** defina em `.env`:

  ```env
  DATABASE_URL=sqlite:///./db/tradecomigo.sqlite3
  ```

2.  **Configuração remota (opcional):** se você for usar um Postgres remoto, forneça a URL no mesmo formato:

  ```env
  DATABASE_URL="postgresql://SEU_USUARIO:SUA_SENHA@SEU_HOST:5432/SEU_BANCO"
  ```

## 3. Como Capturar Dados

O processo é: **Analisar, Configurar e Executar.**

### Passo 3.1: Análise do Site Alvo (Reconhecimento)

Esta é a única etapa manual, onde você atua como um analista.

1.  Abra o site alvo no seu navegador (ex: Chrome) e abra as **Ferramentas de Desenvolvedor** (`F12`).
2.  Vá para a aba **"Network" (Rede)** e filtre por **"Fetch/XHR"**.
3.  Execute a ação que carrega os dados desejados (clicar em um botão, rolar a página, etc.).
4.  Observe as requisições que aparecem. Encontre a que contém os dados JSON que você quer.
5.  Anote as seguintes informações:
    - **`url`**: A URL da página que você precisa visitar.
    - **`espera_inicial`**: O seletor CSS de um elemento que prova que a página carregou inicialmente.
    - **`acao_clique`**: O seletor CSS do elemento em que você precisa clicar.
    - **`espera_pos_acao`**: O seletor CSS de um elemento que aparece *depois* do clique.
    - **`filtros_url`**: Uma parte única da URL da requisição XHR que contém os dados.

### Passo 3.2: Configuração do `config.yaml`

Abra o arquivo `config.yaml`. As informações coletadas acima são traduzidas diretamente para um novo alvo.

```yaml
alvos:
  # Nome único para o seu alvo. Você usará isso para executá-lo.
  meu_novo_alvo:
    # URL da página inicial a ser aberta.
    url: "https://www.exemplo.com/dados"
    
    # Descrição do que este alvo faz.
    descricao: "Captura dados da seção X do site Exemplo."
    
    seletores:
      # Coloque aqui o seletor de espera inicial.
      espera_inicial: "#conteudo-principal"
      
      # Coloque aqui o seletor do botão/link a ser clicado.
      acao_clique: "button.carregar-mais"
      
      # Coloque aqui o seletor que confirma o carregamento após o clique.
      espera_pos_acao: ".item-carregado"
      
    filtros_url:
      # Coloque aqui a parte única da URL da API.
      - "/api/v2/dados"
      
    # Nome base para os arquivos JSON salvos.
    nome_base_arquivo: "dados_exemplo"
```
Você pode adicionar quantos alvos quiser ao arquivo.

### Passo 3.3: Execução

Execute o motor a partir do seu terminal, passando o **nome do alvo** que você definiu no `config.yaml` como um argumento.

```bash
# Executa o alvo 'flashscore_futebol'
python main.py flashscore_futebol

# Executa o 'meu_novo_alvo' que você acabou de criar
python main.py meu_novo_alvo
```

O motor irá ler a configuração do alvo especificado e executar todo o processo automaticamente.

## 4. Verificação

Após a execução, conecte-se ao seu banco de dados e verifique se os dados foram inseridos:

```sql
SELECT * FROM partidas LIMIT 10;
SELECT * FROM estatisticas LIMIT 10;
```

Se as tabelas estiverem populadas, a missão foi um sucesso.
