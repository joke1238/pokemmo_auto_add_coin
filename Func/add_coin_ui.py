import time
import tkinter as tk
from tkinter import Checkbutton, IntVar, ttk
import threading
from pokemmo.Func.add_gold import Add_Gold
import requests


class AddCoinApp:
    def __init__(self, root):
        self.add_gold = Add_Gold()
        self.running = False
        self.countdown_seconds = 3600

        root.title("Add Coin")
        root.geometry("540x400")
        root.configure(bg="#f0f4f8")
        root.resizable(False, False)

        # 控制区（左）
        control_frame = tk.Frame(root, bg="#e2e8f0")
        control_frame.place(x=10, y=10, width=120, height=380)

        self.start_button = tk.Button(control_frame, text="▶ 开始", bg="#4caf50", fg="white",
                                      font=("微软雅黑", 9))
        self.start_button.place(x=10, y=10, width=100, height=35)
        self.start_button.bind("<Button-1>", self.start_script)

        self.end_button = tk.Button(control_frame, text="■ 停止", bg="#f44336", fg="white",
                                    font=("微软雅黑", 9))
        self.end_button.place(x=10, y=50, width=100, height=35)
        self.end_button.bind("<Button-1>", self.stop_script)

        self.check_box_var = IntVar()
        self.check_box = Checkbutton(control_frame, text="结束后关闭", variable=self.check_box_var,
                                     bg="#e2e8f0", font=("微软雅黑", 8))
        self.check_box.place(x=10, y=95, width=100, height=20)

        self.countdown_label = tk.Label(control_frame, text="倒计时：00:00:00", bg="#e2e8f0",
                                        font=("微软雅黑", 8, "bold"))
        self.countdown_label.place(x=10, y=120, width=100, height=20)

        tk.Label(control_frame, text="时间(分钟)", bg="#e2e8f0", font=("微软雅黑", 8)).place(x=10, y=145)
        self.time_var = tk.StringVar(value="60")
        self.time_selector = ttk.Combobox(control_frame, textvariable=self.time_var,
                                          state="readonly", font=("微软雅黑", 8))
        self.time_selector['values'] = [str(i) for i in range(10, 181, 10)]
        self.time_selector.place(x=10, y=165, width=100)

        # 数据统计（更紧凑）
        stats_y = 200
        self.create_stat(control_frame, "金币", self.add_gold.gold, stats_y)
        self.create_stat(control_frame, "爪子", self.add_gold.paw, stats_y + 30)
        self.create_stat(control_frame, "香气", self.add_gold.aroma, stats_y + 60)

        # 信息展示区（右）
        info_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
        info_frame.place(x=140, y=10, width=390, height=380)

        self.text_move_title = self.create_right_label(info_frame, "move_check", 10, 5)
        self.text_move = self.create_right_text(info_frame, 10, 28, 180, 320)

        self.label_pokemon = self.create_right_label(info_frame, "pokemon", 200, 5)
        self.text_pokemon = self.create_right_text(info_frame, 200, 28, 180, 100)

        self.label_pc = self.create_right_label(info_frame, "pc", 200, 140)
        self.text_pc = self.create_right_text(info_frame, 200, 165, 370, 200)

    def create_stat(self, parent, label_text, value, y):
        tk.Label(parent, text=f"累计{label_text}", bg="#e2e8f0", font=("微软雅黑", 8)).place(x=10, y=y)
        entry = tk.Entry(parent, justify='center', font=("微软雅黑", 9), width=12)
        entry.insert(0, value)
        entry.place(x=10, y=y + 15)

        if "金币" in label_text:
            self.lineEdit_coin_num = entry
        elif "爪子" in label_text:
            self.lineEdit_paws_num = entry
        elif "香气" in label_text:
            self.lineEdit_aroma_num = entry

    def create_right_label(self, parent, text, x, y):
        label = tk.Entry(parent, justify='center', font=("微软雅黑", 8))
        label.insert(0, text)
        label.configure(state='readonly', bg="#e2e8f0")
        label.place(x=x, y=y, width=180, height=20)
        return label

    def create_right_text(self, parent, x, y, width, height):
        text = tk.Text(parent, font=("微软雅黑", 8), wrap="word")
        text.place(x=x, y=y, width=width, height=height)
        return text

    def safe_insert(self, widget, msg, max_lines=100):
        widget.insert(tk.END, msg)
        lines = widget.get("1.0", tk.END).split("\n")
        if len(lines) > max_lines:
            widget.delete("1.0", f"{len(lines) - max_lines}.0")

    def start_script(self, event):
        if not self.running:
            self.running = True
            try:
                minutes = int(self.time_var.get())
            except ValueError:
                minutes = 60
            self.countdown_seconds = minutes * 60

            threading.Thread(target=self.run_script_loop, daemon=True).start()
            threading.Thread(target=self.update_entries, daemon=True).start()
            threading.Thread(target=self.update_countdown, daemon=True).start()
            self.safe_insert(self.text_move, "✨ 脚本已启动\n")

    def stop_script(self, event=None):
        self.running = False
        self.safe_insert(self.text_move, "🛑 脚本已终止\n")

    def run_script_loop(self):
        end_time = time.time() + self.countdown_seconds
        while self.running and time.time() < end_time:
            self.add_gold.main()
            time.sleep(1)
        self.running = False
        self.safe_insert(self.text_move, "🛑 脚本已终止\n")
        if self.check_box_var.get():
            self.safe_insert(self.text_move, "⏹️ 自动关闭窗口\n")
            self.add_gold.close_window()
        requests.get("http://miaotixing.com/trigger?id=tnvffj1")

    def update_entries(self):
        fail_count = 0
        while self.running:
            self.lineEdit_coin_num.delete(0, tk.END)
            self.lineEdit_coin_num.insert(0, self.add_gold.gold)
            self.lineEdit_paws_num.delete(0, tk.END)
            self.lineEdit_paws_num.insert(0, self.add_gold.paw)
            self.lineEdit_aroma_num.delete(0, tk.END)
            self.lineEdit_aroma_num.insert(0, self.add_gold.aroma)

            if self.add_gold.text_move_flag == 1:
                self.safe_insert(self.text_move, self.add_gold.text_move + "\n")
                self.add_gold.text_move_flag = 0
            if self.add_gold.text_poke_flag == 1:
                self.text_pokemon.insert(tk.END, self.add_gold.text_poke + "\n")
                self.add_gold.text_poke_flag = 0
            if self.add_gold.text_pc_flag == 1:
                self.text_pc.insert(tk.END, self.add_gold.text_pc + "\n")
                self.add_gold.text_pc_flag = 0

            if self.add_gold.move_flag == 1:
                if self.add_gold.pokeDll.getMove() == 0:
                    fail_count += 1
                else:
                    fail_count = 0
                if fail_count >= 10:
                    self.safe_insert(self.text_move, "⚠️ 连续异常，正在停止脚本...\n")
                    requests.get("http://miaotixing.com/trigger?id=t1CyfXL")
                    self.stop_script()
                    self.add_gold.close_window()
                    break

            time.sleep(0.5)

    def update_countdown(self):
        while self.running and self.countdown_seconds > 0:
            mins, secs = divmod(self.countdown_seconds, 60)
            hrs, mins = divmod(mins, 60)
            self.countdown_label.config(text=f"倒计时：{hrs:02}:{mins:02}:{secs:02}")
            time.sleep(1)
            self.countdown_seconds -= 1


if __name__ == "__main__":
    root = tk.Tk()
    app = AddCoinApp(root)
    root.mainloop()
