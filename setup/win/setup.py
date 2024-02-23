from cx_Freeze import setup, Executable

with open("setup/win/requirements.txt", "r") as file:
    requirements_list = [
        line.strip().replace("pywebview", "webview").replace("pywin32", "win32gui")
        for line in file.readlines()
        if line.strip() and not line.strip() == "cx_Freeze"
    ]

build_options = {
    "include_files": [],
    "packages": requirements_list,
    "excludes": ["cx_Freeze"],
    "zip_include_packages": [],
    "zip_exclude_packages": "*"
}

import sys, os, json, shutil
import time


start_time = time.time()
sys.setrecursionlimit(10000)
base = "Win32GUI" if sys.platform == "win32" else None
# base = 'console' if sys.platform=='win32' else None

executables = [
    Executable("main.py", base=base, target_name="JigglyConnect", icon="icon.ico"),
    Executable("updater.py", base=base, target_name="JC-updater")
]

with open("config.json", encoding="utf-8") as f:
    version = json.load(f)["client-version"]

setup(
    name="JigglyConnect",
    description="JigglyConnect",
    author="Bishoko Team",
    version=version,
    options={"build_exe": build_options},
    executables=executables,
)


exclude_folders = [
    ".git",
    ".github",
    ".vscode",
    "__pycache__",
    "build",
    "requirements.txt",
    "build.bat",
    "JigglyConnect.exe",
    "JC-updater.exe",
    "icon.ico",
    "DOC.txt",
    "TODO.txt",
    "debug.log",
    "server",
    "setup",
    "JigglyConnect",
]

script_dir = os.getcwd()
build_dir = os.path.join(script_dir, "build")

print(script_dir)

if os.path.exists(build_dir):
    first_folder = next(
        entry
        for entry in os.listdir(build_dir)
        if os.path.isdir(os.path.join(build_dir, entry))
    )
    target_dir = os.path.join(build_dir, first_folder)

    shutil.copy2("join_room.py", os.path.join(target_dir, "lib"))
    shutil.copy2("updater.py", os.path.join(target_dir, "lib"))

    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)
        if (
            item != target_dir
            and item not in exclude_folders
            and item.endswith(".py") == False
            and item.endswith(".md") == False
        ):
            if os.path.isdir(item_path):
                shutil.copytree(item_path, os.path.join(target_dir, item))
            else:
                shutil.copy2(item_path, target_dir)
            print(f"copying {item_path} -> {target_dir}")


end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(f"build done! {minutes}m{seconds}s")
