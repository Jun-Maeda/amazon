from tkinter import *
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

TITLE_NAME_LABEL="SQLiteViewer"
FILE_PATH_LABEL="FilePath"
FILE_OPEN_BUTTON_LABEL="open"
FILE_READ_BUTTON_LABEL="read"
TABLE_LIST_LABEL="TableList"
TABLE_SELECT_BUTTON_LABEL="select"
TREE_TITLE_LABEL="DBData"
ROW_DATA_TITLE_LABEL="RawData"
ROW_DATA_UPDATE_BUTTON_LABEL="update"
ROW_DATA_INSERT_BUTTON_LABEL="insert"
ROW_DATA_SAVE_BUTTON_LABEL="save"
INSERT_MESSAGE_DIALOG_TITLE="insert"
INSERT_MESSAGE_SUCCEED="insert succeed"
INSERT_MESSAGE_FAILED="insert failed"
UPDATE_MESSAGE_DIALOG_TITLE="update"
UPDATE_MESSAGE_SUCCEED="update succeed"
SAVE_MESSAGE_DIALOG_TITLE="save"
SAVE_MESSAGE_SUCCEED="save succeed"
SAVE_MESSAGE_FAILED="save failed"

class FileOpenFrame(ttk.Frame):
    """
    ファイルの読み込み用フレーム
    """
    def __init__(self, master,file_entry_width=100):
        super().__init__(master)
        self.filePath = StringVar()
        self.createWidget(file_entry_width)
        self.pack()

    def createWidget(self,entry_width):
        filePathLabel = ttk.Label(self,text=FILE_PATH_LABEL)
        filePathLabel.grid(column=0,row=0)
        filepathEntry = ttk.Entry(self,textvariable=self.filePath,widt=entry_width)
        filepathEntry.grid(column=1,row=0)
        filepathButton = ttk.Button(self,text=FILE_OPEN_BUTTON_LABEL,command=self.openFileDialog)
        filepathButton.grid(column=2,row=0)
        self.readButton = ttk.Button(self,text=FILE_READ_BUTTON_LABEL)
        self.readButton.grid(column=3,row=0)

    def openFileDialog(self):
        """
        ファイルダイアログを開く
        """
        file  = filedialog.askopenfilename(filetypes=[("sqliteファイル", "*.*")]);
        self.filePath.set(file)

    def getFilePath(self):
        return self.filePath.get()

    def setReadButtonCommand(self,func):
        """
        読み込みを押したときのコマンドを指定する
        """
        self.readButton["command"] = func

class ComboboxFrame(ttk.Frame):
    def __init__(self, master,combo_width=100):
        super().__init__(master)
        self.table = StringVar()
        self.createWidget(combo_width)
        self.pack()

    def createWidget(self,entry_width):
        table_label = ttk.Label(self,text=TABLE_LIST_LABEL)
        table_label.grid(column=0,row=0)
        self.combo= combo = ttk.Combobox(self,textvariable=self.table,width=entry_width,state="readonly")
        combo.grid(column=1,row=0)
        self.select_button = select_button = ttk.Button(self,text=TABLE_SELECT_BUTTON_LABEL)
        select_button.grid(column=2,row=0)

    def setComboValues(self,values):
        self.table.set(values[0])
        print(self.table.get())
        self.combo['values'] = values

    def getTableName(self):
        return self.table.get()

    def setTableCommand(self,func):
        self.select_button['command'] = func

class TreeView(ttk.Frame):
    """
    DBのデータを実際に表示するTreeview
    """
    def __init__(self,master):
        super().__init__(master)
        self.tree = None
        self.selected_iid = None
        self.columns =[]
        self.createWidget()
        self.pack()
        self.setSampleData()
    def createWidget(self):
        """
        icon列は不要なのでshow="headings"を指定
        """
        self.tree = ttk.Treeview(self)
        self.tree["show"] = "headings"
        self.tree.pack()

    def setColomns(self,columns):
        """
        テーブルの列名を指定
        """
        self.columns = columns
        self.tree["columns"] = self.columns
        for col in columns:
            self.tree.heading(col,text=col)

    def setRow(self,index ="" ,row_data=[]):
        """
        新規レコードの挿入
        """
        self.tree.insert("",index="end",text=index,values = row_data)

    def setRows(self,rows_data):
        """
        複数の新規レコードの挿入
        """
        for i,row_data in enumerate(rows_data):
            self.setRow(index = i,row_data = row_data)

    def setSampleData(self):
        """
        起動時のサンプルデータ
        """
        column_data = ("Name","Value")
        rows_data = [("None","None")]
        self.deleteRows()
        self.setColomns(column_data)
        self.setRows(rows_data)

    def deleteRows(self):
        """
        レコードの全削除
        """
        children = self.tree.get_children("")
        for child in children:
            self.tree.delete(child)

    def addSelectAction(self,func):
        """
        レコードが選択されたときに呼ばれるイベントを登録
        """
        self.tree.bind("<<TreeviewSelect>>",func)

    def getItem(self):
        """
        現在選択状態のレコードの取得
        """
        self.selcted_iid = self.tree.focus()
        return self.tree.item(self.selcted_iid,"values")
    def getRows(self):
        """
        全レコードの取得
        """
        rows =[]
        children = self.tree.get_children("")
        for child in children:
            item = self.tree.item(child,"values")
            rows.append(item)
        return rows

    def getColumn(self):
        """
        列名の取得
        """
        return self.columns

    def getDataMap(self):
        """
        現在選択されているレコードの
        列名と値のマップを取得
        """
        item = self.getItem()
        if len(self.columns) != len(item):
            return {"none":"none"}
        else:
            data_map = {}
            for i,column in enumerate(self.columns):
                data_map[column] = item[i]
            return data_map

    def updateValue(self,iid,new_values):
        """
        値の更新
        """
        self.tree.item(self.iid,values=new_values)

    def updateValue(self,new_values):
        """
        現在選択されているレコードの値の更新
        """
        self.tree.item(self.selcted_iid,values=new_values)

    def update(self,value_dict):
        """
        マップからリストに変更後
        値の更新
        """
        data =[]
        for column in self.columns:
            data.append(value_dict[column])
        self.updateValue(data)

    def insert(self,value_dict):
        """
        マップからリストに変更後
        新規レコードの挿入
        """
        data =[]
        for column in self.columns:
            data.append(value_dict[column])
        children = self.tree.get_children("")
        index = len(children)
        self.setRow(index = str(index), row_data=data)

