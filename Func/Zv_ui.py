import time
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
from pokemmo.Func.AutoSpeed import AutoSpeed
from pokemmo.Func.Hit_Point import AutoHp
from pokemmo.Func.attack import AutoAttack
from pokemmo.Func.specialAttack import AutoSpecialAttack


class EffortTrainerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Effort Trainer")
        self.geometry("520x440")  # 增加窗口高度以容纳新的选择框
        self.configure(bg="#F5F5F5")
        self.resizable(False, False)

        # 实例化功能类
        self.auto_hp = AutoHp()
        self.auto_attack = AutoAttack()
        self.auto_speed = AutoSpeed()
        self.auto_spatk = AutoSpecialAttack()

        self.running_task = None
        self.task_thread = None
        self.task_flags = {
            'speed': False,
            "hp": False,
            "attack": False,
            "spatk": False,
            "def": False,
            "exp": False
        }

        self.instance = {
            "hp": self.auto_hp,
            "speed": self.auto_speed,
            "attack": self.auto_attack,
            "spatk": self.auto_spatk,
            "exp": self.auto_speed
        }

        self.abandon_skill_flag = tk.BooleanVar(value=False)  # 初始化选择框的状态变量

        self.create_widgets()

    def create_widgets(self):
        # 标题
        ttk.Label(self, text="Effort Trainer", font=("Arial", 18, "bold")).pack(pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        # 各种刷努力按钮

        self.create_button(btn_frame, "刷 HP 努力", self.start_hp, 0)
        self.create_button(btn_frame, "刷 攻击 努力", self.start_attack, 1)
        self.create_button(btn_frame, "刷 特攻 努力", self.start_spatk, 2)
        self.create_button(btn_frame, "刷 速度 努力", self.start_speed, 3)


        # 停止按钮
        other_btn_frame = ttk.Frame(self)
        other_btn_frame.pack(pady=5)
        self.create_button(other_btn_frame, "停止所有", self.stop_all, 0)
        self.create_button(other_btn_frame, "刷经验", self.start_exp, 1)

        # 状态框架（数量显示）
        info_frame = ttk.Frame(self)
        info_frame.pack(pady=5)

        ttk.Label(info_frame, text="已刷取：", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_count = ttk.Entry(info_frame, font=("Arial", 12), width=10, justify="center")
        self.entry_count.grid(row=0, column=1, padx=5)

        # 选择框
        self.abandon_skill_check = ttk.Checkbutton(self, text="放弃学习技能", variable=self.abandon_skill_flag)
        self.abandon_skill_check.pack(pady=5)

        # 日志文本框
        self.text_browser = ScrolledText(self, wrap=tk.WORD, height=10, width=60, font=("Arial", 10), bg="#FFFFFF", fg="#000000", bd=1, relief="solid", insertbackground="#000000")
        self.text_browser.pack(pady=10, padx=10)

    def create_button(self, parent, text, command, column):
        btn = ttk.Button(parent, text=text, command=command)
        btn.grid(row=0, column=column, padx=8, ipadx=6, ipady=3, sticky="ew")

    def run_task(self, task_name, task_func):
        if self.running_task:
            messagebox.showwarning("已有任务在运行", f"当前正在运行：{self.running_task}，请先结束后再运行其他任务。")
            return

        self.running_task = task_name
        self.task_flags[task_name] = True
        self.text_browser.insert(tk.END, f"开始 {task_name}...\n")

        def task_wrapper():
            while self.task_flags[task_name]:
                task_func()

        self.task_thread = threading.Thread(target=task_wrapper, daemon=True)
        self.update_info_thread = threading.Thread(target=self.update_info, daemon=True)
        self.abandon_skills_thread = threading.Thread(target=self.abandon_skills, daemon=True)
        self.task_thread.start()
        self.update_info_thread.start()
        self.abandon_skills_thread.start()

    def stop_all(self):
        if self.running_task:
            self.task_flags[self.running_task] = False
            self.text_browser.insert(tk.END, f"已停止 {self.running_task}\n")
            self.running_task = None
            self.auto_hp.Map_flag = 0
            self.auto_speed.Map_flag = 0
            self.auto_attack.Map_flag = 0
            self.auto_spatk.Map_flag = 0
            self.auto_spatk.Ev = 0
            self.auto_attack.Ev = 0
            self.auto_speed.Ev = 0
            self.auto_hp.Ev = 0
        else:
            messagebox.showinfo("无任务", "当前没有正在运行的任务。")

    def start_hp(self):
        self.run_task("hp", self.auto_hp.main)

    def start_speed(self):
        self.run_task("speed", self.auto_speed.main)

    def start_attack(self):
        self.run_task("attack", self.auto_attack.main)

    def start_spatk(self):
        self.run_task("spatk", self.auto_spatk.main)

    def start_exp(self):
        self.run_task("exp", self.auto_speed.main)

    def update_info(self):
        while self.running_task and self.task_flags[self.running_task]:
            ev_value = 0
            text_output = ""
            if self.running_task == "hp":
                ev_value = self.auto_hp.Ev if self.auto_hp.Ev < 252 else 252
                if ev_value == 252:
                    self.text_browser.insert(tk.END, f"hp 努力已满\n")
                    self.stop_all()
                if self.auto_hp.text_flag:
                    text_output = self.auto_hp.text
                    self.auto_hp.text_flag = 0
            elif self.running_task == "speed":
                ev_value = self.auto_speed.Ev if self.auto_speed.Ev < 252 else 252
                if ev_value == 252:
                    self.text_browser.insert(tk.END, f"speed 努力已满\n")
                    self.stop_all()
                if self.auto_speed.text_flag:
                    text_output = self.auto_speed.text
                    self.auto_speed.text_flag = 0
            elif self.running_task == "spatk":
                ev_value = self.auto_spatk.Ev if self.auto_spatk.Ev < 252 else 252
                if ev_value == 252:
                    self.text_browser.insert(tk.END, f"spatk 努力已满\n")
                    self.stop_all()
                if self.auto_spatk.text_flag:
                    text_output = self.auto_spatk.text
                    self.auto_spatk.text_flag = 0
            elif self.running_task == "attack":
                ev_value = self.auto_attack.Ev if self.auto_attack.Ev < 252 else 252
                if ev_value == 252:
                    self.text_browser.insert(tk.END, f"attack 努力已满\n")
                    self.stop_all()
                if self.auto_attack.text_flag:
                    text_output = self.auto_attack.text
                    self.auto_attack.text_flag = 0

            elif self.running_task == "exp":
                if self.auto_speed.text_flag:
                    text_output = self.auto_speed.text
                    self.auto_speed.text_flag = 0


            self.entry_count.delete(0, tk.END)
            self.entry_count.insert(0, str(ev_value))

            if text_output:
                self.text_browser.insert(tk.END, f"{text_output}\n")

            self.text_browser.see(tk.END)
            time.sleep(1)

    def abandon_skills(self):
        while self.running_task and self.task_flags[self.running_task]:
            if self.instance[self.running_task].skills == 1 and self.abandon_skill_flag.get():  # 检查选择框的状态
                axi = self.instance[self.running_task].find_axis(r"D:\poke32\pokemmo\pic\Map\quxiao.png")
                if axi:
                    self.instance[self.running_task].virtual_keyboard.mouse_move_press(axi[0], axi[1])
                    while not self.instance[self.running_task].find_axis(r"D:\poke32\pokemmo\pic\Map\yes.png"):
                        time.sleep(0.5)
                        self.instance[self.running_task].virtual_keyboard.key_press("F", 0.1)
                        self.text_browser.insert(tk.END, f"技能已放弃\n")
                        break


if __name__ == "__main__":
    app = EffortTrainerApp()
    app.mainloop()
