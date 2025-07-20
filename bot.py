import time
import threading
import tkinter as tk
import statistics
from keyboard import send
from PIL.Image import frombytes
from mss import mss
import pyautogui
import os

# === Настройки ===
GREEN_TARGET = (75, 255, 50)
TOLERANCE = 60
MARKER_BRIGHTNESS = 245
ZONE_FILE = "config.txt"

def load_zone():
    if not os.path.exists(ZONE_FILE):
        return None
    with open(ZONE_FILE, "r") as f:
        line = f.readline().strip()
        if line.startswith("ZONE="):
            parts = line[5:].split(",")
            if len(parts) == 4:
                return tuple(map(int, parts))
    return None

def save_zone(x1, y1, x2, y2):
    with open(ZONE_FILE, "w") as f:
        f.write(f"ZONE={x1},{y1},{x2},{y2}")

class FishingBot:
    def __init__(self):
        self.active = False
        self.zone = load_zone()
        self.prev_center_x = None
        self.space_pressed = False
        self.fishing_active = False

    def toggle(self):
        if not self.zone:
            self.zone = load_zone()
        if not self.zone:
            print("❌ Зона не выбрана.")
            return
        self.active = not self.active
        self.update_gui()
        if self.active:
            threading.Thread(target=self.run_bot).start()

    def update_gui(self):
        status_label.config(text="Активно ✅" if self.active else "Неактивно ❌")
        toggle_btn.config(bg="red" if self.active else "green")
        toggle_btn.config(text="Остановить" if self.active else "Активировать")

    def run_bot(self):
        while self.active and self.zone:
            img = self.capture_zone()
            green_coords = self.find_green_pixels(img)
            marker_found = self.find_white_marker(img, green_coords)

            if marker_found and not self.space_pressed:
                send('space')
                print("✅ Маркер в зелёной зоне → нажата пробел")
                self.space_pressed = True
                self.fishing_active = True

            if self.fishing_active and green_coords:
                x_vals = [x for x, y in green_coords]
                center_x = statistics.mean(x_vals)
                dx = center_x - (self.prev_center_x or center_x)
                if dx > 2:
                    send('d')
                    print("⬅️ Рыба влево → D")
                elif dx < -2:
                    send('a')
                    print("➡️ Рыба вправо → A")
                self.prev_center_x = center_x

            time.sleep(0.08)

    def capture_zone(self):
        with mss() as sct:
            img = sct.grab(self.zone)
        return frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

    def find_green_pixels(self, img):
        coords = []
        for x in range(0, img.size[0], 3):
            for y in range(0, img.size[1], 3):
                r, g, b = img.getpixel((x, y))
                if abs(r - GREEN_TARGET[0]) < TOLERANCE and \
                   abs(g - GREEN_TARGET[1]) < TOLERANCE and \
                   abs(b - GREEN_TARGET[2]) < TOLERANCE:
                    coords.append((x, y))
        return coords

    def find_white_marker(self, img, green_coords):
        count = 0
        for x, y in green_coords:
            r, g, b = img.getpixel((x, y))
            if r > MARKER_BRIGHTNESS and g > MARKER_BRIGHTNESS and b > MARKER_BRIGHTNESS:
                count += 1
        return count > 8  # можно настроить чувствительность

    def set_zone(self, zone):
        self.zone = zone
        save_zone(*zone)
        print(f"✅ Зона сохранена: {zone}")

# === Выбор зоны ===
def select_zone():
    root.withdraw()
    print("🖱️ Наведи курсор на верхний левый угол и нажми Enter...")
    input("⏎ Enter")
    x1, y1 = pyautogui.position()

    print("🖱️ Наведи курсор на нижний правый угол и снова нажми Enter...")
    input("⏎ Enter")
    x2, y2 = pyautogui.position()

    bot.set_zone((min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2)))
    root.deiconify()

# === GUI ===
bot = FishingBot()
root = tk.Tk()
root.title("🎣 Majestic RP Бот")
root.geometry("300x120+60+60")
root.wm_attributes('-alpha', 0.85)
root.attributes('-topmost', True)

toggle_btn = tk.Button(root, text="Активировать", command=bot.toggle,
                       width=25, bg="green", fg="white", font=("Arial", 11))
toggle_btn.pack(pady=6)

select_btn = tk.Button(root, text="Выбрать зону", command=select_zone,
                       width=25, bg="gray", fg="white", font=("Arial", 10))
select_btn.pack(pady=2)

status_label = tk.Label(root, text="Неактивно ❌", font=("Arial", 10))
status_label.pack()

root.mainloop()
