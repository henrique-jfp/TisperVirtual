import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import time
import re
import pandas as pd
from icalendar import Calendar
import yaml
from PIL import Image
import fitz  # PyMuPDF
from google.cloud import vision
import io

# Configurações
TSDB_KEY = "123"
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{TSDB_KEY}"
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
# embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo de embeddings gratuito

# Inicializar ChromaDB
 # ...existing code...
# ...existing code...

# Funções para integração com a API-Football
API_FOOTBALL_KEY = os.environ.get("API_FOOTBALL_KEY") or os.environ.get("RAPIDAPI_KEY") or os.environ.get("X_APISPORTS_KEY")
API_FOOTBALL_URL = "https://v3.football.api-sports.io"
DEFAULT_SEASON = int(os.environ.get("DEFAULT_SEASON", 2025))

def get_api_football_headers():
    """Constrói cabeçalhos corretos para a API-Football.

    Suporta duas formas de autenticação:
    - Chave direta da API-Football em `API_FOOTBALL_KEY` -> usa `x-apisports-key`.
    - Chave via RapidAPI em `RAPIDAPI_KEY` -> usa `x-rapidapi-key` e `x-rapidapi-host`.
    """
    if os.environ.get('API_FOOTBALL_KEY'):
        return {"x-apisports-key": os.environ.get('API_FOOTBALL_KEY')}
    if os.environ.get('RAPIDAPI_KEY'):
        return {
            "x-rapidapi-key": os.environ.get('RAPIDAPI_KEY'),
            "x-rapidapi-host": "v3.football.api-sports.io"
        }
    if os.environ.get('X_APISPORTS_KEY'):
        return {"x-apisports-key": os.environ.get('X_APISPORTS_KEY')}
    return {}

HEADERS = get_api_football_headers()

def rate_limited_request(url, headers=None, params=None, max_retries=5, delay=1):
    """Realiza uma requisição com controle de taxa, leitura de cabeçalhos e tentativas."""
    headers = headers or {}
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
        except requests.RequestException as e:
            print(f"RequestException ao acessar {url}: {e} (tentativa {attempt}/{max_retries})")
            time.sleep(delay)
            delay *= 2
            continue

        # Ler limites de taxa quando disponível
        remaining_min = response.headers.get("X-RateLimit-Remaining") or response.headers.get("x-ratelimit-requests-remaining")
        if remaining_min is not None:
            try:
                rem = int(remaining_min)
                if rem <= 0:
                    wait = int(response.headers.get("X-RateLimit-Limit", 60))
                    print(f"Rate limit atingido (remaining=0). Aguardando {wait} segundos...")
                    time.sleep(wait)
                    continue
            except ValueError:
                pass

        if response.status_code == 429:
            print(f"429 Too Many Requests para {url}. Backoff e nova tentativa (tentativa {attempt}).")
            time.sleep(delay)
            delay *= 2
            continue

        if response.status_code in (500, 502, 503, 504):
            print(f"Erro servidor {response.status_code} em {url}. Tentativa {attempt}/{max_retries}.")
            time.sleep(delay)
            delay *= 2
            continue

        # 204 No Content -> retornar vazio
        if response.status_code == 204:
            return response

        # Caso comum: retornar response para que chamador verifique status
        return response

    print(f"Falha após {max_retries} tentativas para {url}")
    return None

def buscar_ligas_api_football():
    """Busca ligas disponíveis na API-Football."""
    url = f"{API_FOOTBALL_URL}/leagues"
    headers = get_api_football_headers()
    response = rate_limited_request(url, headers=headers)
    if not response:
        print("Erro ao buscar ligas na API-Football: sem resposta.")
        return []
    if not response.ok:
        print(f"Erro ao buscar ligas na API-Football: status {response.status_code}")
        return []
    try:
        return response.json().get('response', [])
    except Exception as e:
        print(f"Erro ao decodificar JSON em buscar_ligas_api_football: {e}")
        return []

