import win32gui
from datetime import datetime
import subprocess
import ctypes
import asyncio

async def get_focused_window_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)
    except Exception:
        return None
    
async def if_screen():
    try:
        ps_cmd = [
            "powershell",
            "-Command",
            "(Get-CimInstance -Namespace root\\wmi -ClassName WmiMonitorBrightness).CurrentBrightness"
        ]
        result = subprocess.check_output(ps_cmd, stderr=subprocess.DEVNULL, text=True).strip()
        brightness = int(result)
        return brightness > 0
    except Exception:
        ctypes.windll.user32.GetSystemMetrics(80)>0

async def collect_data():
    date = datetime.now()
    application_history = {}

    async def fuckmyself():
        async with asyncio.TaskGroup() as tg:
            app_title = tg.create_task(get_focused_window_title())
            screen = tg.create_task(if_screen())
            _ = tg.create_task(asyncio.sleep(60)) #NEED TO CHANGE LATERRRRR THIS IS ACTUALLY IMPORTANT

        app_title, screen = app_title.result(), screen.result()
        if screen:
            if app_title not in application_history.keys():
                application_history[app_title]=0
            application_history[app_title]+=1
            print(app_title)

    for _ in range(60):
        p = await fuckmyself()
    return {"date":date, "data":{"application_history": application_history, "screen_time":sum(application_history.values())}}


print(asyncio.run(collect_data()))
