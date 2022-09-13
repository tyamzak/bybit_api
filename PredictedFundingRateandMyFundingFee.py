import ccxt
import time

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


Bybit_C = Bybit.fetch_markets() #全通貨シンボルの取得　+ リスト化
for i in range(len(Bybit_C)):
    if Bybit_C[i]['settleId'] == 'USDT':
        Bybit_LIST.append(Bybit_C[i]['id'])
        time.sleep(0.1)

##############################以下、追加コード######################################


#値の引継ぎ
symbols = Bybit_LIST

import asyncio
import httpx 
import hmac
import urllib3
import time
from urllib.parse import quote_plus
import json



##############################################################################
# APIのEndpoint                                                              
##############################################################################

# TestNetのAPI Endpoint
# url = 'https://api-testnet.bybit.com/private/linear/funding/predicted-funding'

# # 本番環境のAPI Endpoint
url = ''
# url = 



#####################################################################################
# TESTNET APIキー                                                                                                      
#####################################################################################
# api_key = ''
# api_secret = ''
#####################################################################################
# 本番APIキー
#####################################################################################
api_key = ""
api_secret = ""
#####################################################################################

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

waittime = 0.2

async def main(symbol):
    time.sleep(waittime)
    client = httpx.AsyncClient(http2=True)
    url_with_params = auth(symbol)
    response = await client.get(url_with_params)
    await client.aclose()
    if   json.loads(response.text)["ret_msg"] == 'OK':
        print('API Request  ' + symbol + ' : ' + str(json.loads(response.text)["result"]))
    else:
        print('API Request  ' + symbol + ' : ' + json.loads(response.text)["ret_msg"])

# テスト用データセット
# symbols = ['BTCUSDT', 'ETHUSDT', 'EOSUSDT', 'XRPUSDT', 'BCHUSDT', 'LTCUSDT', 'XTZUSDT', 'LINKUSDT', 'ADAUSDT', 'DOTUSDT', 'UNIUSDT', 'XEMUSDT', 'SUSHIUSDT', 'AAVEUSDT', 'DOGEUSDT', 'MATICUSDT', 'ETCUSDT', 'BNBUSDT', 'FILUSDT', 'SOLUSDT', 'XLMUSDT', 'TRXUSDT', 'VETUSDT', 'THETAUSDT', 'COMPUSDT', 'AXSUSDT', 'SANDUSDT', 'MANAUSDT', 'KSMUSDT', 'ATOMUSDT', 'AVAXUSDT', 'CHZUSDT', 'CRVUSDT', 'ENJUSDT', 'GRTUSDT', 'SHIB1000USDT', 'YFIUSDT', 'BSVUSDT', 'ICPUSDT', 'FTMUSDT', 'ALGOUSDT', 'DYDXUSDT', 'NEARUSDT', 'SRMUSDT', 'OMGUSDT', 'IOSTUSDT', 'DASHUSDT', 'FTTUSDT', 'BITUSDT', 'GALAUSDT', 'CELRUSDT', 'HBARUSDT', 'ONEUSDT', 'C98USDT', 'AGLDUSDT', 'MKRUSDT', 'COTIUSDT', 'ALICEUSDT', 'EGLDUSDT', 'RENUSDT', 'TLMUSDT', 'RUNEUSDT', 'ILVUSDT', 'FLOWUSDT', 'WOOUSDT', 'LRCUSDT', 'ENSUSDT', 'IOTXUSDT', 'CHRUSDT', 'BATUSDT', 'STORJUSDT', 'SNXUSDT', 'SLPUSDT', 'ANKRUSDT', 'LPTUSDT', 'QTUMUSDT', 'CROUSDT', 'SXPUSDT', 'YGGUSDT', 'ZECUSDT', 'IMXUSDT', 'SFPUSDT', 'AUDIOUSDT', 'ZENUSDT', 'SKLUSDT', 'GTCUSDT', 'LITUSDT', 'CVCUSDT', 'RNDRUSDT', 'SCUSDT', 'RSRUSDT', 'STXUSDT', 'MASKUSDT', 'CTKUSDT', 'BICOUSDT', 'REQUSDT', '1INCHUSDT', 'KLAYUSDT', 'SPELLUSDT', 'ANTUSDT', 'DUSKUSDT', 'ARUSDT', 'REEFUSDT', 'XMRUSDT', 'PEOPLEUSDT', 'IOTAUSDT', 'ICXUSDT', 'CELOUSDT', 'WAVESUSDT', 'RVNUSDT', 'KNCUSDT', 'KAVAUSDT', 'ROSEUSDT', 'DENTUSDT', 'CREAMUSDT', 'LOOKSUSDT', 'JASMYUSDT', '10000NFTUSDT', 'HNTUSDT', 'ZILUSDT', 'NEOUSDT', 'XNOUSDT', 'RAYUSDT', 'CKBUSDT', 'SUNUSDT', 'JSTUSDT', 'BANDUSDT', 'RSS3USDT', 'OCEANUSDT', '1000BTTUSDT', 'API3USDT', 'PAXGUSDT', 'KDAUSDT', 'APEUSDT', 'GMTUSDT', 'OGNUSDT', 'BSWUSDT', 'CTSIUSDT', 'HOTUSDT', 'ARPAUSDT', 'ALPHAUSDT', 'STMXUSDT', 'DGBUSDT', 'ZRXUSDT', 'GLMRUSDT', 'SCRTUSDT', 'BAKEUSDT', 'LINAUSDT', 'ASTRUSDT', 'FXSUSDT', 'MINAUSDT', 'BNXUSDT', 'BOBAUSDT', '1000XECUSDT', 'ACHUSDT', 'BALUSDT', 'MTLUSDT', 'CVXUSDT', 'DODOUSDT', 'TOMOUSDT', 'XCNUSDT', 'DARUSDT', 'FLMUSDT', 'GALUSDT', 'FITFIUSDT', 'CTCUSDT', 'AKROUSDT', 'UNFIUSDT', 'LUNA2USDT', 'OPUSDT', 'ONTUSDT', 'BLZUSDT', 'TRBUSDT', 'BELUSDT', 'USDCUSDT', 'CEEKUSDT', 'LDOUSDT', 'INJUSDT', 'STGUSDT', '1000LUNCUSDT']

for symbol in symbols:
    if symbol == 'OMGUSDT':
        print('API Request  ' + symbol + ' was skipped since it causes errors')  
        continue
    asyncio.run(main(symbol))

print('finished')