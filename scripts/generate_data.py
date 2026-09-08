# scripts/generate_data.py
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('ru_RU')
random.seed(42)
np.random.seed(42)

# 1. Генерация пользователей (1000 человек)
users = []
for i in range(1, 1001):
    users.append({
        'user_id': i,
        'registration_date': fake.date_time_between(start_date='-365d', end_date='now'),
        'city': random.choice(['Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск', 
                              'Екатеринбург', 'Нижний Новгород', 'Ростов-на-Дону', 
                              'Самара', 'Уфа', 'Красноярск']),
        'age': random.randint(18, 70)
    })
users_df = pd.DataFrame(users)

# 2. Генерация заказов (5000 заказов за последние 6 месяцев)
orders = []
statuses = ['completed', 'completed', 'completed', 'completed', 'processing', 'cancelled']
for i in range(1, 5001):
    user_id = random.randint(1, 1000)
    days_ago = random.randint(0, 180)
    order_date = datetime.now() - timedelta(days=days_ago)
    orders.append({
        'order_id': i,
        'user_id': user_id,
        'order_date': order_date,
        'status': random.choice(statuses)
    })
orders_df = pd.DataFrame(orders)

# 3. Генерация товаров в заказах (в среднем 2-5 товаров на заказ)
items = []
product_ids = list(range(1, 101))
for order_id in range(1, 5001):
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 3)
        price = round(random.uniform(500, 15000), 2)
        items.append({
            'order_id': order_id,
            'product_id': product_id,
            'quantity': quantity,
            'price': price
        })
items_df = pd.DataFrame(items)

# 4. Сохранение в CSV
users_df.to_csv('data/raw/users.csv', index=False)
orders_df.to_csv('data/raw/orders.csv', index=False)
items_df.to_csv('data/raw/order_items.csv', index=False)

print(f"✅ Сгенерировано:")
print(f"   - Пользователей: {len(users_df)}")
print(f"   - Заказов: {len(orders_df)}")
print(f"   - Позиций в заказах: {len(items_df)}")
print("📁 Файлы сохранены в data/raw/")