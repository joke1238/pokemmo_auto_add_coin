import ctypes
import sys
import time
from pokemmo.utils.findpic import TemplateMatcher
from pokemmo.utils.htscreenshot import WindowCapture
from pokemmo.utils.window import FindHwnd
from pokemmo.Operate.mouse import Virtual_Keyboard





class Shuaji:
    def __init__(self):
        _,self.hwnd = FindHwnd()
        self.matcher = TemplateMatcher(self.hwnd)
        self.virtual_keyboard = Virtual_Keyboard()
        self.window_capture = WindowCapture(self.hwnd)
        self.pokeDll = ctypes.CDLL(r'./PokeDLL.dll')
        self.pokeDll.InitInject.restype = ctypes.c_bool
        self.pokeDll.Release.restype = ctypes.c_bool
        self.pokeDll.getX.restype = ctypes.c_int
        self.pokeDll.getY.restype = ctypes.c_int
        self.pokeDll.getMap.restype = ctypes.c_int
        self.pokeDll.getToward.restype = ctypes.c_int
        self.pokeDll.getRegion.restype = ctypes.c_int
        self.pokeDll.getMove.restype = ctypes.c_int
        self.pokeDll.getRun.restype = ctypes.c_int
        self.pokeDll.getMoveType.restype = ctypes.c_int
        self.pokeDll.isBatter.restype = ctypes.c_bool
        self.pokeDll.isTalk.restype = ctypes.c_bool


    def move_X(self,X):
        if self.pokeDll.getX() > X:
            print("开始向右移动X轴")
            self.virtual_keyboard.key_down("A")
            while self.pokeDll.getX() != X:
                print("move X:",self.pokeDll.getX())

            self.virtual_keyboard.key_up("A")
        elif self.pokeDll.getX() < X:
            print("开始向左移动X轴")
            self.virtual_keyboard.key_down("D")
            while self.pokeDll.getX() != X:
                print("move X:", self.pokeDll.getX())

            self.virtual_keyboard.key_up("D")
        return True

    def return_pc(self):
        time.sleep(5)
        self.virtual_keyboard.key_press("6", 0.15)

        while True:
            if self.check("D:\poke32\pokemmo\pic\diaoyu\pcnei.png",0.7):
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
            if self.check("D:\poke32\pokemmo\pic\shuaji\duihuaa.png"):
                print("对话框出现")
                self.virtual_keyboard.key_press("F", 0.15)
                break
            else:
                continue
        while True:
            if self.check("D:\poke32\pokemmo\pic\shuaji\duihuaa.png"):
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
            if self.check("D:\poke32\pokemmo\pic\shuaji\duihuaa.png"):
                self.virtual_keyboard.key_press("F", 0.1)
                self.out_pc()
                self.go_fight()
                break
            else:
                continue

    def out_pc(self):
        time.sleep(1)
        self.matcher.load_template("D:\poke32\pokemmo\pic\diaoyu\pcwai.png")
        self.virtual_keyboard.key_down("S")
        while True:
            coordinate = self.matcher.match_template()
            if coordinate:
                break
        self.virtual_keyboard.key_up("S")

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

    import time

    def move_battle(self):
        max_wait_time = 2  # 最大等待时间，防止卡死

        while True:
            if self.pokeDll.getY() - 147 > 158 - self.pokeDll.getY():
                target_Y = 147
            else:
                target_Y = 158

            if self.pokeDll.getY() > target_Y:
                print(f"开始向下移动到 {target_Y}")
                self.virtual_keyboard.key_down("W")
            else:
                print(f"开始向上移动到 {target_Y}")
                self.virtual_keyboard.key_down("S")

            start_time = time.time()  # 记录开始时间

            while self.pokeDll.getY() != target_Y:
                before_y = self.pokeDll.getY()

                # **轮询检测，不使用长 sleep**
                for _ in range(10):  # 10次快速检测，代替 sleep
                    time.sleep(0.05)  # 50ms
                    if self.pokeDll.getY() != before_y:  # 位置发生变化，继续
                        break

                # **战斗检测**
                if before_y == self.pokeDll.getY() and self.pokeDll.isBatter():
                    print("检测到战斗，暂停移动")
                    self.virtual_keyboard.key_up("W")
                    self.virtual_keyboard.key_up("S")
                    return True

                # **超时检测**
                if time.time() - start_time > max_wait_time:
                    print(f"移动超时，目标 {target_Y} 未达成，强制停止")
                    self.virtual_keyboard.key_up("W")
                    self.virtual_keyboard.key_up("S")
                    return False

            print(f"成功移动到 {target_Y}")
            self.virtual_keyboard.key_up("W")
            self.virtual_keyboard.key_up("S")

    def go_fight(self):
        time.sleep(3)
        self.virtual_keyboard.key_press("E", 0.15)
        self.move_X(179)
        self.move_Y(167)
        self.move_X(177)
        self.move_Y(158)
        print("go end !!!!")

    def check_PP(self):
        start_time = time.time()
        while time.time() - start_time < 2:
            if self.check("D:\poke32\pokemmo\Func\img.png",0.74):
                time.sleep(0.1)
                self.virtual_keyboard.key_press("C", 0.15)
                time.sleep(0.1)
                self.virtual_keyboard.key_press("S", 0.15)
                time.sleep(0.1)
                self.virtual_keyboard.key_press("D", 0.15)
                time.sleep(0.1)
                self.virtual_keyboard.key_press("F", 0.15)
                return True
            time.sleep(0.1)  # 短暂等待，减少CPU占用
        return False


    def check(self, path, Threshold=0.8):
        self.matcher.load_template(path)
        while True:
            if self.matcher.match_template(Threshold):
                return True
            else:
                return False


    def check_fight(self):
        before_y = self.pokeDll.getY()
        self.virtual_keyboard.key_down("W")
        time.sleep(0.2)
        self.virtual_keyboard.key_up("W")
        if before_y == self.pokeDll.getY():
            return False
        else:
            print("检测到战斗结束")
            return True




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


    def main(self):
        while True:
            print("新的一轮")
            self.move_battle()
            print("等待战斗界面")
            while True:
                if self.check(r"D:\poke32\pokemmo\pic\shuaji\fight.png", 0.8):
                    print("战斗界面出现")
                    self.check_shiny()
                    time.sleep(0.1)
                    self.virtual_keyboard.key_press("F", 0.15)
                    if self.check_PP():
                        print("检测到PP为0")
                        self.return_pc()
                        break
                    time.sleep(0.1)
                    self.virtual_keyboard.key_press("F", 0.15)
                    time.sleep(0.1)
                    self.virtual_keyboard.key_press("F", 0.15)
                    while True:
                        if self.check_fight():
                            break
                        if self.check(r"D:\poke32\pokemmo\pic\shuaji\fight.png",0.8):
                            self.virtual_keyboard.key_press("F", 0.15)
                            if self.check_PP():
                                print("检测到PP为0")
                                self.return_pc()
                                break
                            time.sleep(0.1)
                            self.virtual_keyboard.key_press("D", 0.15)
                            time.sleep(0.1)
                            self.virtual_keyboard.key_press("F", 0.15)
                            time.sleep(0.1)
                            self.virtual_keyboard.key_press("F", 0.15)
                    break





if __name__ == '__main__':
    shuaji = Shuaji()
    time.sleep(2)
    shuaji.main()