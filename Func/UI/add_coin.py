import tkinter as tk
from tkinter import Text, Checkbutton, IntVar

class AddCoinApp:
    def __init__(self, root):
        root.title("add_coin")
        root.geometry("418x308")
        root.configure(bg="#e8f0fe")  # 窗口背景色淡蓝

        # 按钮 start
        self.start_button = tk.Button(root, text="▶ 开始", bg="#4caf50", fg="white", font=("微软雅黑", 10, "bold"))
        self.start_button.place(x=0, y=0, width=91, height=61)

        # 按钮 end
        self.end_button = tk.Button(root, text="■ 停止", bg="#f44336", fg="white", font=("微软雅黑", 10, "bold"))
        self.end_button.place(x=0, y=60, width=91, height=61)

        # 勾选框
        self.close_after_var = IntVar()
        self.check_box = Checkbutton(root, text="结束后关闭", variable=self.close_after_var, bg="#e8f0fe", font=("微软雅黑", 9))
        self.check_box.place(x=0, y=120, width=91, height=31)

        # 文本框 textEdit（主区域）
        self.text_edit = Text(root, font=("Courier New", 10), bg="white", fg="#333333", relief="solid", bd=1)
        self.text_edit.place(x=90, y=0, width=331, height=311)

        # 只读输入框 - 累计获得金币
        self.lineEdit_coin = self.create_readonly_entry(root, "累计获得金币", 150)

        # 只读输入框 - 累计获得爪子
        self.lineEdit_paws = self.create_readonly_entry(root, "累计获得爪子", 190)

        # 只读输入框 - 累计香气
        self.lineEdit_honey = self.create_readonly_entry(root, "累计香气", 230)

        # 可编辑输入框（作为结果数值）
        self.lineEdit_coin_num = self.create_centered_entry(root, "", 170)
        self.lineEdit_paws_num = self.create_centered_entry(root, "", 210)
        self.lineEdit_honey_num = self.create_centered_entry(root, "", 250)

    def create_readonly_entry(self, root, text, y):
        entry = tk.Entry(root, justify='center', font=("微软雅黑", 9), fg="#555", disabledbackground="#f0f0f0")
        entry.insert(0, text)
        entry.configure(state='readonly')
        entry.place(x=0, y=y, width=91, height=20)
        return entry

    def create_centered_entry(self, root, text, y):
        entry = tk.Entry(root, justify='center', font=("微软雅黑", 9), fg="#222")
        entry.insert(0, text)
        entry.place(x=0, y=y, width=91, height=20)
        return entry

if __name__ == "__main__":
    root = tk.Tk()
    app = AddCoinApp(root)
    root.mainloop()
