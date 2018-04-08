#「ヤフーファイナンス」から
# コマンドライン引数で＜証券コード＞に対応した企業の株価を取り出すスクリプト
import requests
from bs4 import BeautifulSoup
import sys
#ヤフーファイナンスから指定した証券コードに対応した[企業名、株価]を取得する
def get_stockprice(code):
    #URLが"https://stocks.finance.yahoo.co.jp/stocks/detail/?code=証券コード.T"を
    #前提とした場合
    base_url = "http://stocks.finance.yahoo.co.jp/stocks/detail/"
    query = {}
    #code(証券コード)と末尾のT(東証)
    query["code"] = code + ".T"

    ret = requests.get(base_url,params=query)
    soup = BeautifulSoup(ret.content,"lxml")
    stocktable =  soup.find('table', {'class':'stocksTable'})
    try:                    #例外が発生したらexceptに飛ぶ
        #企業名を取得
        symbol =  stocktable.findAll('th', {'class':'symbol'})[0].text
        #株価を取得
        stockprice = stocktable.findAll('td', {'class':'stoksPrice'})[1].text
    except AttributeError:  #証券コードに対応した企業が見つからなかった場合に発生する例外
        symbol = r""
        stockprice = -1
    #企業名、株価を返す
    return symbol,stockprice

#メインルーチン
if __name__ == "__main__":
    argsys = sys.argv
    argc = len(argsys)

    #コマンドライン引数が入力されていないまたは2つ以外の場合はエラーを出して終了する
    if (argc != 2):
        print (r"証券コードが入力されていません")
        quit()

    #連番変更したいファイルが存在するフォルダを指定する　
    #コマンドライン引数を格納するリストから証券コードを取り出す
    #[0]はこのプログラムファイルなので[1]で証券コードを取り出す
    kigyoucode  = argsys[1]

    #企業名、株価を崇徳する関数
    symbol,stockprice = get_stockprice(kigyoucode)
    #関数の結果に応じて表示するメッセージを分ける
    if (stockprice != -1):
        #企業が見つかった場合
        print (r"企業名:" + symbol,r"株価:" + stockprice)
    else:
        #企業が見つからなかった場合
        print(r"指定された証券コードに対応する企業が見つかりませんでした")