def buscar_times_por_liga_api_football(id_liga, season=DEFAULT_SEASON):
    """Busca times de uma liga específica na API-Football."""
    params = {"league": id_liga, "season": season}
    url = f"{API_FOOTBALL_URL}/teams"
    print(f"URL gerada: {url} params={params}")
    headers = get_api_football_headers()
    response = rate_limited_request(url, headers=headers, params=params)
    if not response:
        print(f"Erro ao buscar times da liga {id_liga}: sem resposta")
        return []
    print(f"Status Code: {response.status_code}")
    if not response.ok:
        print(f"Erro ao buscar times: status {response.status_code}")
        return []
    try:
        data = response.json()
        print(f"Resposta da API: resultados={len(data.get('response', []))}")
        return data.get('response', [])
    except Exception as e:
        print(f"Erro ao decodificar JSON: {e}")
        return []

def buscar_jogos_por_time_api_football(id_time, season=DEFAULT_SEASON):
    """Busca jogos de um time específico na API-Football."""
    params = {"team": id_time, "season": season}
    url = f"{API_FOOTBALL_URL}/fixtures"
    headers = get_api_football_headers()
    response = rate_limited_request(url, headers=headers, params=params)
    if not response:
        print(f"Erro ao buscar jogos do time {id_time}: sem resposta")
        return []
    if response.status_code == 204:
        return []
    if response.ok:
        try:
            return response.json().get('response', [])
        except Exception as e:
            print(f"Erro ao decodificar JSON em buscar_jogos_por_time_api_football: {e}")
    print(f"Erro ao buscar jogos do time {id_time}: status {response.status_code}")
    return []

def buscar_jogadores_por_time_api_football(id_time, season=DEFAULT_SEASON):
    """Busca jogadores de um time específico na API-Football."""
    params = {"team": id_time, "season": season}
    url = f"{API_FOOTBALL_URL}/players"
    headers = get_api_football_headers()
    response = rate_limited_request(url, headers=headers, params=params)
    if not response:
        print(f"Erro ao buscar jogadores do time {id_time}: sem resposta")
        return []
    if response.status_code == 204:
        return []
    if response.ok:
        try:
            return response.json().get('response', [])
        except Exception as e:
            print(f"Erro ao decodificar JSON em buscar_jogadores_por_time_api_football: {e}")
    print(f"Erro ao buscar jogadores do time {id_time}: status {response.status_code}")
    return []

def buscar_dados_time(time_nome):
    """Busca dados básicos do time."""
    url_busca = f"{BASE_URL}/searchteams.php?t={time_nome}"
    r = requests.get(url_busca)
    data = r.json()
    if not data['teams']:
        return None
    return data['teams'][0]

def buscar_proximos_jogos(team_id):
    """Busca próximos jogos do time."""
    url_jogos = f"{BASE_URL}/eventsnext.php?id={team_id}"
    r_jogos = requests.get(url_jogos)
    data_jogos = r_jogos.json()
    if not data_jogos or not data_jogos['events']:
        return []
    return data_jogos['events']

def buscar_ultimos_resultados(team_id, limit=10):
    """Busca últimos resultados."""
    url_last = f"{BASE_URL}/eventslast.php?id={team_id}"
    r_last = requests.get(url_last)
    if r_last.status_code != 200:
        print(f"Erro ao buscar últimos resultados para o time {team_id}: {r_last.status_code}")
        return []
    try:
        data_last = r_last.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Resposta inválida ao buscar últimos resultados para o time {team_id}.")
        return []

    if not data_last or not data_last.get('results'):
        print(f"Nenhum resultado encontrado para o time {team_id}.")
        return []
    return data_last['results'][:limit]


def find_team_api_football(team_name: str) -> dict | None:
    """Tenta localizar um time na API-Football por nome. Retorna o objeto do time ou None.

    Estratégia:
    - Chama `/teams` com parâmetro `search` quando disponível.
    - Se não encontrar, tenta obter times da Série A (liga 71) e faz correspondência por substring.
    """
    headers = get_api_football_headers()
    params = {"search": team_name}
    try:
        url = f"{API_FOOTBALL_URL}/teams"
        resp = requests.get(url, headers=headers, params=params, timeout=8)
        if resp.ok:
            data = resp.json().get('response', [])
            if data:
                return data[0].get('team') if isinstance(data[0].get('team'), dict) else data[0]
    except requests.RequestException:
        pass

    # fallback: buscar times da liga Serie A e tentar casar por substring
    try:
        teams = buscar_times_por_liga_api_football(71, season=DEFAULT_SEASON)
        name_lower = team_name.lower()
        for t in teams:
            candidate = t.get('team', {}) if isinstance(t.get('team'), dict) else t.get('team')
            if not candidate:
                # older API shapes
                candidate = t
            cand_name = (candidate.get('name') or candidate.get('team', {}).get('name') if isinstance(candidate, dict) else None)
            if not cand_name:
                # try other keys
                cand_name = candidate.get('team', {}).get('name') if isinstance(candidate, dict) and 'team' in candidate else None
            if cand_name and name_lower in cand_name.lower():
                return candidate
    except Exception:
        pass

    return None


