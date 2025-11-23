from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from supabase import create_client, Client
import json
from datetime import datetime

app = FastAPI(title="TradeComigo API", description="API para consultar dados do Brasileirão")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Config Supabase
SUPABASE_URL = "https://nflmvptqgicabovfmnos.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class ChatRequest(BaseModel):
    prompt: str
    chat_history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    reply: str

def consultar_jogos(time_nome: Optional[str] = None, status: Optional[str] = None, limit: int = 10):
    """Consulta jogos com filtros"""
    query = supabase.table('jogos').select('*')

    if status:
        query = query.eq('status', status)

    if time_nome:
        # Buscar no raw_payload por nome do time
        # Como não temos busca avançada, vamos buscar todos e filtrar
        pass

    query = query.order('start_time', desc=True).limit(limit)
    result = query.execute()
    return result.data

def consultar_classificacao():
    """Consulta a classificação atual"""
    result = supabase.table('classificacao').select('*').order('position').execute()
    return result.data

def consultar_artilheiros(limit: int = 10):
    """Consulta os artilheiros da temporada"""
    result = supabase.table('jogadores').select('name,season_goals,season_assists').order('season_goals', desc=True).limit(limit).execute()
    return result.data

def buscar_jogo_por_times(time1: str, time2: str):
    """Busca jogos entre dois times específicos"""
    all_games = supabase.table('jogos').select('*').execute()

    jogos_encontrados = []
    for game in all_games.data:
        if game.get('raw_payload') and isinstance(game['raw_payload'], dict):
            payload = game['raw_payload']
            home_team = payload.get('homeTeam', {}).get('name', '').lower()
            away_team = payload.get('awayTeam', {}).get('name', '').lower()

            # Verificar se os times estão no jogo
            time1_lower = time1.lower()
            time2_lower = time2.lower()

            has_time1 = any(term in home_team or term in away_team for term in [time1_lower, time1_lower.replace(' ', '')])
            has_time2 = any(term in home_team or term in away_team for term in [time2_lower, time2_lower.replace(' ', '')])

            if has_time1 and has_time2:
                jogos_encontrados.append(game)

    # Ordenar por data (mais recente primeiro)
    jogos_encontrados.sort(key=lambda x: x['start_time'], reverse=True)
    return jogos_encontrados

