import os, sys

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


FONT = resource_path("assets/Vazir.ttf")

#بر حسب درصد
task_time = {
    "بچه داری":20,
    "کمک به خانواده":20,
    "برنامه نویسی":30,
    "سرگرمی":20,
    "سایر":10
}