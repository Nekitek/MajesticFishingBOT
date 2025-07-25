# 🎣 Majestic RP Fishing Tracker

**Автоматизированный бот для слежки за движением рыбы в механике ловли на серверах Majestic RP (AltV)**  
Позволяет удерживать рыбу в зелёной зоне за счёт точного отслеживания её движения и реакции на клавиши `A` и `D`.

---

## ⚙️ Возможности

- 🧭 Автоматическое управление: нажимает `A` или `D` в зависимости от направления движения рыбы
- 🖱️ Выбор зоны сканирования вручную, сохраняется в `config.txt`
- 🪟 Простой графический интерфейс (`tkinter`)
- 💾 Сохранение выбранной зоны между запусками

---

## 🛠️ Технологии

| Библиотека   | Назначение                  |
|--------------|-----------------------------|
| `keyboard`   | Эмуляция клавиш в AltV      |
| `mss`        | Скриншот зоны экрана        |
| `pillow`     | Обработка изображения       |
| `pyautogui`  | Получение позиции курсора   |
| `tkinter`    | Минималистичный GUI         |

---

🚀 Использование

🔧 Запусти файл majestic_bot.py:
```bash
python majestic_bot.py
```
🖱️ Выбери зону:

    Нажми кнопку "Выбрать зону" в GUI

    Наведи курсор на верхний левый угол зоны рыбалки и нажми Enter

    Затем — на нижний правый угол и снова нажми Enter

✅ Активируй бота:

  Нажми кнопку "Активировать"

  Бот начнёт отслеживать движение зелёного маркера

  В консоли будут появляться сообщения:
```
⬅️ Влево → D
➡️ Вправо → A
```


## 📦 Установка

```bash
pip install keyboard pillow mss pyautogui
```

## 💬 Связь

Если у тебя есть вопросы, предложения по улучшению или ты нашёл баг — обязательно сообщи!

- 🔗 Discord-сервер: [discord.gg/TzdKT6krRC](https://discord.gg/TzdKT6krRC)

Всегда открыт к сотрудничеству, идеям и обратной связи 🤝
