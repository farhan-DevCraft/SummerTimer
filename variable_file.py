import os, sys

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


FONT = resource_path("assets/Vazir.ttf")
IDLE_NAME = "سایر"  
RESET_PASSWORD = "1399"  
VERSION = "1.1.0"

FIXED_MINUTES = {
    "سایر": 120,
}
task_time = {
    "بچه داری": 40,
    "کمک به خانواده": 15,
    "برنامه نویسی": 10,
    "درس":25,
    "سرگرمی": 10,
}