def processar_pergunta(prompt: str) -> str:
    """Processa a pergunta do usuário e retorna resposta baseada nos dados"""

    prompt_lower = prompt.lower()

    try:
        # Jogos recentes
        if any(word in prompt_lower for word in ['jogos recentes', 'últimos jogos', 'jogos']):
            jogos = consultar_jogos(limit=5)
            if jogos:
                resposta = "🏆 Últimos jogos do Brasileirão:\n\n"
                for jogo in jogos:
                    if jogo.get('raw_payload') and isinstance(jogo['raw_payload'], dict):
                        payload = jogo['raw_payload']
                        home_team = payload.get('homeTeam', {}).get('name', 'N/A')
                        away_team = payload.get('awayTeam', {}).get('name', 'N/A')
                        home_score = jogo.get('home_team_score', 'N/A')
                        away_score = jogo.get('away_team_score', 'N/A')
                        data = jogo['start_time'][:10]
                        status = jogo['status']

                        resposta += f"📅 {data}: {home_team} {home_score} x {away_score} {away_team} ({status})\n"
                    else:
                        resposta += f"📅 {jogo['start_time'][:10]}: ID {jogo['api_id']} ({jogo['status']})\n"
                return resposta
            else:
                return "❌ Nenhum jogo encontrado."

        # Classificação
        elif any(word in prompt_lower for word in ['classificação', 'tabela', 'ranking']):
            classificacao = consultar_classificacao()
            if classificacao:
                resposta = "🏆 Classificação do Brasileirão:\n\n"
                for time in classificacao:
                    resposta += f"{time['position']}º {time['team_name']} - {time['points']} pts ({time['won']}V {time['draw']}E {time['lost']}D)\n"
                return resposta
            else:
                return "❌ Classificação não encontrada."

        # Artilheiros
        elif any(word in prompt_lower for word in ['artilheiros', 'goleadores', 'gols']):
            artilheiros = consultar_artilheiros(limit=10)
            if artilheiros:
                resposta = "⚽ Artilheiros do Brasileirão:\n\n"
                for jogador in artilheiros:
                    if jogador.get('season_goals', 0) > 0:
                        resposta += f"{jogador['name']}: {jogador['season_goals']} gols"
                        if jogador.get('season_assists', 0) > 0:
                            resposta += f", {jogador['season_assists']} assistências"
                        resposta += "\n"
                return resposta
            else:
                return "❌ Dados de artilheiros não encontrados."

        # Jogos entre times específicos
        elif any(word in prompt_lower for word in ['flamengo', 'fluminense', 'fla', 'flu', 'clássico']):
            # Detectar times mencionados
            times_mencionados = []
            if 'flamengo' in prompt_lower or 'fla' in prompt_lower or 'mengo' in prompt_lower:
                times_mencionados.append('flamengo')
            if 'fluminense' in prompt_lower or 'flu' in prompt_lower or 'xente' in prompt_lower:
                times_mencionados.append('fluminense')

            if len(times_mencionados) >= 2:
                jogos = buscar_jogo_por_times(times_mencionados[0], times_mencionados[1])
                if jogos:
                    resposta = f"🏆 Jogos entre {times_mencionados[0].title()} e {times_mencionados[1].title()}:\n\n"
                    for jogo in jogos[:5]:  # Últimos 5
                        payload = jogo['raw_payload']
                        home_team = payload.get('homeTeam', {}).get('name', 'N/A')
                        away_team = payload.get('awayTeam', {}).get('name', 'N/A')
                        home_score = jogo.get('home_team_score', 'N/A')
                        away_score = jogo.get('away_team_score', 'N/A')
                        data = jogo['start_time'][:10]

                        resposta += f"📅 {data}: {home_team} {home_score} x {away_score} {away_team}\n"

                        # Verificar estatísticas
                        game_id = jogo['api_id']
                        stats_result = supabase.table('estatisticas_jogador').select('*').eq('jogo_api_id', game_id).execute()
                        if stats_result.data:
                            resposta += f"   📊 {len(stats_result.data)} estatísticas de jogadores disponíveis\n"

                        events_result = supabase.table('eventos_jogo').select('*').eq('jogo_api_id', game_id).execute()
                        if events_result.data:
                            resposta += f"   ⚽ {len(events_result.data)} eventos registrados\n"

                    return resposta
                else:
                    return f"❌ Nenhum jogo encontrado entre {times_mencionados[0].title()} e {times_mencionados[1].title()}."
            else:
                return "🤔 Mencione dois times para buscar jogos entre eles."

        # Estatísticas gerais
        elif any(word in prompt_lower for word in ['estatísticas', 'stats', 'dados']):
            total_jogos = len(supabase.table('jogos').select('api_id').execute().data)
            total_jogadores = len(supabase.table('jogadores').select('api_id').execute().data)
            total_stats = len(supabase.table('estatisticas_jogador').select('id').execute().data)

            resposta = f"📊 Estatísticas do sistema:\n\n"
            resposta += f"🏆 Total de jogos: {total_jogos}\n"
            resposta += f"👥 Total de jogadores: {total_jogadores}\n"
            resposta += f"📈 Total de estatísticas: {total_stats}\n"
            return resposta

        # Comando ajuda
        elif any(word in prompt_lower for word in ['ajuda', 'help', 'comandos']):
            resposta = "🤖 Comandos disponíveis:\n\n"
            resposta += "• 'jogos recentes' - Mostra últimos jogos\n"
            resposta += "• 'classificação' - Mostra tabela do campeonato\n"
            resposta += "• 'artilheiros' - Mostra goleadores\n"
            resposta += "• 'fla x flu' ou 'flamengo fluminense' - Jogos entre times\n"
            resposta += "• 'estatísticas' - Resumo dos dados\n"
            resposta += "• 'ajuda' - Este menu\n\n"
            resposta += "💡 Você pode perguntar sobre qualquer time ou combinação!"
            return resposta

        # Resposta padrão
        else:
            return "🤔 Não entendi sua pergunta. Digite 'ajuda' para ver os comandos disponíveis!"

    except Exception as e:
        return f"❌ Erro ao processar pergunta: {str(e)}"

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Endpoint principal do chat"""
    try:
        resposta = processar_pergunta(request.prompt)
        return ChatResponse(reply=resposta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/")
async def root():
    return {"message": "TradeComigo API - Online", "status": "OK"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando TradeComigo API...")
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        import traceback
        traceback.print_exc()