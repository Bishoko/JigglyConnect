import json
import webview
import threading
from join_room import join_room

def server():
    import server
    
server_thread = threading.Thread(target=server, daemon=True)
server_thread.start()


with open("config.json", encoding="utf-8") as f:
    config = json.load(f)


def read_cookies(window):
    cookies = window.get_cookies()
        
if __name__ == '__main__':
    window = webview.create_window(
        'JigglyConnect',
        f'http://{config["server"]}/',
        resizable=False,
        width=1000,
        height=630,
        background_color='#000'
    )
    
    window.expose(join_room)
    
    webview.start(
        read_cookies, window,
        private_mode=False,
        user_agent=f"JigglyConnect Browser {config['client-version']}"
    )