class LabelEntryWidget(ttk.Frame):
    """
    LabelとEntryがくっついたWidget
    """
    def __init__(self, master,text="property"):
        super().__init__(master)
        self.value = StringVar()
        self.createWidgets(text)

    def createWidgets(self,text="property"):
        self.label = ttk.Label(self,text=text)
        self.label.pack(side="left")
        self.entry = ttk.Entry(self,textvariable=self.value)
        self.entry.pack(side="left")

    def getVar(self):
        """
        値を取得するためのWidget変数の取得
        """
        return self.value


    def setLabelOption(self,key_dict):
        """
        Labelのオプション指定(オプションはdictで渡す)
        """
        for k in key_dict.keys():
            self.label[k] = key_dict[k]


    def setEntryOption(self,key_dict):
        """
        Entryのオプション指定(オプションはdictで渡す)
        """
        for k in key_dict.keys():
            self.entry[k] = key_dict[k]


class PropertyView(ttk.Frame):
    """
    選択されたレコードの内容を修正、
    新規レコードなどを挿入するフレーム
    """
    def __init__(self,master):
        super().__init__(master)
        self.pack()
        self.param_dict={}
        self.save_func = None

    def createWidget(self,columns):
        """
        列の要素数分入力ボックスの作成
        """
        self.delete()
        self.param_dict ={}
        for column in columns:
            option = {"width":10}
            param = LabelEntryWidget(self,text = column)
            param.setLabelOption(option)
            param.pack()
            self.param_dict[column] = param.getVar()
        self.createInsertUpdateButton()
        self.createSaveButton()

    def createInsertUpdateButton(self):
        """
        更新ボタンと挿入ボタンを作成
        """
        button_frame = ttk.Frame(self)
        button_frame.pack(anchor="e")
        self.update_button = update = ttk.Button(button_frame,text = ROW_DATA_UPDATE_BUTTON_LABEL)
        self.insert_button = insert = ttk.Button(button_frame,text = ROW_DATA_INSERT_BUTTON_LABEL)
        update.pack(side="left")
        insert.pack(side="left")

    def createSaveButton(self):
        """
        保存ボタンを作成
        """
        save_frame = ttk.Frame(self)
        save_frame.pack(anchor="e")

        self.save_button = save = ttk.Button(save_frame,text = ROW_DATA_SAVE_BUTTON_LABEL)
        if self.save_func:
            self.save_button["command"] = self.save_func
        save.pack(side="left")

    def delete(self):
        """
        更新時用
        自身のフレームに紐づく子Widgetの削除
        """
        children = self.winfo_children()
        for child in children:
            child.destroy()

    def setUpdateButtonCommand(self,command):
        """
        updateボタンにコマンドを登録する
        """
        self.update_button["command"] = command

    def setInsertButtonCommand(self,command):
        """
        insertボタンにコマンドを登録する
        """
        self.insert_button["command"] = command

    def setSaveButtonCommand(self,command):
        """
        saveボタンに保存コマンドを登録する
        データが登録されるごとに登録しなおす必要があるので関数も別途保持する
        """
        self.save_button["command"] =self.save_func = command

    def setParameter(self,param):
        """
        取得したレコードデータを各入力ボックスのWidget変数に振り分け
        """
        for key in self.param_dict.keys():
            self.param_dict[key].set(param[key])

    def getParameter(self):
        """
        列名とWidget変数の値をマップにして返す
        """
        param_dict = {}
        for key,value in self.param_dict.items():
            param_dict[key] = value.get()
        return param_dict


