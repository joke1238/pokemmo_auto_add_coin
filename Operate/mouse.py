import time
import win32api
import win32con
import win32gui

class Virtual_Keyboard:
    def __init__(self):
        self.hwnd = win32gui.FindWindow("GLFW30", None)
        if self.hwnd == 0:
            raise RuntimeError("未找到 PokeMMO 窗口，请确保游戏正在运行。")

        print(f"窗口句柄: {self.hwnd}, 窗口标题: POKÉMON MMO")

        self.vlaue_key = {
            "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70,
            "G": 71, "H": 72, "I": 73, "J": 74, "K": 75, "L": 76,
            "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82,
            "S": 83, "T": 84, "U": 85, "V": 86, "W": 87, "X": 88,
            "Y": 89, "Z": 90,
            "0": 48, "1": 49, "2": 50, "3": 51, "4": 52,
            "5": 53, "6": 54, "7": 55, "8": 56, "9": 57,
            "F1": 112, "F2": 113, "F3": 114, "F4": 115, "F5": 116,
            "F6": 117, "F7": 118, "F8": 119, "F9": 120, "F10": 121,
            "F11": 122, "F12": 123,
            "TAB": 9, "ALT": 18, "ENTER": 13
        }


    def key_press(self, key: str, interval=0.1):
        key = key.upper()
        if key not in self.vlaue_key:
            print(f"[警告] 无效按键: {key}")
            return
        key_num = self.vlaue_key[key]
        scan_code = win32api.MapVirtualKey(key_num, 0)
        dparam = 1 | (scan_code << 16)
        uparam = dparam | (1 << 30) | (1 << 31)

        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, key_num, dparam)
        time.sleep(interval)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, key_num, uparam)

    def key_down(self, key: str):
        key = key.upper()
        if key not in self.vlaue_key:
            return
        key_num = self.vlaue_key[key]
        scan_code = win32api.MapVirtualKey(key_num, 0)
        dparam = 1 | (scan_code << 16)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, key_num, dparam)

    def key_up(self, key: str):
        key = key.upper()
        if key not in self.vlaue_key:
            return
        key_num = self.vlaue_key[key]
        scan_code = win32api.MapVirtualKey(key_num, 0)
        uparam = 1 | (scan_code << 16) | (1 << 30) | (1 << 31)

        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, key_num, uparam)

    def mouse_move(self, x, y):
        point = win32api.MAKELONG(int(x), int(y))
        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, None, point)

    def mouse_down(self, x, y, button="L"):
        point = win32api.MAKELONG(int(x), int(y))
        button = button.upper()
        if button == "L":
            win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, point)
        elif button == "R":
            win32api.SendMessage(self.hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, point)

    def mouse_up(self, x, y, button="L"):
        point = win32api.MAKELONG(int(x), int(y))
        button = button.upper()
        if button == "L":
            win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, point)
        elif button == "R":
            win32api.SendMessage(self.hwnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, point)

    def mouse_double(self, x, y):
        point = win32api.MAKELONG(int(x), int(y))
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDBLCLK, win32con.MK_LBUTTON, point)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, point)

    def mouse_move_press(self, x, y):
        point = win32api.MAKELONG(int(x), int(y))
        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, None, point)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, point)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, point)

    def mouse_move_press_double(self, x, y):
        point = win32api.MAKELONG(int(x), int(y))
        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, None, point)
        time.sleep(1)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, point)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, point)


if __name__ == '__main__':
    keyboard = Virtual_Keyboard()
    # keyboard.key_press("E")
    keyboard.key_down("A")

    # keyboard.mouse_move(100, 100)s