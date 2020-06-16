import datetime
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


#指定のデータベースがなければ作成
def creat_table(dbpath):
    if not os.path.exists(dbpath):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS amazon
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  price INTEGER,
                  date DATETIME)'''
        c.execute(sql)
        conn.close()
        
#最低価格のデータベースがなければ作成
def row_creat_table(dbpath):
    if not os.path.exists(dbpath):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS rower
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  price INTEGER,
                  product TEXT,
                  date DATETIME)'''
        c.execute(sql)
        conn.close()


#データベースへ保存
def insert_db(dbpath,sname,sprice,sdate):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    c.execute("insert into amazon(name,price,date) values(?,?,?)",(sname,sprice,sdate));
    conn.commit()
    conn.close()
    
#最低価格をデータベースへ保存
def row_insert_db(dbpath,sname,sprice,sproduct,sdate):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    c.execute("insert into rower(name,price,product,date) values(?,?,?,?)",(sname,sprice,sproduct,sdate));
    conn.commit()
    conn.close()
    

#データベースから全部出力
def select_db(dbpath):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    list = c.execute("select * from amazon")
    for i in list:
        print(i)
    conn.close()
    
#最低価格をデータベースから全部出力
def row_select_db(dbpath):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    list = c.execute("select * from rower")
    for i in list:
        print(i)
    conn.close()
    
    
#同じ店舗名で一番最近の金額データを出力
def select_price(dbpath,sname):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    list = c.execute("select * from amazon where name=? ORDER BY id DESC limit 1",(sname,))
    for l in list:
        return l[2]
    conn.close()
    
#一番最近の金額データを出力
def row_select_price(pname):
    conn = sqlite3.connect("data/row.db")
    c = conn.cursor()
    list = c.execute("select * from rower where product=? ORDER BY id DESC limit 1",(pname,))
    for l in list:
        return l[2]
    conn.close()
    

#メールを送信する
def send_mail(from_addr, to_addr, body_msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login("mymail@gmail.com", "mypassword")
    smtpobj.sendmail(from_addr, to_addr, body_msg.encode('utf-8'))
    smtpobj.close()

    
if __name__ == "__main__":
    
    dbpath = 'Ｒ１低糖24本.db'    
    dt_now = datetime.datetime.now()    

    #create_table(dbpath)

    #insert_db(dbpath,"moumou",2550,dt_now)

#    select_db(dbpath)

    #print(select_price(dbpath,"momou"))
#    ここから
#    row_select_db("row.db")
#    print(row_select_price("ザバス(SAVAS) ミルクプロテイン 脂肪 0 ココア風味24本"))


#    toadd = "ishida@rinsendo.com"
#    mymail = "ishida@rinsendo.com"
#    s = "ザバス"
#    row_shop = "モウモウ"
#    bprice = 2550
#    rprice = 2660
#    bodytxt = f"{s}にて価格の変動がありました。\n{row_shop}:{bprice}→{rprice}"
#    send_mail(mymail,mymail,bodytxt)