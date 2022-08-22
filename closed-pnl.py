import asyncio
import httpx 
import hmac
import urllib3
import time
from urllib.parse import quote_plus

#######################################
# closed-pnl の取得                   
#######################################

# 通貨ペアを指定
symbol = 'ETHUSDT'


##############################################################################
# APIのEndpoint                                                              
##############################################################################

# TestNetのAPI Endpoint
url = 'https://api-testnet.bybit.com/private/linear/trade/closed-pnl/list'

# 本番環境のAPI Endpoint
# url = 'https://api.bybit.com/private/linear/trade/closed-pnl/list'
# url = 'https://api.bytick.com/private/linear/trade/closed-pnl/list'


#####################################################################################
# APIキー                                                                                                      
#####################################################################################
api_key = ''
api_secret = ''

def auth():
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

async def main():
    client = httpx.AsyncClient(http2=True)
    url_with_params = auth()
    response = await client.get(url_with_params)
    await client.aclose()
    print(response.http_version)  # "HTTP/1.0", "HTTP/1.1", or "HTTP/2".
    print(response)
    print(response.text)

asyncio.run(main())