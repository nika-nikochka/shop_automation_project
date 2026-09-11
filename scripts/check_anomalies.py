# scripts/check_anomalies.py
import pandas as pd
import os
from datetime import datetime
from email_sender import send_email_alert, send_email_report


HISTORY_FILE = 'data/processed/revenue_history.csv'
THRESHOLD = 0.20  # 20% падение — порог алерта


def check_anomalies():
    """Проверка падения выручки"""
    df = pd.read_csv('data/processed/orders_enriched.csv')
    current_revenue = df['price'].sum()
    current_orders = len(df)
    current_avg_check = df['price'].mean()
    
    print(f"📊 Текущая выручка: {current_revenue:,.0f} руб.")
    
    # Проверка истории
    if os.path.exists(HISTORY_FILE):
        history = pd.read_csv(HISTORY_FILE)
        previous_revenue = history['revenue'].iloc[-1]
        
        print(f"📊 Прошлая выручка: {previous_revenue:,.0f} руб.")
        
        # Проверка падения > 20%
        if current_revenue < previous_revenue * (1 - THRESHOLD):
            drop_pct = (1 - current_revenue / previous_revenue) * 100
            
            alert_text = (
                f"Выручка упала на <b>{drop_pct:.1f}%</b>!<br><br>"
                f"📉 Было: {previous_revenue:,.0f} руб.<br>"
                f"📉 Стало: {current_revenue:,.0f} руб.<br>"
                f"📦 Заказов: {current_orders}<br>"
                f"💳 Средний чек: {current_avg_check:,.0f} руб."
            )
            send_email_alert(alert_text)
            print("⚠️ Отправлен алерт о падении выручки!")
        else:
            print("✅ Аномалий не обнаружено.")
    else:
        print("📝 Файл истории не найден. Создаю первый снимок...")
    
    # Сохраняем текущую выручку в историю
    new_row = pd.DataFrame([{
        'date': datetime.now().strftime('%Y-%m-%d'),
        'revenue': current_revenue,
        'orders': current_orders
    }])
    
    if os.path.exists(HISTORY_FILE):
        old_history = pd.read_csv(HISTORY_FILE)
        new_row = pd.concat([old_history, new_row], ignore_index=True)
    
    new_row.to_csv(HISTORY_FILE, index=False)
    print("💾 История обновлена.")


def send_daily_summary():
    """Ежедневная сводка с ключевыми метриками"""
    df = pd.read_csv('data/processed/orders_enriched.csv')
    
    revenue = df['price'].sum()
    profit = df['profit'].sum()
    orders = len(df)
    avg_check = df['price'].mean()
    margin = profit / revenue * 100
    users = df['user_id'].nunique()
    cities = df['city'].nunique()
    
    text = (
        f"<b>📊 Ежедневный отчёт</b><br>"
        f"📅 {datetime.now().strftime('%d.%m.%Y')}<br>"
        f"━━━━━━━━━━━━━━━<br>"
        f"💰 Выручка: <b>{revenue:,.0f} руб.</b><br>"
        f"📈 Прибыль: {profit:,.0f} руб.<br>"
        f"📦 Заказов: {orders}<br>"
        f"💳 Средний чек: {avg_check:,.0f} руб.<br>"
        f"📊 Маржинальность: {margin:.1f}%<br>"
        f"━━━━━━━━━━━━━━━<br>"
        f"👥 Пользователей: {users}<br>"
        f"🏙️ Городов: {cities}"
    )
    
    send_email_alert(text)  # используем ту же функцию
    print("✅ Ежедневная сводка отправлена!")


if __name__ == "__main__":
    check_anomalies()
    send_daily_summary()