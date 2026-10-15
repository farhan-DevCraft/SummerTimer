import json
import os
import time
from variable_file import IDLE_NAME

DATA_FILE = os.path.join(os.path.expanduser("~"), ".summertimer", "timers.json")


class TimerStore:
    def __init__(self):
        self.remaining = {}      # ثانیه‌ی باقی‌مانده تا لحظه‌ی started_at (می‌تواند منفی باشد)
        self.active = None       # نام تایمر فعال
        self.started_at = None   # زمان سیستم هنگام شروع تایمر فعال
        self._load()

    # ---------- فایل ----------
    def _load(self):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                data = json.load(f)
            self.remaining = {k: float(v) for k, v in data["remaining"].items()}
            self.active = data.get("active")
            self.started_at = data.get("started_at")
        except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError):
            self.remaining, self.active, self.started_at = {}, None, None

        # سازگاری با فایل‌های قدیمی: اگر چیزی فعال نبود، «سایر» فعال شود
        if self.remaining and (self.active not in self.remaining or self.started_at is None):
            self.active = IDLE_NAME
            self.started_at = time.time()
            self._save()

    def _save(self):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        tmp = DATA_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "remaining": self.remaining,
                    "active": self.active,
                    "started_at": self.started_at,
                },
                f, ensure_ascii=False, indent=2,
            )
        os.replace(tmp, DATA_FILE)  # نوشتن اتمیک

    # ---------- منطق ----------
    def has_data(self):
        return bool(self.remaining)

    def names(self):
        return list(self.remaining)

    def create(self, times: dict):
        self.remaining = {k: float(v) for k, v in times.items()}
        self._switch(IDLE_NAME)

    def get_remaining(self, name):
        left = self.remaining.get(name, 0)
        if name == self.active and self.started_at is not None:
            left -= max(0, time.time() - self.started_at)
        return left  # بدون محدودیت؛ منفی هم ادامه پیدا می‌کند

    def _switch(self, name):
        # زمان تایمر فعلی را ذخیره می‌کند و تایمر جدید را شروع می‌کند
        if self.active:
            self.remaining[self.active] = self.get_remaining(self.active)
        self.active = name
        self.started_at = time.time()
        self._save()

    def select(self, name):
        if name == IDLE_NAME:
            return
        # کلیک روی تایمر فعال = توقف (برگشت به «سایر»)
        self._switch(IDLE_NAME if name == self.active else name)
    def reset(self):
        self.remaining = {}
        self.active = None
        self.started_at = None
        try:
            os.remove(DATA_FILE)
        except FileNotFoundError:
            pass