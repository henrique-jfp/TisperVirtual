import asyncio
from api_server import api_chat, ChatRequest

async def run():
    req = ChatRequest(prompt='Qual o placar do jogo entre Flamengo e Vasco?', chat_history=[])
    res = await api_chat(req)
    print('RESPONSE:', res)

if __name__ == '__main__':
    asyncio.run(run())
