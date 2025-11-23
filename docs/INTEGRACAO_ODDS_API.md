# Integração com APIs de Odds Reais

Este arquivo contém instruções para integrar o bot com APIs reais de odds/cotas de apostas.

## APIs Disponíveis

### 1. The Odds API (odds-api.com)
- **Site**: https://the-odds-api.com/
- **Preço**: Gratuito para até 500 requests/mês
- **Cobertura**: Odds de múltiplas casas de apostas
- **Esportes**: Futebol, basquete, tênis, etc.

### 2. Odds Portal API
- **Site**: https://www.oddsportal.com/
- **Preço**: Varia (há versão gratuita limitada)
- **Cobertura**: Odds históricas e atuais

### 3. BetExplorer API
- **Site**: https://www.betexplorer.com/
- **Preço**: Gratuito para uso pessoal
- **Cobertura**: Odds e estatísticas detalhadas

### 4. Football Data API (com odds)
- **Site**: https://www.football-data.org/
- **Preço**: Gratuito para uso limitado
- **Cobertura**: Dados de futebol + algumas odds

## Como Integrar

### Passo 1: Obter API Key
```python
# Exemplo com The Odds API
API_KEY = "your_api_key_here"
BASE_URL = "https://api.the-odds-api.com/v4/sports"
```

### Passo 2: Modificar o método buscar_odds_jogo

```python
def buscar_odds_reais_the_odds_api(self, time1, time2):
    """Busca odds reais usando The Odds API"""
    try:
        import requests

        # Mapeia nomes dos times para IDs da API
        team_mapping = {
            'Flamengo': 'Flamengo',
            'Palmeiras': 'Palmeiras',
            # Adicione mais mapeamentos...
        }

        # Busca jogos do dia
        url = f"{BASE_URL}/soccer_brazil_campeonato/odds"
        params = {
            'apiKey': API_KEY,
            'regions': 'us',  # ou 'uk', 'eu', etc.
            'markets': 'h2h',  # head to head (vitória/empate/derrota)
            'dateFormat': 'iso',
            'oddsFormat': 'decimal'
        }

        response = requests.get(url, params=params)
        data = response.json()

        # Procura pelo jogo específico
        for game in data:
            home_team = game['home_team']
            away_team = game['away_team']

            # Verifica se é o jogo que queremos
            if (team_mapping.get(time1, time1) in home_team and
                team_mapping.get(time2, time2) in away_team):

                # Extrai odds da primeira casa de apostas
                if game['bookmakers']:
                    bookmaker = game['bookmakers'][0]
                    h2h_market = next((m for m in bookmaker['markets']
                                     if m['key'] == 'h2h'), None)

                    if h2h_market:
                        outcomes = h2h_market['outcomes']
                        return {
                            'casa': outcomes[0]['price'],  # home
                            'fora': outcomes[1]['price'],  # away
                            'empate': outcomes[2]['price'] if len(outcomes) > 2 else 3.0,  # draw
                            'fonte': bookmaker['title'],
                            'atualizado_em': datetime.now().strftime('%H:%M')
                        }

        return None

    except Exception as e:
        print(f"Erro na API de odds: {e}")
        return None
```

### Passo 3: Configuração no .env

Crie um arquivo `.env` na raiz do projeto:

```env
# Odds API Keys
THE_ODDS_API_KEY=your_key_here
ODDS_PORTAL_API_KEY=your_key_here

# Configurações
ODDS_API_PROVIDER=the_odds_api  # ou 'odds_portal', 'betexplorer'
ODDS_UPDATE_INTERVAL=300  # segundos (5 minutos)
```

### Passo 4: Cache de Odds

Para não fazer requests excessivos, implemente cache:

```python
import time
from functools import lru_cache

class OddsCache:
    def __init__(self, ttl_seconds=300):  # 5 minutos
        self.cache = {}
        self.ttl = ttl_seconds

    def get(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = (value, time.time())

# Uso
odds_cache = OddsCache()

def buscar_odds_jogo_cached(self, time1, time2):
    """Busca odds com cache"""
    cache_key = f"{time1}_vs_{time2}"

    # Verifica cache primeiro
    cached_odds = odds_cache.get(cache_key)
    if cached_odds:
        return cached_odds

    # Busca odds reais
    odds = self.buscar_odds_reais_the_odds_api(time1, time2)

    # Salva no cache se encontrou
    if odds:
        odds_cache.set(cache_key, odds)

    return odds
```

## Implementação Completa

Para implementar completamente, você precisará:

1. **Criar conta** nas APIs desejadas
2. **Obter API keys**
3. **Mapear nomes dos times** para os IDs das APIs
4. **Implementar tratamento de erros** e fallbacks
5. **Adicionar cache** para performance
6. **Configurar limites de rate** para não exceder quotas

## Fallback Inteligente

Quando não conseguir odds reais, o sistema deve:

1. Usar odds estimadas baseadas em força dos times
2. Informar que são estimativas
3. Sugerir verificar com casas de apostas

## Exemplo de Resposta com Odds Reais

```
💰 Odds para Flamengo x Palmeiras:
🏆 Vitória Flamengo: 2.15
🤝 Empate: 3.40
⚽ Vitória Palmeiras: 3.60

📊 Fonte: Bet365
🕐 Atualizado às 15:45

⚠️ Odds sujeitas a mudança. Verifique com sua casa de apostas!
```

## Considerações Legais

- **Verifique termos de uso** das APIs
- **Não use para apostas comerciais** sem licença
- **Inclua disclaimer** sobre riscos das apostas
- **Respeite leis de jogos de azar** do seu país

---

Para implementar qualquer dessas APIs, me diga qual prefere e posso ajudar com o código específico!