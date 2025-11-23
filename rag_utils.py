import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from personas import PERSONA_CRIA_DO_GREEN
import sqlite3
import re

load_dotenv()

# embedder = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedder():
    return SentenceTransformer('all-MiniLM-L6-v2')


# Try to import the shared RAG client wrapper. If it's missing, provide a
# clear runtime error when get_collection() is called.
try:
    from rag_client import get_collection
except Exception:
    def get_collection():
        raise RuntimeError(
            "RAG client not initialized. Configure RAG_PROVIDER and install a supported provider (see .env.example)."
        )


def consultar_sqlite_para_partida(query):
    """Consulta o banco SQLite para dados de partida se a query parecer pedir placar ou dados específicos."""
    # Detectar se é pergunta sobre placar/partida
    if not re.search(r'(placar|partida|resultado|quanto foi|score)', query.lower()):
        return None
    
    # Extrair times da query
    times = re.findall(r'\b([A-Za-zÀ-ú ]+)\b', query)
    times = [t.strip() for t in times if len(t) > 2 and t.lower() not in ['foi', 'entre', 'partida', 'placar', 'resultado', 'quanto', 'foi', 'o', 'a', 'e', 'de', 'do', 'da', 'em', 'com']]
    if len(times) < 2:
        return None
    
    time1, time2 = times[0], times[1]
    
    # Consultar banco
    conn = sqlite3.connect('dados/sports_data.db')
    c = conn.cursor()
    c.execute('''
        SELECT time_casa, time_fora, placar_casa, placar_fora, data_hora 
        FROM partidas 
        WHERE (time_casa LIKE ? AND time_fora LIKE ?) OR (time_casa LIKE ? AND time_fora LIKE ?)
    ''', (f'%{time1}%', f'%{time2}%', f'%{time2}%', f'%{time1}%'))
    result = c.fetchone()
    conn.close()
    
    if result:
        time_casa, time_fora, placar_casa, placar_fora, data = result
        return f"Placar: {time_casa} {placar_casa}-{placar_fora} {time_fora} (Data: {data or 'N/A'})"
    return None
def consultar_rag(query, categoria=None, n_results=3):
    """Consulta o RAG para a query e retorna contexto como string."""
    query_embedding = get_embedder().encode([query])
    where_clause = {"categoria": categoria} if categoria else None
    results = get_collection().query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results,
        where=where_clause
    )
    # Retorna texto concatenado dos documentos
    if results and results.get('documents'):
        # documents is list of lists per query; take first result
        docs = results['documents'][0]
        return "\n\n".join(docs)
    return ""


def consultar_rag_snippets(query, n_results=3):
    """Retorna os top-N snippets (documentos) do RAG para a query como lista."""
    query_embedding = get_embedder().encode([query])
    results = get_collection().query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results
    )
    if results and results.get('documents'):
        docs = results['documents'][0]
        return docs
    return []


def build_chat_messages(time_casa, time_fora, contexto_rag, use_persona=True):
    """Constroi a lista de mensagens para o chat (inclui system prompt opcional)."""
    prompt_user = (
        f"Você é um Tipster de Futebol profissional. Use o contexto fornecido para gerar uma dica de aposta precisa.\n\n"
        f"Contexto histórico:\n{contexto_rag}\n\n"
        f"Jogo atual: {time_casa} vs {time_fora}\n\n"
        f"Gere uma dica de aposta (ex: Vitória mandante, Over 2.5, Ambos Marcam) com justificativa baseada em dados."
    )

    messages = []
    if use_persona:
        messages.append({"role": "system", "content": PERSONA_CRIA_DO_GREEN})
    messages.append({"role": "user", "content": prompt_user})
    return messages


def gerar_dica_com_rag(time_casa, time_fora, contexto_rag, llm_client, model="local-model"):
    """Gera dica usando RAG + LLM. Insere persona como `system` se habilitada via `.env`."""
    use_persona_env = os.environ.get("USE_CRIA_DO_GREEN", "true").lower()
    use_persona = use_persona_env in ("1", "true", "yes", "on")

    messages = build_chat_messages(time_casa, time_fora, contexto_rag, use_persona=use_persona)

    try:
        response = llm_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na IA: {e}"


