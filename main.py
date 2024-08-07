import json
import os
import sys
import shutil
import requests
import subprocess
import webview
from tkinter import messagebox

from join_room import yuzu_ready, join_room, showError, set_global_variable, get_global_variable
from updater import compare_versions


def get_config():
    with open("config.json", encoding="utf-8") as f:
        return json.load(f)
    
config = get_config()

def save_config(config):
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    

def check_for_updates():
    try:
        current_version = config['client-version']
        
        url = "https://api.github.com/repos/Bishoko/JigglyConnect/releases?per_page=1"
        response = requests.get(url)
        releases = response.json()
        try:
            latest_release = next((release for release in releases if not release["draft"]), None)
        except Exception:
            latest_release = None
        latest_version = "0.1"
        if latest_release is not None and "tag_name" in latest_release:
            latest_version = latest_release["tag_name"].replace('v', '')
            

        if compare_versions(latest_version, current_version) > 0:
            print(f"New version available: {latest_version}")
            
            answer = messagebox.askyesno("JigglyConnect Update", "An update is available, do you want to install it?")
            
            if answer:
                if os.path.exists("update"):
                    shutil.rmtree("update", ignore_errors=True)
                os.makedirs("update")
                shutil.copyfile("JC-updater.exe", "update/JC-updater.exe")
                shutil.copyfile("python3.dll", "update/python3.dll")
                shutil.copyfile("python311.dll", "update/python311.dll")
                shutil.copytree("lib", "update/lib")
                subprocess.Popen(["update/JC-updater.exe"])
                
            sys.exit()
        else:
            print('Removing update directory')
            if os.path.exists("update"):
                shutil.rmtree("update", ignore_errors=True)

    except Exception as e:
        showError(f"Auto Update error: {e}\n\n Please update manually on https://github.com/Bishoko/JigglyConnect/releases")
        os.startfile("https://github.com/Bishoko/JigglyConnect/releases/latest")
        sys.exit()

    
def read_cookies(window):
    # read cookies
    try:
        cookies = window.get_cookies()
    except:
        cookies = None
    
if __name__ == '__main__':
    check_for_updates()
    
    server_host = f"http://{config['server'].replace('http://','').replace('https://','')}"

    window = webview.create_window(
        'JigglyConnect',
        server_host,
        resizable=False,
        width=1080,
        height=720,
        background_color='#000'
    )
    
    window.expose(yuzu_ready, join_room)
    window.expose(get_config, save_config)
    
    set_global_variable(window)

    webview.start(
        read_cookies, window,
        private_mode=False,
        user_agent=f"JigglyConnect Browser {config['client-version']}"
    )
    