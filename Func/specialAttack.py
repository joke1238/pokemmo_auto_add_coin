import ctypes
import sys
import time
from pokemmo.utils.findpic import TemplateMatcher
from pokemmo.utils.htscreenshot import WindowCapture
from pokemmo.utils.window import FindHwnd
from pokemmo.Operate.mouse import Virtual_Keyboard


class AutoSpecialAttack:
    def __init__(self):
        _, self.hwnd = FindHwnd()
        self.matcher = TemplateMatcher(self.hwnd)
        self.virtual_keyboard = Virtual_Keyboard()
        self.window_capture = WindowCapture(self.hwnd)
        self.pokeDll = ctypes.CDLL(r'D:\poke32\pokemmo\PokeDLL.dll')
        self.pokeDll.InitInject()
        self.pokeDll.InitInject.restype = ctypes.c_bool
        self.pokeDll.Release.restype = ctypes.c_bool
        self.pokeDll.getX.restype = ctypes.c_int
        self.pokeDll.getY.restype = ctypes.c_int
        self.pokeDll.getMap.restype = ctypes.c_int
        self.pokeDll.getMove.restype = ctypes.c_int
        self.pokeDll.isBatter.restype = ctypes.c_int
        self.text_flag = 0
        self.text = ""
        self.Ev = 0
        self.Map_flag = 0
        self.skills = 0

    def check_shiny(self):
        shutdown_time = time.time() + 1
        while True:
            current_time = time.time()
            if current_time >= shutdown_time:
                self.text = "没有闪光，你个非鬼"
                self.text_flag = 1
                break
            if self.check(path="D:\poke32\pokemmo\pic\diaoyu\shiny.bmp"):
                self.text = "闪光了，滚回来，快！！！！！"
                self.text_flag = 1
                # self.wx.SendMsg("闪光了，滚回来，快！！！！！", '文件传输助手')
                sys.exit(0)

    def check(self, path, Threshold=0.8):
        self.matcher.load_template(path)
        while True:
            if self.matcher.match_template(Threshold):
                return True
            else:
                return False

    def return_pc(self):
        time.sleep(1)
        self.virtual_keyboard.key_press("6", 0.15)

        while True:
            if self.pokeDll.getMap() == 122:
                self.text = "已返回PC"
                self.text_flag = 1
                time.sleep(6)
                self.virtual_keyboard.key_press("F", 0.1)
                self.text = "点击F---1"
                self.text_flag = 1
                self.virtual_keyboard.key_press("F", 0.1)
                self.text = "点击F---2"
                self.text_flag = 1
                self.virtual_keyboard.key_press("F", 0.1)
                self.text = "点击F---3"
                self.text_flag = 1
                break
            else:
                continue
        while True:
            if self.check(r"D:\poke32\pokemmo\pic\shuaji\duihuaa.png"):
                self.text = "对话框出现"
                self.text_flag = 1
                self.virtual_keyboard.key_press("F", 0.15)
                break
            else:
                continue
        while True:
            if self.check(r"D:\poke32\pokemmo\pic\shuaji\duihuaa.png"):
                self.virtual_keyboard.key_press("F", 0.1)
                break
            else:
                continue

        while True:
            if self.check("D:\poke32\pokemmo\pic\diaoyu\pcyes.png"):
                self.virtual_keyboard.key_press("F", 0.1)
                break
            else:
                continue
        while True:
            if self.check(r"D:\poke32\pokemmo\pic\shuaji\duihuaa.png"):
                self.virtual_keyboard.key_press("F", 0.1)
                self.out_pc()
                self.go_fight()
                break

    def out_pc(self):
        time.sleep(1)
        self.matcher.load_template("D:\poke32\pokemmo\pic\diaoyu\pcwai.png")
        self.virtual_keyboard.key_down("S")
        while True:
            coordinate = self.matcher.match_template()
            if coordinate:
                break
        self.virtual_keyboard.key_up("S")

    def main(self):
        if not self.Map_flag:
            self.cheak_Map()
            self.Map_flag = 1

        if self.pokeDll.getMap() == 120:
            self.text = "在医院外前往场地"
            self.text_flag = 1
            self.go_fight()
        if self.pokeDll.getMap() == 122:
            self.text = "在PC前往场地"
            self.text_flag = 1
            self.out_pc()
            self.go_fight()

        if self.pokeDll.getMap() == 92:
            self.text = "已经在场地了"
            self.text_flag = 1

        self.virtual_keyboard.key_press("9", 0.1)
        self.text = "等待战斗界面"
        self.text_flag = 1

        while True:
            if self.check(r"D:\poke32\pokemmo\pic\shuaji\fight.png", 0.8):
                self.text = "战斗界面出现"
                self.text_flag = 1
                self.check_shiny()
                time.sleep(0.1)
                self.virtual_keyboard.key_press("F", 0.15)
                time.sleep(0.1)
                self.virtual_keyboard.key_press("F", 0.15)
                time.sleep(0.1)
                self.virtual_keyboard.key_press("F", 0.15)
                self.skills = 1
                while True:
                    if self.pokeDll.isBatter() == 0:
                        self.Ev += 10
                        self.text = "战斗结束"
                        self.text_flag = 1
                        self.skills = 0
                        break
                break

            if self.check(r"D:\poke32\pokemmo\pic\shuaji\img.png"):
                self.text = "没有足够pp"
                self.text_flag = 1
                time.sleep(0.1)
                self.text = "返回医院"
                self.text_flag = 1
                self.return_pc()
                time.sleep(0.2)

                break

    def move_Y(self, Y):
        if self.pokeDll.getY() > Y:
            self.virtual_keyboard.key_down("W")
            while self.pokeDll.getY() != Y:
                continue
            self.virtual_keyboard.key_up("W")
        elif self.pokeDll.getY() < Y:
            self.virtual_keyboard.key_down("S")
            while self.pokeDll.getY() != Y:
                continue
            self.virtual_keyboard.key_up("S")
        return True

    def move_X(self, X):
        if self.pokeDll.getX() > X:
            self.text = "开始向右移动X轴"
            self.text_flag = 1
            self.virtual_keyboard.key_down("A")
            while self.pokeDll.getX() != X:
                self.text = f"move X: {self.pokeDll.getX()}"
                self.text_flag = 1
            self.virtual_keyboard.key_up("A")
        elif self.pokeDll.getX() < X:
            self.text = "开始向左移动X轴"
            self.text_flag = 1
            self.virtual_keyboard.key_down("D")
            while self.pokeDll.getX() != X:
                self.text = f"move X: {self.pokeDll.getX()}"
                self.text_flag = 1
            self.virtual_keyboard.key_up("D")
        return True

    def go_fight(self):
        time.sleep(1)
        self.virtual_keyboard.key_press("E", 0.15)
        self.move_Y(174)
        self.virtual_keyboard.key_down("A")
        while self.pokeDll.getMap() != 92:
            continue
        self.virtual_keyboard.key_up("A")
        self.move_X(371)
        self.move_Y(179)

    def go_pc(self):
        while True:
            if self.pokeDll.getMap() == 120:
                self.text = "在医院外前往PC"
                self.text_flag = 1
                break

        self.virtual_keyboard.key_down("W")
        while self.pokeDll.getMap() != 122 or self.pokeDll.getY() != 12:
            continue
        self.virtual_keyboard.key_up("W")

        self.text = "已返回PC"
        self.text_flag = 1
        time.sleep(6)
        self.text = "点击F"
        self.text_flag = 1
        self.virtual_keyboard.key_press("F", 0.1)
        self.virtual_keyboard.key_press("F", 0.1)
        self.virtual_keyboard.key_press("F", 0.1)
        while True:
            if self.check(r"D:\\poke32\\pokemmo\\pic\\shuaji\\duihuaa.png"):
                self.text = "对话框出现"
                self.text_flag = 1
                self.virtual_keyboard.key_press("F", 0.15)
                break
        while True:
            if self.check(r"D:\\poke32\\pokemmo\\pic\\shuaji\\duihuaa.png"):
                self.virtual_keyboard.key_press("F", 0.1)
                break
        while True:
            if self.check("D:\\poke32\\pokemmo\\pic\\diaoyu\\pcyes.png"):
                self.virtual_keyboard.key_press("F", 0.1)
                break
        while True:
            if self.check(r"D:\\poke32\\pokemmo\\pic\\shuaji\\duihuaa.png"):
                self.virtual_keyboard.key_press("F", 0.1)
                self.out_pc()
                break

    def cheak_Map(self):
        self.move_map(r"D:\\poke32\\pokemmo\\pic\\Map\\Opelucid.png")
        time.sleep(1)
        self.go_pc()

    def find_axis(self, path, Threshold=0.8):
        self.matcher.load_template(path)
        while True:
            axis = self.matcher.match_template(Threshold)
            if axis:
                return axis
            else:
                return False

    def move_map(self, path):
        self.virtual_keyboard.key_press("1", 0.1)
        time.sleep(0.5)
        while True:
            axi = self.find_axis(path, 0.7)
            if axi:
                self.virtual_keyboard.mouse_move_press_double(axi[0], axi[1])
                self.virtual_keyboard.mouse_move_press_double(axi[0], axi[1])
                self.text = "在医院外前往PC"
                self.text_flag = 1
                break
