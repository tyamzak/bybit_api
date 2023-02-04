import tradingeconomics as te
import json
    
te.login('A7CBF484D68B42B:4D7B65B6A3B8439')

events = ["Date", "Country", "Category", "Event", "Reference", "Source", "Actual", "Previous", "Forecast", "TEForecast", "URL", "DateSpan", "Importance", "LastUpdate", "Revised", "Ticker", "Symbol", "CalendarID"] 

def on_message(ws, message):
    """
    この関数は、WebSocketから受け取ったメッセージに対する処理を行います。

    WebSocketから受け取ったメッセージをJSON形式で解析する。
    解析結果のトピックに応じて、接続確認かイベントかを判別する。
    トピックが接続確認の場合は、トピック名を出力する。
    トピックがイベントの場合は、eventsリストに定義された各イベント要素に対して、該当する要素の値を出力する。

    Args:
        ws (_type_): _description_
        message (_type_): _description_
    """

    print('****************')
    js = json.loads(message)

    if js.get("topic"):
        print('接続確認です')
        print(f'topic : {js.get("topic")}')

    if js.get(events[0]):
        print('イベントが届きました')
        for  event in events:
            description = js.get(event)
            print(f'{event} : {description}')

te.subscribe('calendar')
te.run(on_message)