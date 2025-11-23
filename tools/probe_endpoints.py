import requests

h={'User-Agent':'Mozilla/5.0','Accept':'application/json, text/plain, */*','Referer':'https://www.365scores.com/'}
base='https://webws.365scores.com'
ids=[4467481]
endpoints=[f'/web/game/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&gameId={ids[0]}',
           f'/web/game/lineups/?games={ids[0]}',
           f'/web/game/lineups/?gameId={ids[0]}',
           f'/web/game/stats/?games={ids[0]}&includePlayers=1&includePlayerStats=1',
           f'/web/game/stats/?games={ids[0]}']
for e in endpoints:
    url=base+e
    try:
        r=requests.get(url,headers=h,timeout=10)
        print(url,'->',r.status_code)
        txt=r.text
        found=False
        for token in ('players','playersStats','lineups'):
            if token in txt:
                print(' contains',token)
                found=True
        if not found:
            print(' no players/lineups tokens')
    except Exception as ex:
        print('ERR',url,ex)
