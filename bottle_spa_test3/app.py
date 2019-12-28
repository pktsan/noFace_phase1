# coding:utf-8
from bottle import run, route, get, post, static_file, template, redirect
from bottle import request
import mysql.connector
import random
import json
import os
import cgi
import sys
import io

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
        return url
    else:
        postMakeUrl()
   

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