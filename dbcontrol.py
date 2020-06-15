import tkinter.messagebox as messagebox
from tkinter import *
import tkinter.ttk as ttk
from dbview import *
import sqlite3
import os

SQL_EROROR_MESSAGE = "sqlite3 Error:"
class DBLogic:
    """
    DBViewer読み込み、書き込みロジック
    """

    def __init__(self):
        """
        列とレコード用の配列を初期化
        """
        self.header =[]
        self.data =[]
        self.db_path=""
        self.table=""

    def readDataBase(self,db_path):
        """
        dbを読み込んでテーブルのリストを返す
        """
        table_list = []
        self.db_path = db_path
        if os.path.exists(db_path) == False:
            print("file not found")
            return table_list

        try :
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute("select name from sqlite_master where type='table'")
            table_list=[data[0] for data in cursor.fetchall()]
            connection.close()
        except sqlite3.Error as e:
            print(SQL_EROROR_MESSAGE, e)

        return table_list

    def readColumn(self,table_name):
        """
        選択されたテーブルの列名と主キーを取得する
        cursor.descriptionから列名をとることができるが、
        主キー情報を取得するためSQLiteのPRAGMA TABLE_INFOコマンドを発行し取得する
        """
        self.table_name = table_name
        column=[]
        p_key=""
        try :
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            # cursor.execute("select * from " + table_name)
            # for data in cursor.description:
            #     print(data)
            # column=[data[0] for data in cursor.description]
            sql = "PRAGMA TABLE_INFO("+table_name+")"
            cursor.execute(sql)
            for data in cursor.fetchall():
                column.append(data[1])
                if data[5] == 1:
                    p_key = data[1]

            connection.close()
        except sqlite3.Error as e:
            print(SQL_EROROR_MESSAGE, e)
        return column,p_key

    def readData(self,table_name):
        """
        選択されたテーブル名でSELECT文検索しデータを抽出する
        """
        raws=[]
        try :
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("select * from " + table_name + " ORDER BY id DESC")
            raws=[data for data in cursor.fetchall()]
            connection.close()
        except sqlite3.Error as e:
            print(SQL_EROROR_MESSAGE, e)
        return raws

    def updateRowData(self,coloumns,rows):
        """
        DBのデータを更新する
        """
        ret = True
        p =""
        r_pre = [column for column in coloumns]
        q_pre = ["?" for column in coloumns]

        r = ",".join(r_pre)
        q = ",".join(q_pre)
        replace = "replace into "+self.table_name+"("+r+")" + "values("+q+")"
        print(replace)
        try :
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            for row in rows:
                cursor.execute(replace,row)
            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            print(SQL_EROROR_MESSAGE, e)
            ret = False
        return ret

class DBControl:
    """
    DBViewerのコントローラー
    """
    def __init__(self):
        """
        アプリの立ち上げとイベント登録
        """
        master = Tk()
        master.title(TITLE_NAME_LABEL)
        master.geometry("1000x400")
        self.view = DBView(master)
        self.logic = DBLogic()
        self.view.setReadButtonCommand(self.readButtonCommand)
        self.view.setTableCommand(self.readTableCommand)
        self.view.setSaveButtonCommand(self.saveButtonCommand)
        master.mainloop()

    def readButtonCommand(self):
        """
        DB読み込みボタン用コマンド
        DBから取得した列名、データをViewに反映する。
        """
        file_path = self.view.getFilePath()
        table_list = self.logic.readDataBase(file_path)
        print(table_list)
        self.view.setTableNameList(table_list)

    def saveButtonCommand(self):
        """
        保存ボタン用コマンド
        指定されたパスにviewで指定された情報をDBに書きだす
        """
        columns = self.view.getColumns()
        rows =self.view.getRows()
        ret = self.logic.updateRowData(columns,rows)
        if ret:
            messagebox.showinfo(SAVE_MESSAGE_DIALOG_TITLE,SAVE_MESSAGE_SUCCEED)
        else:
            messagebox.showerror(SAVE_MESSAGE_DIALOG_TITLE,SAVE_MESSAGE_FAILED)

    def readTableCommand(self):
        """
        選択されたテーブル名から
        列名、主キー、データを取得し画面に反映させる
        """
        table_name = self.view.getSelectTable()
        columns,p_key = self.logic.readColumn(table_name)
        datas = self.logic.readData(table_name)
        self.view.setNewColumnAndData(columns,datas)
        self.view.setPrimaryKey(p_key)


if __name__ == '__main__':
    control =  DBControl()