class DBView(ttk.Frame):
    """
    DBViewerのメインView

    """
    def __init__(self, master):
        super().__init__(master,borderwidth=10)
        self.tree = None
        self.p_key_id =-1
        self.createWidget()
        self.setAction()
        self.pack()

    def createWidget(self):
        """
        viewの組み立て
        """
        self.createUpperFrame()
        self.createLowerFrame()

    def createUpperFrame(self):
        """
        DB読み込み用フレーム
        """
        upper_frame = ttk.Frame(self)
        upper_frame.pack()
        self.file_path_frame = FileOpenFrame(upper_frame)
        self.combo_box_frame = ComboboxFrame(upper_frame)
        self.combo_box_frame.setComboValues(["none"])

    def createLowerFrame(self):
        """
        Treeviewとレコード編集Widget用フレーム
        """
        lower_frame = ttk.Frame(self)
        lower_frame.pack()
        left_frame = ttk.LabelFrame(lower_frame,text=TREE_TITLE_LABEL)
        left_frame.pack(side="left")
        self.tree = TreeView(left_frame)
        right_frame = ttk.LabelFrame(lower_frame,text=ROW_DATA_TITLE_LABEL)
        right_frame.pack(side = "right",anchor="n")

        self.property = PropertyView(right_frame)
        self.property.createWidget(self.tree.getColumn())


    def setAction(self):
        """
        ツリーアイテム選択アクションの登録
        """
        def _updateCommand():
            """
            更新アクション
            """
            param = self.property.getParameter()
            item = self.tree.getDataMap()
            if self.p_key != "":
                if param[self.p_key] != item[self.p_key]:
                    _insertCommand()
                    return
            self.tree.update(param)
            messagebox.showinfo(UPDATE_MESSAGE_DIALOG_TITLE,UPDATE_MESSAGE_SUCCEED)

        def _insertCommand():
            """
            挿入アクション
            """
            param = self.property.getParameter()
            # 重複チェックを行う
            if self.checkPrimaryKey(param):
                self.tree.insert(param)
                messagebox.showinfo(INSERT_MESSAGE_DIALOG_TITLE,INSERT_MESSAGE_SUCCEED)
            else:
                messagebox.showerror(INSERT_MESSAGE_DIALOG_TITLE,INSERT_MESSAGE_FAILED)

        def _func(event):
            """
            レコード選択アクション
            レコード選択ごとに更新インサートコマンドを登録しなおす
            """
            self.property.setParameter(self.tree.getDataMap())
            self.property.setUpdateButtonCommand(_updateCommand)
            self.property.setInsertButtonCommand(_insertCommand)

        self.tree.addSelectAction(_func)

    def getFilePath(self):
        """
        ファイルパスの取得
        """
        return self.file_path_frame.getFilePath()

    def setReadButtonCommand(self,func):
        """
        読み込みボタンコマンド登録
        """
        self.file_path_frame.setReadButtonCommand(func)

    def setNewColumnAndData(self,columns,rows):
        """
        新しい列名とレコードを設定する。
        プロパティのWidgetも更新する。
        """
        self.tree.deleteRows()
        self.tree.setColomns(columns)
        self.tree.setRows(rows)
        self.property.createWidget(self.tree.getColumn())

    def setSaveButtonCommand(self,func):
        """
        保存ボタンコマンド登録
        """
        self.property.setSaveButtonCommand(func)
    def getColumns(self):
        """
        列名リスト取得
        """
        return self.tree.getColumn()
    def getRows(self):
        """
        レコードリスト取得
        """
        return self.tree.getRows()

    def setTableNameList(self,values):
        """
        DBに入っているテーブルのリストを設定する
        """
        self.combo_box_frame.setComboValues(values)

    def getSelectTable(self):
        """
        選択されているテーブル名を取得する
        """
        return self.combo_box_frame.getTableName()

    def setTableCommand(self,func):
        """
        テーブル名を決定したときのコマンドを登録する
        """

        self.combo_box_frame.setTableCommand(func)

    def setPrimaryKey(self,p_key):
        """
        主キーを登録する
        主キーと列名から対応する列番号も保持しておく
        """
        self.p_key = ""
        self.p_key_id= -1
        for id,column in enumerate(self.getColumns()):
            if column == p_key:
                self.p_key = p_key
                self.p_key_id= id

    def checkPrimaryKey(self,new_data):
        """
        主キーが登録済みでない(登録可能)か調べる
        主キーが設定されていなければ常に登録可能
        """
        if self.p_key == "" or self.p_key_id == -1:
            return True
        print(self.p_key,new_data)
        check_data = new_data[self.p_key]
        print(check_data)
        for row in self.getRows():
            if check_data == row[self.p_key_id]:
                return False
        return True



if __name__ == '__main__':
    master = Tk()
    master.title("DBview")
    DBView(master)
    master.geometry("800x400")
    master.mainloop()



