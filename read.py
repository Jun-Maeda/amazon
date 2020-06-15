import os, tkinter, tkinter.filedialog, tkinter.messagebox
from tkinter import filedialog

# ファイル選択ダイアログの表示
root = tkinter.Tk()
# 見た目の設定
# 画面作成
root.geometry('800x600') # 画面サイズの設定
root.title('amazon価格確認アプリ') # 画面タイトルの設定


# ボタンの作成
btn = tkinter.Button(root, text='ボタン', command = file_select) # ボタンの設定(text=ボタンに表示するテキスト)
btn.place(x=130, y=20) #ボタンを配置する位置の設定



root.mainloop()