def gerar_resposta_chat(user_message, contexto_rag, llm_client, chat_history=None, temperature=0.15, max_tokens=600, model="local-model"):
    """Gera uma resposta livre para o chat conversacional usando RAG + persona.

    - `chat_history` deve ser uma lista de tuplas (user_msg, assistant_msg) na ordem em que ocorreram.
    """
    use_persona_env = os.environ.get("USE_CRIA_DO_GREEN", "true").lower()
    use_persona = use_persona_env in ("1", "true", "yes", "on")

    messages = []
    # system persona
    if use_persona:
        messages.append({"role": "system", "content": PERSONA_CRIA_DO_GREEN})

    # If there is prior conversation, add an extra system instruction to avoid re-greeting
    if chat_history and len(chat_history) > 0:
        messages.append({
            "role": "system",
            "content": "Esta é uma conversa contínua. NÃO repita a saudação inicial em respostas subsequentes; seja direto e não repita já dito."
        })

    # Add previous turns to messages so the model knows the context and won't repeat itself
    if chat_history:
        for user_turn, assistant_turn in chat_history:
            messages.append({"role": "user", "content": user_turn})
            # include assistant replies as well so model sees what it answered
            messages.append({"role": "assistant", "content": assistant_turn})

    # Consultar SQLite para dados específicos de partida
    sqlite_data = consultar_sqlite_para_partida(user_message)
    if sqlite_data:
        messages.append({
            "role": "system",
            "content": f"Dados da partida coletados: {sqlite_data}. Use estes dados para responder à pergunta."
        })

    # Add RAG context as a concise system message (advise model to use it only if relevant)
    contexto_brief = contexto_rag
    if isinstance(contexto_rag, (list, tuple)):
        contexto_brief = "\n".join(contexto_rag[:5])
    if contexto_brief:
        # Keep context length reasonable
        messages.append({
            "role": "system",
            "content": f"Contexto recuperado (use somente fatos relevantes; sumarize se necessário):\n{contexto_brief[:3000]}"
        })

    # Build top-3 factual snippets from RAG (prefer structured facts)
    snippets = []
    try:
        snippets = consultar_rag_snippets(user_message, n_results=3)
    except Exception:
        # fallback to provided contexto_rag if query fails
        if isinstance(contexto_rag, (list, tuple)):
            snippets = contexto_rag[:3]
        elif isinstance(contexto_rag, str):
            snippets = [contexto_rag]

    contexto_brief = "\n".join(snippets) if snippets else (contexto_rag if isinstance(contexto_rag, str) else "")
    if contexto_brief:
        messages.append({
            "role": "system",
            "content": (
                "Contexto recuperado (use somente fatos relevantes abaixo para justificar a dica):\n"
                + contexto_brief[:3000]
            )
        })

    # Add few-shot examples to demonstrate desired output format
    examples = [
        {
            "user": "Dá uma dica pro próximo jogo do Flamengo",
            "assistant": (
                "Saudação: Fala tu!\n"
                "Análise: O Flamengo tem ataque em boa fase (3 vitórias nos últimos 4), defesa vulnerável fora de casa.\n"
                "Sugestão de aposta: Vitória do Flamengo — aposta simples (odds não fornecidas).\n"
                "Gestão de banca: Vai com calma, 1-2% da banca."
            )
        },
        {
            "user": "Me dá uma dica pro clássico Botafogo x Vasco",
            "assistant": (
                "Saudação: Qual foi!\n"
                "Análise: Jogo tende a poucas chances; ambos os times com média baixa de gols nas últimas 5.\n"
                "Sugestão de aposta: Under 2.5 gols — justificativa pela forma recente das defesas. (odds não fornecidas)\n"
                "Gestão de banca: Sem emocionar, stake conservador."
            )
        }
    ]
    # Inject examples as user+assistant turns
    for ex in examples:
        messages.append({"role": "user", "content": ex['user']})
        messages.append({"role": "assistant", "content": ex['assistant']})

    # Also add a strict format instruction to avoid ambiguity
    messages.append({
        "role": "system",
        "content": (
            "OBRIGATÓRIO: Responda em 4 partes separadas por quebras de linha:\n"
            "1) Saudação curta (apenas na primeira resposta da conversa).\n"
            "2) Análise/justificativa com até 3 fatos (use os fatos do contexto).\n"
            "3) Sugestão de aposta clara em UMA LINHA (ex: 'Aposta: Vitória Flu @1.90').\n"
            "4) Aviso de gestão de banca curto (ex: 'Vai com calma, 1-2% da banca').\n"
              "NÃO invente números ou odds numéricas. Se as odds numéricas não estiverem explicitamente no contexto (odds ao vivo injetadas), escreva 'odds não disponíveis'. Se não houver dados suficientes para justificar a aposta, diga 'Dados insuficientes, aposta conservadora sugerida'."
        )
    })

    # If user asked about odds/market, try to fetch live odds and inject as facts
    try:
        from odds_fetcher import get_live_odds_for_match
        # simple parsing for 'TeamA x TeamB' patterns
        import re
        m = re.search(r"([A-Za-zÀ-ú0-9 ]+)\s+[xXvV]|vs\s+([A-Za-zÀ-ú0-9 ]+)", user_message)
    except Exception:
        m = None

    # better parsing: look for 'TeamA x TeamB' or 'TeamA vs TeamB' or 'TeamA v TeamB'
    if ' vs ' in user_message.lower() or ' x ' in user_message.lower() or ' v ' in user_message.lower():
        # try multiple separators
        sep_found = None
        for sep in [' vs ', ' x ', ' v ', ' X ', ' VS ', ' V ', ' x ', ' vs ']:
            if sep in user_message:
                sep_found = sep
                break
        if sep_found:
            parts = user_message.split(sep_found)
            if len(parts) >= 2:
                team_a = parts[0].strip()
                team_b = parts[1].split()[0].strip()
                try:
                    odds_data = get_live_odds_for_match(team_a, team_b)
                    if odds_data and odds_data.get('bookmakers'):
                        # build a short bullet list of top bookmakers and sample prices if available
                        bullets = []
                        for bm in odds_data.get('bookmakers')[:3]:
                            # Try to extract key info; structure can vary
                            name = bm.get('bookmaker', {}).get('name') if isinstance(bm.get('bookmaker'), dict) else bm.get('bookmaker')
                            bullets.append(f"- {name}")
                        messages.append({"role": "system", "content": f"Odds ao vivo (Fonte: API-Football) para {team_a} x {team_b}:\n" + "\n".join(bullets)})
                except Exception:
                    pass

                # Also fetch recent detailed matches for both teams and inject as structured facts
                try:
                    from data_collector import get_recent_matches_detailed
                    form_a = get_recent_matches_detailed(team_a, limit=5)
                    form_b = get_recent_matches_detailed(team_b, limit=5)

                    def format_table(team, rows):
                        if not rows:
                            return f"Sem dados recentes para {team}."
                        lines = [f"Time: {team}", "Date | Venue | Opponent | Score | GF | GA | YC | RC | Corners"]
                        for r in rows:
                            lines.append(f"{r.get('date','N/A')} | {r.get('venue')} | {r.get('opponent')} | {r.get('score')} | {r.get('goals_for')} | {r.get('goals_against')} | {r.get('yellow_cards')} | {r.get('red_cards')} | {r.get('corners')}")
                        return "\n".join(lines)

                    table_a = format_table(team_a, form_a)
                    table_b = format_table(team_b, form_b)
                    messages.append({
                        "role": "system",
                        "content": (
                            "DADOS FACTUAIS DOS ÚLTIMOS JOGOS (use apenas estes fatos para análise):\n\n"
                            + table_a + "\n\n" + table_b
                        )
                    })
                    # Force the model to prefer these facts
                    messages.append({
                        "role": "system",
                        "content": (
                            "INSTRUÇÃO RÍGIDA: USE APENAS os fatos listados acima ao fazer a análise. Se houver conflito entre sua memória e estes fatos, prefira estes fatos. NÃO invente resultados, cartões ou corners que não estejam listados."
                        )
                    })
                except Exception:
                    pass

    # Final user message
    prompt_user = f"{user_message}"
    messages.append({"role": "user", "content": prompt_user})

    try:
        response = llm_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na IA: {e}"


def gerar_resposta_simples(user_message, llm_client, temperature=0.0, max_tokens=150, model="local-model"):
    """Gera resposta curta e direta com mensagens mínimas — usada para prompts simples e baixa latência.

    - Não injeta exemplos longos nem múltiplas instruções de system.
    - Uso: quando prompt for direto, p.ex. "Quem ganhou o jogo X?" ou "Dê uma dica rápida".
    """
    messages = []
    # breve system prompt que define papel sem verbose examples
    persona = os.environ.get("USE_CRIA_DO_GREEN", "true").lower() in ("1", "true", "yes", "on")
    if persona:
        from personas import PERSONA_CRIA_DO_GREEN
        messages.append({"role": "system", "content": PERSONA_CRIA_DO_GREEN})
    # user message
    messages.append({"role": "user", "content": user_message})

    try:
        response = llm_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na IA: {e}"
