import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import datetime
import os
from creat_db import creat_table,insert_db,select_db,select_price,row_creat_table,row_insert_db,row_select_db,row_select_price
import pandas as pd
from read_csv import product_csv
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate




#現在の時間を取得
dt_now = datetime.datetime.now() 

#調べたいものの名前とＵＲＬを辞書に入れる
csvfile = "products.csv"
url = product_csv(csvfile)

#最安値を保存するデータベース名を指定
row_db = "data/row.db"


#商品、ＵＲＬ事に処理を繰り返す
for s,v in url.items():
    shop = []
    price = []
    row_shop = ""
    row_price = ""
    target_url = v
    dbname = f"data/{s}.db"
    r = requests.get(target_url)         #requestsを使って、ＵＲＬから情報を取得
    soup = BeautifulSoup(r.text, 'lxml') #要素を抽出
    
    creat_table(dbname)
    row_creat_table(row_db)


    #金額を取得
    for a in soup.find_all('span', class_='a-size-large'):
    #    不要な記号を消して数字型に変換する
        pr = a.text.strip("￥ ")
        pn = pr.replace(",", "")
        price.append(int(pn))

#    店舗名を取得
    for a in soup.find_all('h3', class_='olpSellerName'):
        sn = a.text.strip("\n")
        sn = sn.strip(" ")
        if sn == "":
            sn = "amazon"
        shop.append(sn)

     
    
#    取得したデータ分だけ処理
    for i in range(len(shop)):
        sname = shop[i]
        sprice = price[i]
#         データベースに保存
        insert_db(dbname,sname,sprice,dt_now)
#        その中で最安値を取得
        if (row_price == "") or (sprice < row_price):
            row_shop = sname
            row_price = sprice


        
    #    前回の最安値を取得
    bprice = row_select_price(s)
    rprice = row_price
    rshop = row_shop

    if bprice is None:
        print("初めてのデータ。")
        row_insert_db(row_db,rshop,rprice,s,dt_now)
    elif rprice != bprice:
        mailadd = "mymail@gmail.com"
        mailtxt = f"{s}にて価格の変動がありました。\n{row_shop}:{bprice}→{rprice}"
        send_mail(mailadd,mailadd,bodytxt)
            #       データベースに保存 
        row_insert_db(row_db,rshop,rprice,s,dt_now)
    else:
        print("変わりませんでした。")            


        
    
    
    
    
    
##ショップ名と値段をそれぞれ一緒のリストにする
#shop_info = []    
#for i in range(len(shop)):
#    shop_info.append([shop[i],price[i]])
#
   
    
#    
##csvで取得
#f = open('some.csv', 'w')
#
#writer = csv.writer(f, lineterminator='\n')
#
#for i in shop_info:
#    writer.writerow(i)
#
#f.close()



        
    
    
    