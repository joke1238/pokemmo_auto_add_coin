import ctypes
import json
import os
import sys
import time
import win32con
import win32gui
from pokemmo.utils.findpic import TemplateMatcher
from pokemmo.utils.htscreenshot import WindowCapture
from pokemmo.utils.window import FindHwnd
from pokemmo.Operate.mouse import Virtual_Keyboard
import requests

def get_resource_path(relative_path):
    """获取资源文件路径，支持打包后运行"""
    return os.path.join(os.path.abspath("."), relative_path)

class Add_Gold:
    def __init__(self):
        _,self.hwnd = FindHwnd()
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
        self.gold = 0
        self.paw = 0
        self.aroma = 0
        self.text_pc = ""
        self.text_pc_flag = 0
        self.text_poke = ""
        self.text_poke_flag = 0
        self.text_move = ""
        self.text_move_flag = 0
        self.move_flag = 0
        with open(get_resource_path(r"config.json"), "r") as f:
            self.config = json.load(f)



    def check_aware(self):
        shutdown_time = time.time() + 3
        while True:
            current_time = time.time()
            if current_time >= shutdown_time:
                return False
            if self.check(path=get_resource_path(R"gold\paw.png"), Threshold=0.55):
                self.text_move = "🐾 感知了1，快！！！！！"

                return True
            if self.check(path=get_resource_path(R"gold\new_paw.png"), Threshold=0.91):
                self.text_move ="🐾 感知了2，快！！！！！"

                return True

    def check(self, path, Threshold=0.8):
        self.matcher.load_template(path)
        while True:
            if self.matcher.match_template(Threshold):
                return True
            else:
                return False

    def find_axis(self,path,Threshold=0.8):
        self.matcher.load_template(path)
        axis = self.matcher.match_template(Threshold)
        if axis:
            return axis
        else:
            return False

    def return_pc(self):
        self.text_move = "开始检测返回1"
        self.text_move_flag = 1
        self.move_flag = 1
        self.virtual_keyboard.key_press(self.config["key"]["bicycle_key"], 0.15)
        self.move_Y(69)
        self.move_X(11)
        self.move_Y(66)
        self.move_X(13)
        self.move_Y(60)
        self.move_X(15)
        self.move_flag = 0
        self.text_move = "返回1检测结束"
        self.text_move_flag = 1
        self.virtual_keyboard.key_down(self.config["key"]["up_key"])
        while self.pokeDll.getMap() != 2:
            continue
        self.text_move = "开始检测返回2"
        self.text_move_flag = 1
        self.move_flag = 1
        self.virtual_keyboard.key_up(self.config["key"]["up_key"])
        self.move_Y(20)
        self.move_X(21)
        self.move_Y(9)
        self.move_X(13)
        self.move_Y(13)
        self.move_flag = 0
        self.text_move = "返回2检测结束"
        self.text_move_flag = 1
        while True:
            if self.check(get_resource_path(r"gold\sanjiao.png"), 0.75):
                self.text_pc ="▲检测到三角▲"
                self.text_pc_flag = 1
                time.sleep(0.13)
                self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)
                time.sleep(2)
                break

        while True:
            if self.check(get_resource_path(r"gold\sanjiao.png"), 0.74):
                self.text_pc = "▲检测到三角▲"
                self.text_pc_flag = 1
                time.sleep(1)
                self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)
                self.text_pc = "▲检测到三角▲"
                self.text_pc_flag = 1

                break

        time.sleep(3)

        while True:
            self.matcher.load_template(get_resource_path(r"gold\niula.png"))
            zuobiao = self.matcher.match_template(0.7)
            if zuobiao:
                self.text_pc = "检測到玛狃ラ"
                self.text_pc_flag = 1
                self.virtual_keyboard.mouse_move_press(zuobiao[0], zuobiao[1])
                while True:
                    self.matcher.load_template(get_resource_path(r"gold\wd.png"))
                    zuobiao = self.matcher.match_template(0.7)
                    if zuobiao:
                        self.text_pc = "检测到挖洞"
                        self.text_pc_flag = 1
                        self.virtual_keyboard.mouse_move_press(zuobiao[0], zuobiao[1])

                        self.out_pc()
                        break
                break

    def out_pc(self):
        time.sleep(1)
        while True:
            if self.check(get_resource_path(r"gold\pcwai.png"), 0.7):
                self.text_pc = "🚪 出pc了"
                self.text_pc_flag = 1
                time.sleep(0.14)
                self.virtual_keyboard.key_press(self.config["key"]["bicycle_key"], 0.15)
                self.text_move = "离开检测开始"
                self.text_move_flag = 1
                self.move_flag = 1
                self.move_Y(61)
                self.move_X(13)
                self.move_Y(67)
                self.move_X(10)
                self.move_Y(70)
                self.move_X(8)
                self.move_Y(83)
                self.move_flag = 0
                self.text_move = "离开检测结束"
                self.text_move_flag = 1
                break

    def main(self):

        self.virtual_keyboard.key_press(self.config["key"]["sweet_key"], 0.2)
        self.text_move = "⌛ 等待战斗界面 ⌛"
        self.text_move_flag = 1

        while True:
            if self.check(get_resource_path(r"gold\fight.png"), 0.7):
                self.text_move ="⚔️に戦闘界面出现⚔️"
                self.aroma += 1


                if self.check_poke():
                    if self.check_aware():

                        self.text_move = "🐾 感知了，使用封印"

                        time.sleep(0.15)
                        self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)
                        time.sleep(0.15)
                        self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)
                        time.sleep(0.15)
                        self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)
                        while True:
                            if self.check(get_resource_path(r"gold\fight.png"), 0.7):
                                self.text_move = "⚔️に戦闘界面出现⚔️"

                                time.sleep(0.3)
                                self.virtual_keyboard.key_press(self.config["key"]["down_key"], 0.15)
                                time.sleep(0.3)
                                self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)
                                time.sleep(0.3)
                                self.virtual_keyboard.key_press(self.config["key"]["right_key"], 0.15)
                                time.sleep(0.3)
                                self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)
                                while True:
                                    if self.check(r"D:\poke32\pokemmo\pic\gold\fight.png", 0.7):
                                        self.text_move = "⚔️に戦闘界面出现⚔️"

                                        time.sleep(0.15)
                                        self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)
                                        time.sleep(0.15)
                                        self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)
                                        time.sleep(0.15)
                                        self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)
                                        self.flag = 1
                                        break
                                break

                    else:
                        time.sleep(0.15)
                        self.virtual_keyboard.key_press(self.config["key"]["down_key"], 0.15)
                        time.sleep(0.15)
                        self.virtual_keyboard.key_press(self.config["key"]["right_key"], 0.15)
                        time.sleep(0.15)
                        self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)

                    while True:
                        if self.pokeDll.isBatter() == 0:
                            break

                        # if self.check(r"D:\poke32\pokemmo\pic\shuaji\img_20.png", 0.65):
                        #     self.text_poke ="检测到对话 战斗结束")
                        #     break
                        # if self.check(r"D:\poke32\pokemmo\pic\shuaji\img_19.png", 0.75):
                        #     self.text_poke ="检测到草丛 战斗结束")
                        #     break

                    if self.flag == 1:
                        self.removeTheProps()
                    break

                else:
                    time.sleep(0.15)
                    self.virtual_keyboard.key_press(self.config["key"]["down_key"], 0.15)
                    time.sleep(0.15)
                    self.virtual_keyboard.key_press(self.config["key"]["right_key"], 0.15)
                    time.sleep(0.15)
                    self.virtual_keyboard.key_press(self.config["key"]["A_key"], 0.15)
                    while True:
                        if self.pokeDll.isBatter() == 0:
                            break

                        # if self.check(r"D:\poke32\pokemmo\pic\shuaji\img_20.png", 0.65):
                        #     self.text_poke ="检测到对话 战斗结束")
                        #     break
                        # if self.check(r"D:\poke32\pokemmo\pic\shuaji\img_19.png", 0.75):
                        #     self.text_poke ="检测到草丛 战斗结束")
                        #     break
                    break

            if self.check(get_resource_path(r"gold\img_3.png")):
                self.text_pc ="PP不足"
                self.text_pc_flag = 1
                time.sleep(0.1)
                self.text_pc = "回医院"
                self.text_pc_flag = 1
                self.return_pc()
                time.sleep(0.2)
                break

    def move_Y(self, Y):
        if self.pokeDll.getY() > Y:
            self.virtual_keyboard.key_down(self.config["key"]["up_key"])
            while self.pokeDll.getY() != Y:
                continue
            self.virtual_keyboard.key_up(self.config["key"]["up_key"])
        elif self.pokeDll.getY() < Y:
            self.virtual_keyboard.key_down(self.config["key"]["down_key"])
            while self.pokeDll.getY() != Y:
                continue
            self.virtual_keyboard.key_up(self.config["key"]["down_key"])
        return True



    def move_X(self, X):
        if self.pokeDll.getX() > X:
            self.virtual_keyboard.key_down(self.config["key"]["left_key"])
            while self.pokeDll.getX() != X:
                continue
            self.virtual_keyboard.key_up(self.config["key"]["left_key"])
        elif self.pokeDll.getX() < X:
            self.virtual_keyboard.key_down(self.config["key"]["right_key"])
            while self.pokeDll.getX() != X:
                continue
            self.virtual_keyboard.key_up(self.config["key"]["right_key"])
        return True

    def removeTheProps(self):
        self.text_move = "移除道具"

        while True:
            self.matcher.load_template(get_resource_path(r"gold\img_1.png"))
            zuobiao = self.matcher.match_template(0.7)
            if zuobiao:
                self.text_move = "检测到精灵"

                self.virtual_keyboard.mouse_move_press(zuobiao[0], zuobiao[1])
                time.sleep(0.15)
                while True:
                    axis_gold = self.find_axis(get_resource_path(r"gold\gold.png"), 0.7)
                    axis_paw = self.find_axis(get_resource_path(r"gold\remove.png"), 0.7)
                    if axis_gold:
                        self.text_move = "检测到金币"
                        self.text_move_flag = 1
                        self.gold += 1
                        self.virtual_keyboard.mouse_move_press(axis_gold[0], axis_gold[1])
                        self.flag = 0
                        break
                    if axis_paw:
                        self.text_move = "检测到爪子"
                        self.text_move_flag = 1
                        self.paw += 1
                        self.virtual_keyboard.mouse_move_press(axis_paw[0], axis_paw[1])
                        self.flag = 0
                        break
                break

                # 如果在循环外部需要继续执行其他操作，可以取消break语句并添加适当的退出条件

    def get_shiny(self, code):
        url = f"http://miaotixing.com/trigger?id={code}"
        requests.get(url)

    def check_poke(self):
        while True:
            result = {
                "shiny": False,
                "喵喵": False,
                "小火马": False,
                "呆呆": False,
                "老大": False,
                "烈焰马": False,
                "可达鸭": False,
                "傻鸟": False
            }

            # 一次性检查所有图像
            if self.check(get_resource_path(r"gold\shiny.bmp"), 0.65):
                result["shiny"] = True
            if self.check(get_resource_path(r"gold\miaomiao.png"), 0.7):
                result["喵喵"] = True
            if self.check(get_resource_path(r"gold\huoma.png"), 0.7):
                result["小火马"] = True
            if self.check(get_resource_path(r"gold\daidai.png"), 0.7):
                result["呆呆"] = True
            if self.check(get_resource_path(r"gold\laoda.png"), 0.7):
                result["老大"] = True
            if self.check(get_resource_path(r"gold\lieyan.png"), 0.7):
                result["烈焰马"] = True
            if self.check(get_resource_path(r"gold\duck.png"), 0.7):
                result["可达鸭"] = True
            if self.check(get_resource_path(r"gold\sb.png"), 0.7):
                result["傻鸟"] = True

            # 优先处理闪光
            if result["shiny"]:
                self.text_poke ="✨ 检测到闪光宝可梦！ ✨"
                self.text_poke_flag = 1
                self.get_shiny("tmfrnH4")

                sys.exit(0)

            # 没有闪光，处理其他宝可梦（优先喵喵）
            if result["喵喵"]:
                self.text_poke ="🐱 检测到喵喵！ 🐱"
                self.text_poke_flag = 1
                return True
            elif result["小火马"]:
                self.text_poke ="🔥 检测到小火马！🔥"
                self.text_poke_flag = 1
                return False
            elif result["呆呆"]:
                self.text_poke ="🐻 检测到呆呆！ 🐻"
                self.text_poke_flag = 1
                return False
            elif result["老大"]:
                self.text_poke ="👑 检测到老大！ 👑"
                self.text_poke_flag = 1
                return False
            elif result["烈焰马"]:
                self.text_poke ="🔥 检测到烈焰马！ 🔥"
                self.text_poke_flag = 1
                return False
            elif result["可达鸭"]:
                self.text_poke ="🦆 检測到可达鸭！ 🦆"
                self.text_poke_flag = 1
                return False
            elif result["傻鸟"]:
                self.text_poke ="🐦 检測到傻鸟！ 🐦"
                self.text_poke_flag = 1
                return False

    def close_window(self):
        if self.hwnd is not None:
            win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
        else:
            raise ValueError("窗口句柄无效")


if __name__ == '__main__':
    print(get_resource_path(r"gold\shiny.bmp"))