def get_recent_matches_detailed(team_name: str, limit: int = 5) -> list:
    """Retorna os últimos `limit` jogos para `team_name` usando somente a API-Football.

    Cada item contém: date, opponent, venue ('home'|'away'), score, goals_for, goals_against,
    yellow_cards, red_cards, corners (N/A se não disponíveis).
    """
    api_key = API_FOOTBALL_KEY
    headers = get_api_football_headers()
    if not api_key:
        return []

    team_obj = find_team_api_football(team_name)
    if not team_obj:
        return []

    team_id = team_obj.get('id') or team_obj.get('team_id') or team_obj.get('idTeam')
    if not team_id:
        return []

    # Buscar últimos jogos via endpoint fixtures com parâmetro last
    try:
        url = f"{API_FOOTBALL_URL}/fixtures"
        params = {"team": team_id, "season": DEFAULT_SEASON, "last": limit}
        resp = requests.get(url, headers=headers, params=params, timeout=8)
        if not resp.ok:
            return []
        fixtures = resp.json().get('response', [])
    except requests.RequestException:
        return []

    detailed = []
    for fix in fixtures:
        fixture = fix.get('fixture', {})
        teams = fix.get('teams', {})
        goals = fix.get('goals', {})
        date = fixture.get('date') or fixture.get('timestamp')

        home = teams.get('home', {})
        away = teams.get('away', {})

        # Determine perspective
        if str(team_id) == str(home.get('id')) or team_name.lower() in (home.get('name') or '').lower():
            venue = 'home'
            opponent = away.get('name')
            gf = goals.get('home')
            ga = goals.get('away')
            team_stats_id = home.get('id')
        else:
            venue = 'away'
            opponent = home.get('name')
            gf = goals.get('away')
            ga = goals.get('home')
            team_stats_id = away.get('id')

        entry = {
            'date': date.split('T')[0] if isinstance(date, str) and 'T' in date else date,
            'opponent': opponent,
            'venue': venue,
            'score': f"{gf if gf is not None else 'N/A'}-{ga if ga is not None else 'N/A'}",
            'goals_for': gf if gf is not None else 'N/A',
            'goals_against': ga if ga is not None else 'N/A',
            'yellow_cards': 'N/A',
            'red_cards': 'N/A',
            'corners': 'N/A'
        }

        # Try to enrich via fixtures/statistics endpoint
        try:
            fid = fixture.get('id')
            if fid:
                stats_url = f"{API_FOOTBALL_URL}/fixtures/statistics"
                sresp = requests.get(stats_url, headers=headers, params={"fixture": fid}, timeout=8)
                if sresp.ok:
                    sdata = sresp.json().get('response', [])
                    for team_stats in sdata:
                        t = team_stats.get('team', {})
                        t_id = t.get('id') or t.get('team_id')
                        if str(t_id) == str(team_stats_id) or team_name.lower() in (t.get('name') or '').lower():
                            for stat in team_stats.get('statistics', []):
                                label = (stat.get('type') or '').lower()
                                value = stat.get('value')
                                if 'corner' in label:
                                    entry['corners'] = value
                                if 'yellow' in label:
                                    entry['yellow_cards'] = value
                                if 'red' in label:
                                    entry['red_cards'] = value
        except requests.RequestException:
            pass

        detailed.append(entry)

    return detailed


# (antiga função baseada no TheSportsDB removida — usamos apenas API-Football agora)

def buscar_tabela_liga(id_league):
    """Busca tabela da liga."""
    url_table = f"{BASE_URL}/lookuptable.php?l={id_league}"
    r_table = requests.get(url_table)
    data_table = r_table.json()
    return data_table.get('table', []) if data_table else []

