@echo off
cd /d "C:\Users\PC\PycharmProjects\lexicon_answer_bot"

rem === Подтягиваем последние изменения ===
git pull > nul

rem === Получаем текущий коммит ===
for /f %%i in ('git rev-parse HEAD') do set NEW_COMMIT=%%i

rem === Читаем предыдущий коммит из файла ===
set FILE=last_commit.txt
if exist %FILE% (
    set /p OLD_COMMIT=<%FILE%
) else (
    set OLD_COMMIT=none
)

rem === Если нет изменений — выходим ===
if "%NEW_COMMIT%"=="%OLD_COMMIT%" (
    echo [%DATE% %TIME%] ✅ Нет обновлений >> watcher.log
    exit /b
)

rem === Обновление обнаружено ===
echo [%DATE% %TIME%] 🔁 Обнаружены изменения. Перезапуск... >> watcher.log
echo %NEW_COMMIT% > %FILE%

rem === Завершаем python.exe (старый бот) ===
taskkill /f /im python.exe > nul 2>&1
timeout /t 2 > nul

rem === Запускаем обновлённый бот ===
start "" .venv\Scripts\python.exe main.py
echo [%DATE% %TIME%] ✅ Новый бот запущен >> watcher.log
