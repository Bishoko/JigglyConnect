import ctypes
import sys
import os
import shutil
import json
import requests
import psutil
import win32com
import subprocess
import ctypes
import zipfile
import tkinter as tk
from tkinter import messagebox


def error(message):
    print(message)
    ctypes.windll.user32.MessageBoxW(None, message, "WebDeck Updater Error", 0)


def move_folder_content(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    for element in os.listdir(source):
        source_path = os.path.join(source, element)
        destination_path = os.path.join(destination, element)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)

        elif os.path.isdir(source_path):
            move_folder_content(source_path, destination_path)


def close_process(process_name):
    try:
        for proc in psutil.process_iter(["pid", "name"]):
            if process_name.lower() in proc.info["name"].lower():
                try:
                    pid = proc.info["pid"]
                    os.kill(pid, psutil.signal.SIGTERM)
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    pass

    except:
        try:
            wmi = win32com.client.GetObject("winmgmts:")
            processes = wmi.InstancesOf("Win32_Process")
            for process in processes:
                if process.Properties_('Name').Value.replace('.exe','').lower().strip() in ["jigglyconnect"]:
                    print(f"Stopping process: {process.Properties_('Name').Value}")
                    result = process.Terminate()
                    if result == 0:
                        print("Process terminated successfully.")
                    else:
                        print("Failed to terminate process.")
        except:
            try:
                subprocess.Popen(f"taskkill /f /IM {process_name}", shell=True)
            except:
                pass


def compare_versions(version1, version2):
    v1_components = list(map(int, version1.split(".")))
    v2_components = list(map(int, version2.split(".")))

    for v1, v2 in zip(v1_components, v2_components):
        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1

    if len(v1_components) > len(v2_components):
        return 1
    elif len(v1_components) < len(v2_components):
        return -1

    return 0


# TESTING
# def compare_versions(version1, version2):
#     return 1


def check_updates(current_version):
    url = "https://api.github.com/repos/Bishoko/JigglyConnect/releases?per_page=1"
    response = requests.get(url)
    releases = response.json()
    try:
        latest_release = next(
            (release for release in releases if not release["draft"]), None
        )
    except Exception:
        latest_release = None
    latest_version = "0.1"
    if latest_release is not None and "tag_name" in latest_release:
        latest_version = latest_release["tag_name"].replace("v", "")

    if compare_versions(latest_version, current_version) > 0:
        print(f"New version available: {latest_version}")

        close_process("JigglyConnect.exe")
        for file_url in latest_release["assets"]:
            if (
                file_url["browser_download_url"].endswith("portable.zip")
                and file_url["state"] == "uploaded"
            ):
                download_and_extract(file_url["browser_download_url"])
                break

        # Remove the JigglyConnect directory
        print("Removing JigglyConnect directory")
        update_dir_path = os.path.join(jc_dir, "JigglyConnect")
        shutil.rmtree(update_dir_path, ignore_errors=True)
        
        # Remove the JC-update directory
        print("Removing JC-update directory")
        update_dir_path = os.path.join(jc_dir, "JC-update")
        shutil.rmtree(update_dir_path, ignore_errors=True)

        # Delete the JC-update.zip file
        zip_file_path = os.path.join(jc_dir, "JC-update.zip")
        os.remove(zip_file_path)
        print("JC-update.zip deleted")

        # Launch JigglyConnect.exe from the jc_dir (root) directory
        print("Restarting JigglyConnect.exe")
        exe_path = os.path.join(jc_dir, "JigglyConnect.exe")
        os.system(exe_path)


def download_and_extract(download_url):
    response = requests.get(download_url, stream=True)
    if response.status_code != 200:
        error("Failed to download update ZIP file.")
    else:
        with open("JC-update.zip", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        with zipfile.ZipFile("JC-update.zip", "r") as zip_ref:
            zip_ref.extractall("JC-update")

        source = os.path.join(jc_dir, "JC-update/JigglyConnect")
        destination = jc_dir

        move_folder_content(source, destination)


# TESTING
# def download_and_extract(download_url):
#     shutil.copyfile("E:/Users/81len/Downloads/JC-fake-update.zip", "JC-update.zip")
#     with zipfile.ZipFile('JC-update.zip', 'r') as zip_ref:
#         zip_ref.extractall(jc_dir)
#
#     source = os.path.join(jc_dir, "JigglyConnect")
#     destination = jc_dir
#
#     move_folder_content(source, destination)


if __name__ == "__main__":
    print("Starting updater...")

    current_dir = f"{os.path.abspath(os.path.dirname(__file__))}/update"
    jc_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    if not current_dir.endswith("update"):
        sys.exit()
    version_path = os.path.join(jc_dir, "config.json")

    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    with open(version_path, encoding="utf-8") as f:
        current_version = json.load(f)["client-version"]

    check_updates(current_version)