def armazenar_dados_rag(time_nome):
    """Coleta e armazena dados no ChromaDB para RAG."""
    time_obj = buscar_dados_time(time_nome)
    if not time_obj:
        print(f"Time {time_nome} não encontrado.")
        return

    team_id = time_obj['idTeam']
    jogos = buscar_proximos_jogos(team_id)
    resultados = buscar_ultimos_resultados(team_id)

    # Preparar documentos para embeddings
    documentos = []
    metadados = []
    ids = []

    # Adicionar descrição do time
    desc = time_obj.get('strDescriptionEN', 'Sem descrição')
    documentos.append(f"Descrição do time {time_nome}: {desc}")
    metadados.append({"tipo": "descricao_time", "time": time_nome})
    ids.append(f"{time_nome}_desc")

    # Adicionar resultados
    for i, res in enumerate(resultados):
        texto = f"Jogo: {res['strHomeTeam']} {res.get('intHomeScore', 'N/A')} x {res.get('intAwayScore', 'N/A')} {res['strAwayTeam']} em {res.get('dateEvent', 'N/A')}"
        documentos.append(texto)
        metadados.append({"tipo": "resultado", "time": time_nome, "data": res.get('dateEvent')})
        ids.append(f"{time_nome}_resultado_{i}")

    # Adicionar próximos jogos
    for i, jogo in enumerate(jogos):
        texto = f"Próximo jogo: {jogo['strHomeTeam']} vs {jogo['strAwayTeam']} em {jogo['dateEvent']} no {jogo['strVenue']}"
        documentos.append(texto)
        metadados.append({"tipo": "proximo_jogo", "time": time_nome, "data": jogo['dateEvent']})
        ids.append(f"{time_nome}_jogo_{i}")

    # Se houver liga, adicionar tabela
    if jogos:
        id_league = jogos[0].get('idLeague')
        if id_league:
            tabela = buscar_tabela_liga(id_league)
            for i, pos in enumerate(tabela[:10]):  # Top 10
                texto = f"Posição {i+1}: {pos['strTeam']} - Pontos: {pos.get('intPoints', 'N/A')}, Jogos: {pos.get('intPlayed', 'N/A')}"
                documentos.append(texto)
                metadados.append({"tipo": "tabela_liga", "liga": jogos[0]['strLeague']})
                ids.append(f"liga_{id_league}_pos_{i}")

    # Gerar embeddings e armazenar
    print(f"Dados de {time_nome} armazenados no RAG!")
    print(f"Dados de {time_nome} armazenados no RAG!")

def consultar_rag(query, n_results=5):
    """Consulta o RAG para contexto relevante."""
    query_embedding = get_embedder().encode([query])
    results = get_collection().query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results
    )
    return results['documents'][0] if results['documents'] else []

