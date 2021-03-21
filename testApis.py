import requests
import json
BASE_URL = 'https://api.binance.com'
payload = {
    'symbol' : 'BTCUSDC',
    'interval' : '5m',
    'limit' : 1

}
resp = requests.get(BASE_URL + '/api/v3/klines', params=payload)
tulostus = resp.headers
print(tulostus)
