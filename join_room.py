import sys
import time
import pyautogui
import pygetwindow as gw

platform = sys.platform.lower()


class GlobalContainer:
    global_variable = None

def set_global_variable(value):
    GlobalContainer.global_variable = value

def get_global_variable():
    return GlobalContainer.global_variable


def callback(result):
    print(result)

window = None
def send_error(window, message):
    window.evaluate_js(f"showError('{message}');", callback)


if platform.startswith("win"):
    import ctypes
    import win32gui

    def showError(message):
        print(message)
        window = get_global_variable()
        send_error(window, message)
        set_global_variable(window)
        
        ctypes.windll.user32.MessageBoxW(None, message, "JigglyConnect Error", 0)

    def focus_yuzu():
        found = False
        windows = gw.getAllWindows()

        for window in windows:
            title = window.title.lower()
            if "yuzu" in title and "installer" not in title:
                if "smash" not in title:
                    showError("SSBU is not launched!")
                    return False
                if "13.0." not in title:
                    showError("Please update your game! Only 13.0.1 is supported.")
                    return False
                found = True
                window.activate()  # Focus window
                win32gui.ShowWindow(window._hWnd, 9)  # Restore window if minimized
                break

        if not found:
            showError("Yuzu window not found")
            return False

        return True

    def macro(ip, port, username, password):
        pyautogui.press("esc")
        pyautogui.hotkey("ctrl", "c")

        window_rect = pyautogui.getActiveWindow()
        click_x = window_rect.left + window_rect.width // 2
        click_y = window_rect.top + 50

        pyautogui.click(click_x, click_y)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.write(ip)
        pyautogui.press("tab")
        pyautogui.write(port)
        pyautogui.press("tab")
        pyautogui.write(username)
        pyautogui.press("tab")
        pyautogui.write(password)
        pyautogui.press("tab")
        pyautogui.press("enter")
        pyautogui.press("enter")
        pyautogui.press("enter")


    cooldown_timestamp = 0

    def join_room(ip, port, username, password):
        global cooldown_timestamp

        current_timestamp = time.time()
        if not current_timestamp >= cooldown_timestamp:
            print("cooldown")
        else:
            cooldown_timestamp = current_timestamp + 10

            result = focus_yuzu()
            if result == True:
                time.sleep(0.5)
                macro(ip, str(port), username, password)

            print("Room joined")


if __name__ == "__main__":
    # test
    join_room("74.47.74.47", 35008, "usérname", "password :3")
