import os
import datetime
# スリープを使うために必要
import time                                 
import mysql.connector
import json
# Webブラウザを自動操作する（python -m pip install selenium)
from selenium import webdriver              

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#定数一覧
driver = webdriver.Chrome(BASE_DIR+'./chromedriver.exe')
targetUrl = 'https://news.yahoo.co.jp/'

#遷移
driver.get(targetUrl)       
 
def ranking(driver):
    # ループ番号、ページ番号を定義
    i = 1 
    # 最大何ページまで分析するかを定義              
    i_max = 1

    while i <= i_max:
        # リンクはclass="topicsListItem"に入っている
        class_group = driver.find_elements_by_class_name("topicsListItem")
        # タイトルとリンクを抽出しリストに追加するforループ    
        for elem in class_group:

            # データ登録用
            title = elem.find_element_by_tag_name('a').text
            url = elem.find_element_by_tag_name('a').get_attribute('href')
            
            #日にち取得
            now = datetime.datetime.now()
            dt = "{0:%Y-%m-%d %H:%M:%S}".format(now)
            #DB設定
            f = open('./bottle_spa_test3/conf/prop.json', 'r')
            info = json.load(f)
            print(f)
            f.close()

            conn = mysql.connector.connect(
                host = info['host'],
                port = info['port'],
                user = info['user'],
                password = info['password'],
                database = info['database']
            )

            # データベースに接続する
            c = conn.cursor()
            #データ登録
            sql = "INSERT INTO testdb.yahoo_news_urls (title,url,dt) VALUES (%s,%s,%s)"
            c.execute(sql, (title, url, dt))
            print(c)
            # 挿入した結果を保存（コミット）する
            conn.commit()
            # データベースへのアクセスが終わったら close する
            conn.close()
        i = i_max + 1
#    return title_list, link_list   

# ranking関数を実行してタイトルとURLリストを取得する
ranking(driver)
# ブラウザを閉じる
driver.quit() 
# タイトルリストをテキストに保存
# URLリストをテキストに保存
#now = datetime.datetime.now()
#titleFilename = 'output/title_{0:%Y%m%d%H%M}.text'.format(now)
#linkFilename = 'output/link_{0:%Y%m%d%H%M}.text'.format(now)

#with open(titleFilename, mode='w', encoding='utf-8') as f:
#    f.write("\n".join(title))
# URLリストをテキストに保存
#with open(linkFilename, mode='w', encoding='utf-8') as f:
#    f.write("\n".join(link))
# ブラウザを閉じる
driver.quit()                              
