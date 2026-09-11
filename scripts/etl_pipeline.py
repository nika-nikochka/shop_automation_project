# scripts/etl_pipeline.py
import pandas as pd
import os
from datetime import datetime

def run_etl():
    print("🔄 Запуск ETL-конвейера...")
    
    # 1. Загрузка данных
    print("📂 Чтение CSV-файлов...")
    orders = pd.read_csv('data/raw/orders.csv', parse_dates=['order_date'])
    users = pd.read_csv('data/raw/users.csv', parse_dates=['registration_date'])
    items = pd.read_csv('data/raw/order_items.csv')
    
    print(f"   Заказов: {len(orders)}, Пользователей: {len(users)}, Позиций: {len(items)}")
    
    # 2. JOIN (объединение)
    print("🔗 Объединение таблиц...")
    merged = orders.merge(users, on='user_id', how='left')
    merged = merged.merge(items, on='order_id', how='left')
    
    # 3. Агрегация на уровне заказа
    print("📊 Агрегация данных...")
    final = merged.groupby(['order_id', 'user_id', 'order_date', 'city', 'status'], 
                           as_index=False).agg({
        'quantity': 'sum',
        'price': 'sum'
    })
    
    # 4. Создание новых колонок
    print("➕ Добавление расчетных колонок...")
    final['profit'] = final['price'] * 0.3  # маржа 30%
    final['order_month'] = final['order_date'].dt.to_period('M').astype(str)
    final['order_year'] = final['order_date'].dt.year
    final['order_quarter'] = final['order_date'].dt.quarter
    
    # 5. Очистка данных
    print("🧹 Очистка данных...")
    final = final[final['quantity'] > 0]
    final = final.drop_duplicates(subset=['order_id'])
    final = final.sort_values('order_date')
    
    # 6. Сохранение результата
    print("💾 Сохранение обработанных данных...")
    os.makedirs('data/processed', exist_ok=True)
    final.to_csv('data/processed/orders_enriched.csv', index=False)
    
    # 7. Вывод статистики
    print("\n📊 СТАТИСТИКА:")
    print(f"   - Всего заказов: {len(final)}")
    print(f"   - Выручка: {final['price'].sum():,.0f} руб.")
    print(f"   - Средний чек: {final['price'].mean():,.0f} руб.")
    print(f"   - Прибыль: {final['profit'].sum():,.0f} руб.")
    print(f"   - Маржинальность: {final['profit'].sum() / final['price'].sum() * 100:.1f}%")
    
    print("\n✅ ETL завершен! Файл сохранен в data/processed/orders_enriched.csv")
    return final

if __name__ == "__main__":
    final = run_etl()
    
    try:
        from check_anomalies import check_anomalies, send_daily_summary
        from email_sender import send_email_report
        
        # 1. Алерты + сводка (каждый день)
        check_anomalies()
        send_daily_summary()
        
        # 2. PDF-отчёт (только по понедельникам)
        today = datetime.now().weekday()  # 0 = Пн, 6 = Вс
        
        if today == 0:  # Понедельник
            pdf_path = 'powerbi/shop_dashboard.pdf'
            if os.path.exists(pdf_path):
                send_email_report(
                    pdf_path,
                    "📊 Еженедельный PDF-отчёт"
                )
                print("📨 PDF отправлен (понедельник)!")
            else:
                print(f"⚠️ PDF не найден: {pdf_path}")
        else:
            print(f"📅 Сегодня не понедельник (день {today}), PDF не отправляем")
        
        print("📨 Отчёты отправлены!")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        traceback.print_exc()