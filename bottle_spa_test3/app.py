# coding:utf-8
from bottle import run, static_file, template, redirect
from bottle import request, route, get, post
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

@get('/spa')
def getIndex():
    return template('top')

@post('/spa')
def getMakeUrl():
    #値取得
    data = request.json
    ranNo = data['ranNo']
    #print(ranNo)
    #URL取得
    url = dbconn(ranNo)
    #ID NULLチェック
    if isUrlCheck(url):
        print('checkedUrl:')
        #json作成
        #url = {'id':ranNo, 'url':url}
        jsonUrl = makeJson(url)
        print(jsonUrl)
        print(type(jsonUrl))
        return jsonUrl
    else:
        return reMakeUrl() 
   
def reMakeUrl():
    #ID発番
    ranNo = mkranId()
    print(ranNo)
    #URL取得
    url = dbconn(ranNo)
    #ID NULLチェック
    if isUrlCheck(url):
        print('checkedUrl:')
        #json作成
        jsonUrl = makeJson(url)
        print(type(jsonUrl))
        print(jsonUrl)
        return jsonUrl
    else:
        return reMakeUrl()


def mkranId():

    setNm = 10
    list(range(setNm))
    ranNo = random.randrange(setNm)
    return ranNo

def isUrlCheck(url):

    if url == None:
        print('チェックNG')
        return False
    else:
        print('チェックOK')
        return True

#def makeJson(ranNo,url):
def makeJson(url):
    #url = {'id':ranNo, 'url':url}
    jsonUrl = jsonDumps(url)
    return jsonUrl
    
def jsonDumps(url):
    url = json.dumps(url)
    return isTypeCheck(url)

def isTypeCheck(jsonUrl):
    if type(jsonUrl) is str:
        return jsonUrl
    else:
        jsonDumps(jsonUrl)
    

def dbconn(ranNo):

    f = open('./conf/prop.json', 'r')
    info = json.load(f)
    f.close()
    #DB設定
    
    conn = mysql.connector.connect(
            host = info['host'],
            port = info['port'],
            user = info['user'],
            password = info['password'],
            database = info['database'],
    )
    
    #データベースに接続する
    #c = conn.cursor()
    cur = conn.cursor(dictionary=True)   
    try:    
        #接続クエリ
        sql = 'SELECT id, title, url FROM yahoo_news_urls WHERE id ='
        #クエリ発行
        #デバックのため
        #ranNo = 5 
        print(ranNo)
        cur.execute(sql+'%s', [ranNo])
        cur.statement    
        #url = cur.fetchone()
        url = cur.fetchall()
        print(url)
        
        if url is not None: 
            return url[0]
        else:
            return None

    except:
        import traceback
        traceback.print_exc()
        print("DBエラーが発生しました")
        return None
    finally:
        cur.close()
        conn.close()
        
if __name__ == "__main__":
    run(host='localhost', port=8080, reloader=True, debug=True)