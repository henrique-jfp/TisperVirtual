import os
import re
import json
import requests
from datetime import datetime

# Load .env-like file
env_path = os.path.join(os.path.dirname(__file__), '.env')
LLM_API_KEY = None
LLM_BASE = 'https://api.groq.com/openai/v1'
MODEL = 'llama-2-7b'

if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'([^=]+)=(.*)', line)
            if not m:
                continue
            k = m.group(1).strip()
            v = m.group(2).strip().strip('"')
            if k == 'LLM_API_KEY':
                LLM_API_KEY = v
            if k == 'LLM_BASE':
                LLM_BASE = v
            if k == 'LLM_MODEL':
                MODEL = v

if not LLM_API_KEY:
    print('No LLM_API_KEY found in .env')
    raise SystemExit(1)

url = LLM_BASE.rstrip('/') + '/chat/completions'
headers = {
    'Authorization': f'Bearer {LLM_API_KEY}',
    'Content-Type': 'application/json'
}

data = {
    'model': MODEL,
    'messages': [
        {'role': 'user', 'content': 'Olá, Groq! Teste de conexão.'}
    ]
}

log_path = os.path.join(os.path.dirname(__file__), 'call_groq.log')
try:
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    out = {
        'timestamp': datetime.utcnow().isoformat(),
        'url': url,
        'status_code': resp.status_code,
        'headers': dict(resp.headers),
        'body': None
    }
    try:
        out['body'] = resp.json()
    except Exception:
        out['body'] = resp.text
    print('STATUS', resp.status_code)
    print(out['body'])
    with open(log_path, 'a', encoding='utf-8') as lf:
        lf.write(json.dumps(out, ensure_ascii=False, indent=2))
        lf.write('\n---\n')
except Exception as e:
    err = {'timestamp': datetime.utcnow().isoformat(), 'error': repr(e)}
    print('ERROR', err)
    with open(log_path, 'a', encoding='utf-8') as lf:
        lf.write(json.dumps(err, ensure_ascii=False) + '\n')
    raise