def processar_imagem_para_markdown(imagem_path):
    """Processa uma imagem usando Google Vision API para OCR e retorna texto em formato Markdown."""
    try:
        # Configurar cliente Google Vision
        client = vision.ImageAnnotatorClient()
        
        # Carregar imagem
        with io.open(imagem_path, 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        
        # Detectar texto
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if not texts:
            return ""
        
        # Texto completo
        texto_completo = texts[0].description
        
        # Estruturar em Markdown
        linhas = texto_completo.split('\n')
        markdown = ""
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
            # Detectar headings (linhas maiúsculas ou com padrões)
            if linha.isupper() and len(linha) < 50:
                markdown += f"# {linha}\n\n"
            elif linha.startswith(('1.', '2.', '3.', '-')):
                markdown += f"{linha}\n"
            else:
                markdown += f"{linha}\n\n"
        return markdown.strip()
    except Exception as e:
        print(f"Erro ao processar imagem {imagem_path} com Google Vision: {e}")
        return ""

def processar_pdf_para_markdown(pdf_path):
    """Processa um PDF e converte para Markdown estruturado."""
    try:
        doc = fitz.open(pdf_path)
        markdown = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            texto = page.get_text()
            # Estruturar: detectar headings, listas, etc.
            linhas = texto.split('\n')
            for linha in linhas:
                linha = linha.strip()
                if not linha:
                    continue
                # Simples heurística para headings
                if len(linha) < 100 and linha[0].isupper() and not linha.endswith('.'):
                    markdown += f"## {linha}\n\n"
                else:
                    markdown += f"{linha}\n\n"
        doc.close()
        return markdown.strip()
    except Exception as e:
        print(f"Erro ao processar PDF {pdf_path}: {e}")
        return ""


def processar_pdf_e_armazenar(pdf_path, categoria="livros"):
    """Processa um PDF, converte para Markdown e armazena no ChromaDB."""
    markdown_texto = processar_pdf_para_markdown(pdf_path)
    if not markdown_texto:
        print(f"Falha ao extrair texto do PDF {pdf_path}")
        return
    
    # Salvar Markdown temporário
    md_path = pdf_path.replace('.pdf', '.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown_texto)
    
    # Processar como Markdown
    processar_markdown_e_armazenar(md_path, categoria)
    print(f"PDF {pdf_path} convertido para Markdown e armazenado na categoria {categoria}!")
    """Processa um arquivo Markdown, divide por headings e armazena no ChromaDB."""
    if not os.path.exists(md_path):
        print(f"Arquivo não encontrado: {md_path}")
        return 0

    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Encontrar seções por headings
    pattern = re.compile(r'(^#{1,6}\s.*$)', re.MULTILINE)
    matches = list(pattern.finditer(text))

    parts = []
    if not matches:
        # Sem headings, chunk simples
        for i in range(0, len(text), chunk_size):
            parts.append(("document", text[i:i+chunk_size].strip()))
    else:
        for i, m in enumerate(matches):
            start = m.start()
            header = m.group().strip()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            content = text[start:end].strip()
            # Quebrar em pedaços menores
            for j in range(0, len(content), chunk_size):
                chunk = content[j:j+chunk_size].strip()
                if chunk:
                    parts.append((header, chunk))

    documentos = []
    metadados = []
    ids = []
    base = os.path.basename(md_path).replace('.', '_')
    for idx, (secao, chunk) in enumerate(parts):
        doc = f"{secao}\n\n{chunk}"
        documentos.append(doc)
        metadados.append({"categoria": "livros", "tipo": "markdown", "origem": md_path, "secao": secao})
        ids.append(f"{base}_secao_{idx}")

    if not documentos:
        print("Nenhum conteúdo extraído do Markdown.")
        return 0

    embeddings = get_embedder().encode(documentos)
    get_collection().add(
        documents=documentos,
        metadatas=metadados,
        ids=ids,
        embeddings=embeddings.tolist()
    )
    print(f"{len(documentos)} blocos do Markdown {md_path} indexados no RAG.")
    return len(documentos)

def processar_csv_json(dados, categoria, chunk_size=500):
    """Processa dados de CSV ou JSON e armazena no ChromaDB."""
    documentos = []
    metadados = []
    ids = []
    
    if isinstance(dados, str):
        if dados.endswith('.csv'):
            df = pd.read_csv(dados)
        elif dados.endswith('.json'):
            with open(dados, 'r') as f:
                data = json.load(f)
            df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame([data])
        else:
            # Assume texto JSON
            data = json.loads(dados)
            df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame([data])
    else:
        df = pd.DataFrame(dados)
    
    texto_completo = df.to_string()
    partes = [texto_completo[i:i+chunk_size] for i in range(0, len(texto_completo), chunk_size)]
    
    for i, parte in enumerate(partes):
        documentos.append(parte)
        metadados.append({"categoria": categoria, "tipo": "dados_estruturados", "origem": "csv_json"})
        ids.append(f"{categoria}_dados_{i}")
    
    embeddings = get_embedder().encode(documentos)
    get_collection().add(
        documents=documentos,
        metadatas=metadados,
        ids=ids,
        embeddings=embeddings.tolist()
    )
    print(f"Dados estruturados processados e armazenados na categoria {categoria}!")

def processar_ics(ics_path, categoria):
    """Processa arquivo ICS e armazena eventos no ChromaDB."""
    with open(ics_path, 'r') as f:
        cal = Calendar.from_ical(f.read())
    
    documentos = []
    metadados = []
    ids = []
    
    for i, component in enumerate(cal.walk()):
        if component.name == "VEVENT":
            summary = component.get('summary')
            start = component.get('dtstart').dt if component.get('dtstart') else 'N/A'
            location = component.get('location') or 'N/A'
            texto = f"Evento: {summary} em {start} no {location}"
            documentos.append(texto)
            metadados.append({"categoria": categoria, "tipo": "evento", "origem": ics_path})
            ids.append(f"{categoria}_evento_{i}")
    
    if documentos:
        embeddings = get_embedder().encode(documentos)
        get_collection().add(
            documents=documentos,
            metadatas=metadados,
            ids=ids,
            embeddings=embeddings.tolist()
        )
        print(f"Eventos do ICS processados e armazenados na categoria {categoria}!")
    else:
        print("Nenhum evento encontrado no ICS.")

def processar_yaml(yaml_path, categoria, chunk_size=500):
    """Processa arquivo YAML e armazena como texto no ChromaDB."""
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    texto = yaml.dump(data)
    partes = [texto[i:i+chunk_size] for i in range(0, len(texto), chunk_size)]
    
    documentos = []
    metadados = []
    ids = []
    
    for i, parte in enumerate(partes):
        documentos.append(parte)
        metadados.append({"categoria": categoria, "tipo": "documentacao", "origem": yaml_path})
        ids.append(f"{categoria}_yaml_{i}")
    
    embeddings = get_embedder().encode(documentos)
    get_collection().add(
        documents=documentos,
        metadatas=metadados,
        ids=ids,
        embeddings=embeddings.tolist()
    )
    print(f"YAML processado e armazenado na categoria {categoria}!")

def processar_manual(titulo, texto, categoria):
    """Processa texto manual e armazena no ChromaDB."""
    documentos = [texto]
    metadados = [{"categoria": categoria, "tipo": "manual", "titulo": titulo}]
    ids = [f"manual_{titulo.replace(' ', '_')}"]
    
    embeddings = get_embedder().encode(documentos)
    get_collection().add(
        documents=documentos,
        metadatas=metadados,
        ids=ids,
        embeddings=embeddings.tolist()
    )
    print(f"Nota manual '{titulo}' armazenada na categoria {categoria}!")

def armazenar_dados_coletados_api(dados, categoria="api_coletada"):
    """Armazena dados coletados por API no ChromaDB."""
    if isinstance(dados, dict):
        texto = json.dumps(dados)
    elif isinstance(dados, list):
        texto = "\n".join([json.dumps(item) for item in dados])
    else:
        texto = str(dados)
    
    partes = [texto[i:i+500] for i in range(0, len(texto), 500)]
    documentos = []
    metadados = []
    ids = []
    
    for i, parte in enumerate(partes):
        documentos.append(parte)
        metadados.append({"categoria": categoria, "tipo": "dados_api", "origem": "coletor"})
        ids.append(f"api_coletada_{i}")
    
    embeddings = get_embedder().encode(documentos)
    get_collection().add(
        documents=documentos,
        metadatas=metadados,
        ids=ids,
        embeddings=embeddings.tolist()
    )
    print(f"Dados da API armazenados na categoria {categoria}!")

def buscar_times_brasileiros():
    """Busca times brasileiros na API TheSportsDB."""
    url_times = f"{BASE_URL}/search_all_teams.php?s=Soccer&c=Brazil"
    r_times = requests.get(url_times)
    data_times = r_times.json()
    if not data_times or not data_times['teams']:
        print("Nenhum time brasileiro encontrado.")
        return []
    return data_times['teams']

def armazenar_dados_rag_api_football(time_nome, id_time, id_liga):
    """Coleta e armazena dados no ChromaDB usando a API-Football."""
    jogos = buscar_jogos_por_time_api_football(id_time)
    times_liga = buscar_times_por_liga_api_football(id_liga)

    # Preparar documentos para embeddings
    documentos = []
    metadados = []
    ids = []

    # Adicionar próximos jogos
    for i, jogo in enumerate(jogos[:5]):
        texto = f"Próximo jogo: {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']} em {jogo['fixture']['date']}"
        documentos.append(texto)
        metadados.append({"tipo": "proximo_jogo", "time": time_nome, "data": jogo['fixture']['date']})
        ids.append(f"{time_nome}_jogo_{i}")

    # Adicionar times da liga
    for i, time in enumerate(times_liga[:5]):
        texto = f"Time: {time['team']['name']} - Fundado em {time['team']['founded']}"
        documentos.append(texto)
        metadados.append({"tipo": "time_liga", "liga": id_liga, "time": time['team']['name']})
        ids.append(f"liga_{id_liga}_time_{i}")

    # Gerar embeddings e armazenar
    embeddings = get_embedder().encode(documentos)
    get_collection().add(
        documents=documentos,
        metadatas=metadados,
        ids=ids,
        embeddings=embeddings.tolist()
    )
    print(f"Dados de {time_nome} armazenados no RAG usando API-Football!")

def armazenar_dados_completos_api_football(time_nome, id_time, id_liga):
    """Coleta e armazena dados completos no ChromaDB usando a API-Football."""
    jogos = buscar_jogos_por_time_api_football(id_time)
    times_liga = buscar_times_por_liga_api_football(id_liga)
    jogadores = buscar_jogadores_por_time_api_football(id_time)

    # Preparar documentos para embeddings
    documentos = []
    metadados = []
    ids = []

    # Adicionar próximos jogos
    for i, jogo in enumerate(jogos[:5]):
        texto = f"Próximo jogo: {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']} em {jogo['fixture']['date']}"
        documentos.append(texto)
        metadados.append({"tipo": "proximo_jogo", "time": time_nome, "data": jogo['fixture']['date']})
        ids.append(f"{time_nome}_jogo_{i}")

    # Adicionar times da liga
    for i, time in enumerate(times_liga[:5]):
        texto = f"Time: {time['team']['name']} - Fundado em {time['team']['founded']}"
        documentos.append(texto)
        metadados.append({"tipo": "time_liga", "liga": id_liga, "time": time['team']['name']})
        ids.append(f"liga_{id_liga}_time_{i}")

    # Adicionar jogadores
    for i, jogador in enumerate(jogadores[:5]):
        texto = f"Jogador: {jogador['player']['name']} - Idade: {jogador['player']['age']} - Nacionalidade: {jogador['player']['nationality']}"
        documentos.append(texto)
        metadados.append({"tipo": "jogador", "time": time_nome, "jogador": jogador['player']['name']})
        ids.append(f"{time_nome}_jogador_{i}")

    # Gerar embeddings e armazenar
    embeddings = get_embedder().encode(documentos)
    get_collection().add(
        documents=documentos,
        metadatas=metadados,
        ids=ids,
        embeddings=embeddings.tolist()
    )
    print(f"Dados completos de {time_nome} armazenados no RAG usando API-Football!")

def validate_league(league_id, season=DEFAULT_SEASON):
    url = f"{API_FOOTBALL_URL}/leagues"
    headers = get_api_football_headers()
    if not headers:
        print("API_FOOTBALL_KEY não configurada. Defina a variável de ambiente API_FOOTBALL_KEY.")
        return None
    params = {"id": league_id, "season": season}

    response = rate_limited_request(url, headers=headers, params=params)
    if not response:
        print("Erro na requisição: sem resposta")
        return None
    if not response.ok:
        print(f"Erro na requisição: {response.status_code}")
        return None

    try:
        data = response.json()
    except Exception as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None

    if not data.get("response"):
        print("Erro: Resposta inválida ou vazia.")
        return None

    print("Dados da liga recebidos (exemplo):", {"results": len(data.get('response', []))})
    return data

# Exemplo de uso
if __name__ == "__main__":
    league_id = 71  # Substitua pelo ID da liga que deseja validar
    season = DEFAULT_SEASON
    validate_league(league_id, season)

    # Testar armazenamento de dados completos para todos os times da Série A do Brasileirão
    times_serie_a = buscar_times_por_liga_api_football(71, season=season)  # ID da Série A do Brasileirão

    for time in times_serie_a:
        time_nome = time['team']['name']
        id_time = time['team']['id']
        id_liga = 71  # Série A do Brasileirão

        print(f"Processando dados para o time: {time_nome}")
        armazenar_dados_completos_api_football(time_nome, id_time, id_liga)
