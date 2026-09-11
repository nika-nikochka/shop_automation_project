# scripts/email_sender.py
import yagmail
import os
from datetime import datetime

EMAIL = "nika-nikochka@inbox.ru"
APP_PASSWORD = "6K6lz2vDTIRbWeZUzgmU"
TO_EMAIL = "nika-nikochka@inbox.ru"
SMTP_HOST = "smtp.mail.ru"
SMTP_PORT = 465


def send_email_report(pdf_path, caption=""):
    """Отправка PDF-отчёта на email"""
    try:
        yag = yagmail.SMTP(
            user=EMAIL,
            password=APP_PASSWORD,
            host=SMTP_HOST,
            port=SMTP_PORT,
            smtp_ssl=True
        )
        
        subject = f"📊 Отчёт интернет-магазина за {datetime.now().strftime('%d.%m.%Y')}"
        
        body = f"""
        <h2>Еженедельный отчёт интернет-магазина</h2>
        <p>{caption}</p>
        <p>PDF-отчёт во вложении.</p>
        <hr>
        <p style="color: #888; font-size: 12px;">
            Автоматическая система отчётности • {datetime.now().strftime('%d.%m.%Y %H:%M')}
        </p>
        """
        
        yag.send(to=TO_EMAIL, subject=subject, contents=[body, pdf_path])
        print(f"✅ Email отправлен на {TO_EMAIL}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False


def send_email_alert(text):
    """Отправка алерта"""
    try:
        yag = yagmail.SMTP(
            user=EMAIL,
            password=APP_PASSWORD,
            host=SMTP_HOST,
            port=SMTP_PORT,
            smtp_ssl=True
        )
        
        subject = f"🚨 АЛЕРТ: {datetime.now().strftime('%d.%m.%Y')}"
        
        body = f"""
        <div style="background: #ffe6e6; padding: 20px; border-left: 4px solid #d13438;">
            <h2 style="color: #d13438;">🚨 ВНИМАНИЕ!</h2>
            <p style="font-size: 16px;">{text}</p>
        </div>
        """
        
        yag.send(to=TO_EMAIL, subject=subject, contents=body)
        print("✅ Алерт отправлен")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def send_weekly_report():
    pdf_path = 'powerbi/shop_dashboard.pdf'
    if not os.path.exists(pdf_path):
        print(f"⚠️ Файл {pdf_path} не найден!")
        return
    
    caption = "Ключевые метрики за последнюю неделю."
    send_email_report(pdf_path, caption)


if __name__ == "__main__":
    send_weekly_report()