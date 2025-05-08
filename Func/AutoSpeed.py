import ctypes
import sys
import time
import win32con
import win32gui
from pokemmo.utils.findpic import TemplateMatcher
from pokemmo.utils.htscreenshot import WindowCapture
from pokemmo.utils.window import FindHwnd
from pokemmo.Operate.mouse import Virtual_Keyboard


class AutoSpeed:
    def __init__(self):
        self.Map_flag = 0
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
        self.text = ""
        self.text_flag = 0
        self.Ev = 0
        self.skills = 0

    def check_shiny(self):
        shutdown_time = time.time() + 1
        while True:
            if time.time() >= shutdown_time:
                self.text = "没有闪光，你个非鬼"
                self.text_flag = 1
                break
            if self.check(path="D:\\poke32\\pokemmo\\pic\\diaoyu\\shiny.bmp"):
                self.text = "闪光了，滚回来，快！！！！！"
                self.text_flag = 1
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
            if self.pokeDll.getMap() == 151:
                self.text = "以返回PC"
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
                self.go_fight()
                break

    def out_pc(self):

        self.virtual_keyboard.key_down("S")
        while self.pokeDll.getMap() != 150:
            continue
        self.virtual_keyboard.key_up("S")

    def main(self):
        if not self.Map_flag:
            self.cheak_Map()
            self.Map_flag = 1

        if self.pokeDll.getMap() == 151:
            self.text = "在151PC前往场地"
            self.text_flag = 1
            self.out_pc()
            self.go_fight()

        if self.pokeDll.getMap() == 150:
            self.text = "在150地图前往场地"
            self.text_flag = 1
            self.go_fight()

        if self.pokeDll.getMap() == 112:
            self.text = "已经在122场地"
            self.text_flag = 1

        self.virtual_keyboard.key_press("9", 0.1)
        self.text = "等待战斗界面"
        self.text_flag = 1

        while True:
            if self.check(r"D:\\poke32\\pokemmo\\pic\\shuaji\\fight.png", 0.8):
                self.text = "战斗界面出现"
                self.text_flag = 1
                self.check_shiny()
                time.sleep(0.1)
                self.virtual_keyboard.key_press("F", 0.15)
                self.virtual_keyboard.key_press("F", 0.15)
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

            if self.check(r"D:\\poke32\\pokemmo\\pic\\shuaji\\img.png"):
                self.text = "没有足够pp，返回医院"
                self.text_flag = 1
                time.sleep(0.1)
                self.return_pc()
                time.sleep(0.2)
                break

    def go_fight(self):
        if self.pokeDll.getMap() == 150:
            time.sleep(2)
            self.virtual_keyboard.key_press("E", 0.1)
            self.virtual_keyboard.key_down("A")
            while self.pokeDll.getX() != 624:
                continue
            self.virtual_keyboard.key_up("A")
            self.virtual_keyboard.key_down("W")
            while self.pokeDll.getY() != 184:
                continue
            self.virtual_keyboard.key_up("W")
            self.text = "到达位置"
            self.text_flag = 1

    def check_fight(self):
        while True:
            if self.check(r"D:\\poke32\\pokemmo\\pic\\shuaji\\img_10.png", 0.7):
                self.text = "战斗结束"
                self.text_flag = 1
                break

    def close_window(self):
        try:
            win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
            self.text = "窗口已关闭"
            self.text_flag = 1
        except Exception as e:
            self.text = f"关闭窗口失败: {e}"
            self.text_flag = 1

    def go_pc(self):
        while True:
            if self.pokeDll.getMap() == 150:
                self.text = "在医院外前往PC"
                self.text_flag = 1
                break

        self.virtual_keyboard.key_down("W")
        while self.pokeDll.getMap() != 151 or self.pokeDll.getY() != 12:
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

        self.move_map(r"D:\\poke32\\pokemmo\\pic\\Map\\Lacunosa.png")
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
                break


if __name__ == '__main__':
    auto_speed = AutoSpeed()
    auto_speed.cheak_Map()