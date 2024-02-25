import sys
import time
import pyautogui
import pygetwindow as gw
import tkinter as tk
from tkinter import messagebox

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
def send_error(message):
    print(message)
    window = get_global_variable()
    window.evaluate_js(f"showError('{message}');", callback)
    focus_webview()
    set_global_variable(window)

def send_info(message):
    print(message)
    window = get_global_variable()
    window.evaluate_js(f"showInfo('{message}');", callback)
    focus_webview()
    set_global_variable(window)


if platform.startswith("win"):
    import ctypes
    import win32gui

    def showError(message):
        ctypes.windll.user32.MessageBoxW(None, message, "JigglyConnect Error", 0)

    def yuzu_ready():
        found = False
        windows = gw.getAllWindows()

        for window in windows:
            title = window.title.lower()
            if "yuzu" in title and "installer" not in title:
                if "smash" not in title:
                    send_error("SSBU is not launched!")
                    return False
                if "13.0." not in title:
                    send_error("Please update your game! Only 13.0.1 and 13.0.2 are supported.")
                    return False
                yuzu_window = window
                found = True
                break

        if not found:
            send_error("Yuzu doesn&#39;t seem to be launched.")
            return False

        return yuzu_window

    def focus_yuzu_window():
        yuzu_window = yuzu_ready()
        if yuzu_window != False:
            try:
                yuzu_window.activate()  # Focus window
            except gw.PyGetWindowException:
                pass
            win32gui.ShowWindow(yuzu_window._hWnd, 9)  # Restore window if minimized
            
            return True
        return False
    
    def focus_yuzu():
        print('1')
        if not 'yuzu' in gw.getActiveWindow().title.lower():
            print('2')
            windows = gw.getAllWindows()

            for window in windows:
                title = window.title.lower()
                if "yuzu" in title and not "yuzu 1" in title:
                    try:
                        window.activate()  # Focus window
                    except gw.PyGetWindowException:
                        pass
                    win32gui.ShowWindow(window._hWnd, 9)  # Restore window if minimized
                    pyautogui.press("esc")
            return focus_yuzu_window()
                        
        return True
    
    def focus_webview():
        windows = gw.getAllWindows()

        for window in windows:
            title = window.title.lower()
            if "JigglyConnect" in title and not "[" in title:
                try:
                    window.activate()  # Focus window
                except gw.PyGetWindowException:
                    pass
                win32gui.ShowWindow(window._hWnd, 9)  # Restore window if minimized
                break
    
    def check_room_status():
        return any(
            "[jigglyconnect] matchmaking" in window.title.lower()
            for window in gw.getAllWindows()
        )
    
    def handle_room_failed(ip, port, username, password):
        fenetre = tk.Tk()
        fenetre.withdraw()
        answer = messagebox.askyesno("Failed to join the room.", "Retry?")
        
        if answer:
            if focus_yuzu() == True:
                time.sleep(0.5)
                macro(ip, str(port), username, password)

                print("Room joined")
            else:
                print("Failed to join room")
        else:
            send_info(
                f" Go on Yuzu -> Ctrl+C, and then enter:<BR><BR>Adress: {ip}<BR>Port: {port}<BR>Password: {password}<BR>"
            )
    
    
    def macro(ip, port, username, password):
        pyautogui.press("esc")
        pyautogui.press("esc")
        pyautogui.press("esc")
        time.sleep(0.1)
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
        
        time.sleep(0.1)
        if not check_room_status():
            print('room not joined!')
            handle_room_failed(ip, port, username, password)
            

    cooldown_timestamp = 0
    
    def join_room(ip, port, username, password):
        global cooldown_timestamp
        
        current_timestamp = time.time()
        if not current_timestamp >= cooldown_timestamp:
            print("cooldown")
        else:
            cooldown_timestamp = current_timestamp + 10

            if focus_yuzu() == True:
                time.sleep(0.5)
                macro(ip, str(port), username, password)

                print("Room joined")
            else:
                print("Failed to join room")
    


if __name__ == "__main__":
    # test
    join_room("74.47.74.47", 35008, "usérname", "password :3")
