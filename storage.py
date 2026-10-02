import json
import os
import time

DATA_FILE = os.path.join(os.path.expanduser("~"), ".summertimer", "timers.json")


class TimerStore:
    def __init__(self):
        self.remaining = {}      # ثانیه‌ی باقی‌مانده‌ی هر تایمر (تا لحظه‌ی started_at)
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
        os.replace(tmp, DATA_FILE)  # نوشتن اتمیک؛ حتی با قطع برق فایل خراب نمی‌شود

    # ---------- منطق ----------
    def has_data(self):
        return bool(self.remaining)

    def names(self):
        return list(self.remaining)

    def create(self, times: dict):
        self.remaining = {k: float(v) for k, v in times.items()}
        self.active = self.started_at = None
        self._save()

    def get_remaining(self, name):
        left = self.remaining.get(name, 0)
        if name == self.active and self.started_at is not None:
            left -= max(0, time.time() - self.started_at)
        return max(0, left)

    def pause(self):
        if self.active:
            self.remaining[self.active] = self.get_remaining(self.active)
        self.active = self.started_at = None
        self._save()

    def select(self, name):
        self.pause()  # تایمر قبلی ذخیره و متوقف می‌شود
        if self.remaining.get(name, 0) > 0:
            self.active = name
            self.started_at = time.time()
            self._save()

    def check_finished(self):
        if self.active and self.get_remaining(self.active) <= 0:
            self.pause()