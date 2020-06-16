amazon価格スクレイピングアプリケーション
 
# DEMO
 

 
# Features
 
products.csvに登録したＵＲＬの店舗名と金額を取得してそれぞれのデータベースに保存。
最低価格を取得。
最低価格が変わっていればメール通知して保存。
 
# Requirement
 
 
* requests
* bs4
* sqlite3
* datetime
* os
* smtplib
* email
* pandas


 
# Installation
 
 
```bash
pip install 〇〇
```
 
# Usage
 
そのあと、メールアドレスとパスワードを自分のgmail情報に書き換える。
products.csvに取得したいamazonの商品名とＵＲＬを記載（プライムで絞り込んだもの）。
main.pyをcronやタスクスケジューラで処理を自動化させる。
 
```bash
python main.py
```
 
# Note
 
注意点などがあれば書く
 
# Author
 
作成情報を列挙する
 
* 作成者 mj
* 所属
* E-mail
 
# License
ライセンスを明示する
 
"hoge" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
 
社内向けなら社外秘であることを明示してる
 
"hoge" is Confidential.