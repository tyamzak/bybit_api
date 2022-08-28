from distutils.log import info
from re import A, I
import time
import ccxt
import datetime
from datetime import datetime
import csv
import json
import requests
import hmac
import base64
import asyncio
from re import A
import httpx 
import urllib3
from urllib.parse import quote_plus


now = datetime.now()
timestamp=requests.get("https://api.bitget.com/api/spot/v1/public/time").json()["data"]

StartTime=str(int(datetime(2022, 8, 20, 00, 00, 00, 000000).timestamp())*1000)
EndTime=timestamp

print(now.day)
print(now.month)

binance_LIST = []
OKEX_LIST = []
Bitget_LIST = []
Sub_bitget_LIST = []
Bybit_LIST = []


#Bybit
Bybit = ccxt.bybit(
   {
       "apiKey": "",
       "secret": "",
       "enableRateLimit": True,
       "options": {"defaultType": "swap"},
       "enableRateLimit": True,
   }
)


Bybit_C = Bybit.fetch_markets() 
for i in range(len(Bybit_C)):
    if Bybit_C[i]['settleId'] == 'USDT':
        Bybit_LIST.append(Bybit_C[i]['id'])
        time.sleep(0.1)

print(Bybit_LIST)

url = 'https://api.bytick.com/private/linear/trade/closed-pnl/list'
api_key = ''
api_secret = ''
waittime = 0.1

def auth(symbol:str):
    """_summary_
        パラメータ設定及びsignを作成し、リクエスト用の文字列を返す
    Returns:
        str : リクエスト用の文字列
    """
    timestamp = int(time.time() * 10 ** 3)
    headers = {}
    params = {
        'symbol': symbol,
        'api_key': api_key,
        'timestamp': str(timestamp),
        'recv_window': '5000'
    }

    #signの作成
    param_str = ''
    for key in sorted(params.keys()):
        v = params[key]
        if isinstance(params[key], bool):
            if params[key]:
                v = "true"
            else:
                v = "false"
        param_str += key + "=" + v + "&"
    param_str = param_str[:-1]
    signature = str(hmac.new(
        bytes(api_secret, "utf-8"),
        bytes(param_str, "utf-8"), digestmod="sha256"
    ).hexdigest())
    sign_real = {
        "sign": signature
    }
    param_str = quote_plus(param_str, safe="=&")
    full_param_str = f"{param_str}&sign={sign_real['sign']}"
    urllib3.disable_warnings()
    return f"{url}?{full_param_str}"


async def bybit_API_request(symbol):
    time.sleep(waittime)
    client = httpx.AsyncClient(http2=True)
    url_with_params = auth(symbol)
    response = await client.get(url_with_params)
    await client.aclose()
    print('API Request  ' + symbol + ' : ' + response.reason_phrase)  
    return response

reslist = []
for symbol in Bybit_LIST:

    reslist.append({symbol : asyncio.run(bybit_API_request(symbol))})

for i, symbol in enumerate(Bybit_LIST):
    tradelist = json.loads(reslist[i][symbol].content)

    if tradelist['result']['data'] is None:
        print(f'{symbol} has no trade data')
        continue

    for trade in tradelist['result']['data']:
        tradeside = trade['side']

        # Sellの時のトレード収支
        if tradeside == 'Sell':

            closed_value =  trade['cum_exit_value'] - trade['cum_entry_value']
            printstr = f'Symbol:{symbol} Side:{tradeside} ClosedValue:{closed_value}'

            print(printstr)