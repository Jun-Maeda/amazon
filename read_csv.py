import pandas as pd

#csvファイルから商品名とＵＲＬを取得してそれぞれを辞書に入れる
def product_csv(csv_file):
    read_lots = pd.read_csv(csv_file, header=0)
#    file = read_lots[read_lots["販売店舗"] == "Rakuten"]
    urls = {}
    shops = read_lots.iterrows()
    for i,n in shops:
        pname = n["商品名"]
        purl = n["URL"]
        urls.update({pname:purl})
        
        
    return urls

pcsv = product_csv("products.csv")

#print(pcsv)