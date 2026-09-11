@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo ========================================
echo Запуск ETL + отправка email-отчёта
echo ========================================
python scripts\etl_pipeline.py
echo.
echo Готово! Нажми любую клавишу для выхода.
pause