# coding:utf-8
from bottle import run, route, get, post, static_file, template, redirect
from bottle import request
import mysql.connector
import random
import json
import os

#ファイルパス
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

#CSS
@route('/assets/css/<filename:path>')
def send_static(filename):
    return static_file(filename, root=f'{STATIC_DIR}/css')

#rootの場合
@route("/")
def index():
    return template('top')

@post('/spa')
def getMakeUrl():
    #値取得
    data = request.json
    ranNo = data['ranNo']
    print(ranNo)
    #URL取得
    url = dbconn(ranNo)
    #ID NULLチェック
    if isUrlCheck(url):
        print('checkedUrl:')

        #json作成
        url = {'id':ranNo, 'url':url}
        url = json.dumps(url)
 
        print(url)
        print(type(url))
        return url
    else:
        return reMakeUrl() 
   
def reMakeUrl():

    """
    urlの再取得を行う

    Parameters
    ----------
    なし

    Returns
    -------
    url : text
        jsonタイプのidとurl
    """

    #ID発番
    ranNo = mkranId()
    print(ranNo)
    #URL取得
    url = dbconn(ranNo)
    #ID NULLチェック
    if isUrlCheck(url):
        print('checkedUrl:')
        #json作成
        url = {'id':ranNo, 'url':url}
        reUrl = json.dumps(url)
        print('reUrl')
        print(type(url))
        print(reUrl)
        return reUrl
    else:
        reMakeUrl()


def mkranId():

    """
    ランダムにIdを発番する

    Parameters
    ----------
    なし

    Returns
    -------
    ranNo : int
       ランダムなid 
    """

    setNm = 10
    list(range(setNm))
    ranNo = random.randrange(setNm)
    return ranNo

def isUrlCheck(url):

    """
    urlがNoneでないことを確認

    Parameters
    ----------
    url : text

    Returns
    -------
    bool値
    """

    if url == None:
        print('チェックNG')
        return False
    else:
        print('チェックOK')
        return True


def dbconn(ranNo):

    """
    データベース接続

    Parameters
    ----------
    ranNo : int

    Returns
    -------
    url : text
       urlを返却 
    """

    try:
        #DB設定
        try:
            f = open('./conf/prop.json', 'r')
            info = json.load(f)
            print('ファイルopen成功')
        except:
            print('ファイルopenエラー')
        conn = mysql.connector.connect(
            host = info['host'],
            port = info['port'],
            user = info['user'],
            password = info['password'],
            database = info['database'],
        )
        #データベースに接続する
        c = conn.cursor()
        #接続クエリ
        sql = 'SELECT url FROM yahoo_news_urls WHERE id ='
        #データ登録
        print('ranNo')
        print(ranNo)
        #クエリ発行
        c.execute(sql+'%s', [ranNo])
        c.statement
        url = c.fetchone() 
        #クローズ
        conn.close()
        return url[0]
    except:
        print("DBエラーが発生しました")

if __name__ == "__main__":
    run(host='localhost', port=8080, reloader=True, debug=True)