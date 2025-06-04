import subprocess
import time
import os
from datetime import datetime
import platform
import requests

# Настройки
BOT_TOKEN = 'ТВОЙ_ТОКЕН_БОТА'
ADMIN_ID = 'ТВОЙ_ID_ТЕЛЕГРАМ'

def log(message):
    with open("watcher.log", "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {message}\n")

def notify_admin(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": ADMIN_ID,
        "text": message
    }
    try:
        requests.post(url, data=data)
        log(f"📨 Уведомление отправлено: {message}")
    except Exception as e:
        log(f"❌ Ошибка отправки уведомления: {e}")

def get_latest_commit():
    result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
    return result.stdout.strip()

def run():
    log("🕵️ Наблюдатель запущен")
    notify_admin("🛠 Наблюдатель обновлений запущен на сервере")

    last_commit = get_latest_commit()

    while True:
        time.sleep(60)  # проверять раз в минуту
        subprocess.run(['git', 'pull'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        current_commit = get_latest_commit()
        if current_commit != last_commit:
            log("🔁 Обнаружены изменения. Перезапуск бота...")
            notify_admin("♻️ Обнаружены изменения. Бот будет перезапущен с обновлениями.")

            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)

            subprocess.Popen(['.venv\\Scripts\\python.exe', 'main.py'], shell=True)
            last_commit = current_commit
            log("✅ Новый бот запущен")
            notify_admin("✅ Бот успешно перезапущен после обновления")
        else:
            log("✅ Нет изменений")

if __name__ == '__main__':
    if platform.system() == "Windows":
        os.chdir(r"C:\Users\PC\PycharmProjects\lexicon_answer_bot")
        run()
    else:
        log("❌ Эта программа предназначена только для Windows")
