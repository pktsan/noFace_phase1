# coding:utf-8
from bottle import run, route, get, post, static_file, template, redirect
from bottle import request
import mysql.connector
import random
import json
import os
import cgi

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

#GETの場合
@get('/makeUrl')
def getMakeUrl():
    #値取得
    #print("get")
    #data = request.environ.get('ranNo')
    #data = params.get('ranNo')
    #params = FormsDict()
    #data = request.params('ranNo')
    


    #print(data)
    #print(type(data))
    #data = request.params.get('ranNo')
    data = request.params.get.ranNo
    #query = cgi.parse_qsl(environ.get('ranNo'))
    #data = parse_query(query)
    #params = json.loads(data)
    #c = params['ranNo']

    #print(data)
    #print(params)
    #       print(c)
    
    testDict = {
        'one': 1,
        'two': 2,
    }
    result = json.dumps(testDict)
    
    print(result)
    
    return result
#return template('top')

#POSTの場合
@post('/makeUrl')
def postMakeUrl():
    print("post")
    #ID発番
    ranNo = mkranId()
    print(ranNo)
    #URL取得
    url = dbconn(ranNo)
    #ID NULLチェック
    if isUrlCheck(url):
        print('checkedUrl:')
        print(url)
        #redirect(url)
        return template('next',url=url)
    else:
        postMakeUrl()

#ランダムにIdを発番する関数
def mkranId():
    setNm = 10
    list(range(setNm))
    ranNo = random.randrange(setNm)
    return ranNo

#URLがNULLでないことを確認する関数
def isUrlCheck(url):
    if url == None:
        print('チェックNG')
        return False
    else:
        print('チェックOK')
        return True

#DBに接続し結果を取得する関数
def dbconn(ranNo):
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