import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup

URL = 'https://www.365scores.com/soccer/brazil/brazil-serie-a/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

r = requests.get(URL, headers=HEADERS, timeout=(5,15))
print('status', r.status_code)
if r.status_code == 200:
    html = r.text
    # procura gameId na página
    ids = set(re.findall(r'game\?\/?\?gameId=(\d+)', html))
    ids2 = set(re.findall(r'game\?gameId=(\d+)', html))
    ids3 = set(re.findall(r'match/(\d+)', html))
    ids_all = ids | ids2 | ids3
    print('found ids:', list(ids_all)[:30])
    # também tenta extrair links
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'game' in href or 'match' in href:
            links.add(href)
    print('sample links:', list(links)[:20])
else:
    print('failed to fetch')
