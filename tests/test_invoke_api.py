import asyncio
from api_server import api_chat
from api_server import ChatRequest

async def run_test():
    req = ChatRequest(prompt="Teste direto sem uvicorn", chat_history=[])
    try:
        resp = await api_chat(req)
        print('RESPONSE:', resp)
    except Exception as e:
        print('ERROR', e)

if __name__ == '__main__':
    asyncio.run(run_test())
