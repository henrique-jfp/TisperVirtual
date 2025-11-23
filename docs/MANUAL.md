# Tipster AI - Coleta de Dados Esportivos

## Visão Geral
Este sistema automatiza a coleta de dados esportivos de sites como Flashscore, sem necessidade de APIs pagas. Usa Playwright para navegação headless, captura XHR JSON ou parsing HTML, processa com Pandas e armazena em SQLite para consultas via RAG/LLM.

## Pré-requisitos
- Python 3.8+
- Playwright instalado e configurado
- Dependências: pandas, beautifulsoup4, sqlite3 (incluído no Python)

## Instalação
1. Instale Python e crie um ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. Instale dependências:
   ```
   pip install playwright pandas beautifulsoup4
   playwright install chromium
   ```

3. Clone ou copie os arquivos do projeto para `C:/TradeComigo`.

## Estrutura de Arquivos
- `coletor.py`: Script principal para coleta.
- `coleta/`: Módulos auxiliares (navegador.py, captura_xhr.py, processador.py, banco.py).
- `dados_raw/`: JSONs capturados (temporários).
- `dados/`: Banco SQLite (sports_data.db).

## Como Usar
### Coleta Básica
Execute o coletor com uma URL de partida:
```
python coletor.py "https://www.flashscore.com/match/football/ceara-p0JrJCV5/internacional-tSCiHj0I/?mid=CErzIAye" 5
```
- Parâmetros: URL (string), segundos de espera (int, padrão 10).

### Exemplo de URLs
- Partida específica: `https://www.flashscore.com/match/football/equipe1-equipe2/?mid=ID`
- Liga: `https://www.flashscore.com/football/brazil/serie-a/` (parsing limitado a HTML, pode não extrair todas as partidas).

### Processamento
- O sistema captura XHR JSON (preferencial) ou fallback para HTML.
- Normaliza dados em DataFrames: partidas (id, times, placar, data, liga, status), estatísticas (opcional).
- Salva em SQLite automaticamente.

### Consulta de Dados
Após coleta, consulte o banco:
```python
import sqlite3
conn = sqlite3.connect('dados/sports_data.db')
c = conn.cursor()
c.execute('SELECT * FROM partidas')
print(c.fetchall())
conn.close()
```

### Limitações
- Parsing HTML específico para Flashscore; títulos de partida devem seguir formato "CEA 1-2 INT | Ceara v Internacional DD/MM/YYYY".
- XHRs dinâmicos podem não ser capturados; ajuste filtros em captura_xhr.py se necessário.
- Para ligas, implementar scraping adicional de tabelas HTML.
- Dados históricos limitados à disponibilidade do site.

### Expansão
- Para múltiplas URLs: loop no coletor ou script batch.
- Integração com RAG: Use dados do SQLite para embeddings e queries LLM.
- Debug: Ver logs em console; arquivos em dados_raw/ para inspeção.

## Captura de Estatísticas'

### Como coletar estatísticas de partidas
1. Execute o coletor normalmente com a URL da partida:
   ```
   python coletor.py "https://www.flashscore.com/match/football/ceara-p0JrJCV5/internacional-tSCiHj0I/?mid=CErzIAye" 5
   ```
2. O sistema tentará capturar estatísticas via XHR JSON. Se não houver, pode ser necessário ajustar o parsing em `processador.py` para buscar estatísticas no HTML (ex: posse de bola, finalizações, escanteios).
3. As estatísticas são normalizadas e salvas na tabela `estatisticas` do banco `dados/sports_data.db`.

### Consulta manual das estatísticas
Execute no terminal Python:
```python
import sqlite3
conn = sqlite3.connect('dados/sports_data.db')
c = conn.cursor()
c.execute('SELECT * FROM estatisticas')
for row in c.fetchall():
    print(row)
conn.close()
```
- Cada linha: (id, id_partida, tipo_estatistica, valor_casa, valor_fora)

### Teste no chat do Tipster AI
1. Após coletar e validar estatísticas no banco, faça perguntas naturais no chat, por exemplo:
   - "Quantos escanteios o Ceará teve contra o Internacional?"
   - "Qual foi a posse de bola do Internacional na última partida?"
2. O backend do Tipster AI deve:
   - Interpretar entidades (time, tipo de estatística, data/partida).
   - Gerar uma query SQL:
     ```sql
     SELECT valor_casa FROM estatisticas WHERE tipo_estatistica LIKE '%escanteio%' AND id_partida = 'CErzIAye'
     ```
   - Retornar o valor encontrado, formatando a resposta para o usuário.

### Observações
- Se não houver estatísticas, revise o parsing em `processador.py` para buscar elementos HTML correspondentes (ex: divs, spans com dados estatísticos).
- Para novas estatísticas, adicione o tipo desejado no parser e normalize para o banco.
- Sempre valide no banco antes de testar no chat.

## Suporte
Sistema crash-proof; erros logados. Para issues, verifique dependências e URLs válidas.