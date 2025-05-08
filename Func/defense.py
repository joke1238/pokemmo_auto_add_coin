import ctypes
import sys
import time
import pygame
from pokemmo.utils.findpic import TemplateMatcher
from pokemmo.utils.htscreenshot import WindowCapture
from pokemmo.utils.window import FindHwnd
from pokemmo.Operate.mouse import Virtual_Keyboard





class Shuaji:
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
        self.flag = 0
        # 初始化pygame mixer模块
        pygame.mixer.init()


    def check_shiny(self):
        shutdown_time = time.time() + 1
        while True:
            current_time = time.time()
            if current_time >= shutdown_time:
                print("没有闪光，你个非鬼")
                break
            if self.check(path="D:\poke32\pokemmo\pic\diaoyu\shiny.bmp"):
                print("闪光了，滚回来，快！！！！！")
                # self.wx.SendMsg("闪光了，滚回来，快！！！！！", '文件传输助手')
                sys.exit(0)



    def check(self,path,Threshold=0.8):
        self.matcher.load_template(path)
        while True:
            if self.matcher.match_template(Threshold):
                return True
            else:
                return False

    def return_pc(self):
        self.virtual_keyboard.key_down("S")
        while self.pokeDll.getMap() != 214:
            continue
        self.virtual_keyboard.key_up("S")
        time.sleep(1)
        self.virtual_keyboard.key_press("6", 0.15)

        while True:
            if self.pokeDll.getMap() == 146:
                print("以返回PC")
                time.sleep(6)
                self.virtual_keyboard.key_press("F", 0.1)
                print("点击F---1")
                self.virtual_keyboard.key_press("F", 0.1)
                print("点击F---2")
                self.virtual_keyboard.key_press("F", 0.1)
                print("点击F---3")
                break
            else:
                continue
        while True:
            if self.check(r"D:\poke32\pokemmo\pic\shuaji\duihuaa.png"):
                print("对话框出现")
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
        self.virtual_keyboard.key_down("S")
        while self.pokeDll.getMap() != 136:
            continue
        self.virtual_keyboard.key_up("S")


    def main(self):
        if self.pokeDll.getMap() == 146:
            print("在医院外前往场地")
            self.go_fight()

        if self.pokeDll.getMap() == 222:
            time.sleep(4)
            print("已经在场地了")


        self.virtual_keyboard.key_press("9", 0.1)
        print("等待战斗界面")

        while True:
            if self.check(r"D:\poke32\pokemmo\pic\shuaji\fight.png",0.8):
                print("战斗界面出现")
                self.check_shiny()
                time.sleep(0.1)
                self.virtual_keyboard.key_press("F", 0.15)
                time.sleep(0.1)
                self.virtual_keyboard.key_press("F", 0.15)
                time.sleep(0.1)
                self.virtual_keyboard.key_press("F", 0.15)
                while True:
                    if self.pokeDll.isBatter() ==  0:
                        break
                break

            if self.check(r"D:\poke32\pokemmo\pic\shuaji\img.png"):
                print("没有足够pp")
                time.sleep(0.1)
                print("返回医院")
                self.return_pc()
                time.sleep(0.2)

                break


    def move_Y(self,Y):
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
            print("开始向右移动X轴")
            self.virtual_keyboard.key_down("A")
            while self.pokeDll.getX() != X:
                print("move X:", self.pokeDll.getX())

            self.virtual_keyboard.key_up("A")
        elif self.pokeDll.getX() < X:
            print("开始向左移动X轴")
            self.virtual_keyboard.key_down("D")
            while self.pokeDll.getX() != X:
                print("move X:", self.pokeDll.getX())

            self.virtual_keyboard.key_up("D")
        return True

    def go_fight(self):
        time.sleep(1)
        self.virtual_keyboard.key_press("E", 0.15)
        self.move_Y(53)
        self.move_X(32)
        self.virtual_keyboard.key_down("S")
        while self.pokeDll.getMap() != 214:
            continue
        self.virtual_keyboard.key_up("S")
        self.move_Y(0)
        self.virtual_keyboard.key_down("A")
        while self.pokeDll.getX() != 5:
            continue
        self.virtual_keyboard.key_up("A")
        self.virtual_keyboard.key_down("S")
        while self.pokeDll.getY() != -5:
            continue
        self.virtual_keyboard.key_up("S")
        self.move_X(7)
        self.virtual_keyboard.key_down("W")
        while self.pokeDll.getMap() != 222:
            continue
        self.virtual_keyboard.key_up("W")
        print("到达战斗地点")








if __name__ == '__main__':
    shuaji = Shuaji()
    time.sleep(4)
    # shuaji.go_fight()

    while True:
        shuaji.main()
