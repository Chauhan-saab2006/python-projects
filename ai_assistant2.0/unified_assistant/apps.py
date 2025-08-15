import subprocess
import os
import pygetwindow
import win32gui
import win32con

software_paths = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "visual studio code": r"C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "word": r"C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "excel": r"C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
}

def open_software(name: str):
    for key, path in software_paths.items():
        if key in name.lower():
            try:
                subprocess.Popen(path)
                return True
            except Exception:
                return False
    return False

def close_software(name: str):
    for key, path in software_paths.items():
        if key in name.lower():
            process_name = os.path.basename(path)
            os.system(f"taskkill /f /im {process_name}")
            return True
    return False

def minimize_software(name: str):
    for window in pygetwindow.getAllTitles():
        if name.lower() in window.lower():
            hwnd = win32gui.FindWindow(None, window)
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return True
    return False

def maximize_software(name: str):
    for window in pygetwindow.getAllTitles():
        if name.lower() in window.lower():
            hwnd = win32gui.FindWindow(None, window)
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            return True
    return False
