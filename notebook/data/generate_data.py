import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from faker import Faker

# ============================
# CONFIG
# ============================
fake = Faker("pt_BR")
random.seed(42)
np.random.seed(42)

N_CUSTOMERS = 1000
N_PRODUCTS = 300
N_ORDERS = 12000          # pedidos reais
MAX_ITEMS_PER_ORDER = 5
N_VIEWS = 70000

NOW = datetime.now()
START_DATE = NOW - timedelta(days=365)

# ============================
# 1. CUSTOMERS
# ============================
categories = ["Roupas", "Calçados", "Acessórios", "Eletrônicos", "Casa"]

customers = []

for customer_id in range(1, N_CUSTOMERS + 1):
    favorite_categories = random.sample(categories, k=random.choice([2, 3]))

    customers.append({
        "customer_id": customer_id,
        "name": fake.name(),
        "email": fake.unique.email(),
        "gender": np.random.choice(["M", "F", "O"], p=[0.48, 0.48, 0.04]),
        "age": np.random.randint(18, 65),
        "city": fake.city(),
        "state": fake.estado_sigla(),
        "registration_date": fake.date_time_between(start_date="-2y", end_date="now"),
        "favorite_categories": favorite_categories
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv("customers.csv", index=False)
print("✅ customers.csv")

# ============================
# 2. PRODUCTS
# ============================
brands_by_category = {
    "Roupas": ["Nike", "Adidas", "Puma", "Reserva"],
    "Calçados": ["Nike", "Adidas", "Puma", "Mizuno"],
    "Acessórios": ["Rayban", "Oakley", "Apple", "Samsung"],
    "Eletrônicos": ["Apple", "Samsung", "LG", "Sony"],
    "Casa": ["Tramontina", "Brastemp", "Electrolux"]
}

products = []

for product_id in range(1, N_PRODUCTS + 1):
    category = random.choice(categories)
    brand = random.choice(brands_by_category[category])

    products.append({
        "product_id": product_id,
        "name": f"{category} {brand} {fake.word().capitalize()}",
        "category": category,
        "brand": brand,
        "price": round(random.uniform(30, 1500), 2),
        "created_at": fake.date_time_between(start_date="-1y", end_date="now"),
        "is_active": 1
    })

products_df = pd.DataFrame(products)
products_df.to_csv("products.csv", index=False)
print("✅ products.csv")

# ============================
# 3. TRANSACTIONS (COM CARRINHO)
# ============================
transactions = []
transaction_id = 1

# Probabilidades de tamanho do carrinho
cart_size_probs = [0.5, 0.3, 0.15, 0.04, 0.01]

cross_sell_map = {
    "Calçados": ["Acessórios"],
    "Eletrônicos": ["Acessórios"],
    "Casa": ["Casa"],
    "Roupas": ["Acessórios"]
}

for _ in range(N_ORDERS):
    cust = customers_df.sample(1).iloc[0]

    order_date = START_DATE + timedelta(
        days=random.randint(0, 365),
        seconds=random.randint(0, 86400)
    )

    cart_size = np.random.choice(
        [1, 2, 3, 4, 5],
        p=cart_size_probs
    )

    base_category = random.choice(cust["favorite_categories"])

    cart_products = []

    for i in range(cart_size):
        if i == 0:
            category = base_category
        else:
            if base_category in cross_sell_map and random.random() < 0.6:
                category = random.choice(cross_sell_map[base_category])
            else:
                category = random.choice(categories)

        prod_pool = products_df[products_df["category"] == category]
        product = prod_pool.sample(1).iloc[0]

        cart_products.append(product)

    for product in cart_products:
        quantity = np.random.choice([1, 2, 3], p=[0.65, 0.25, 0.10])
        total_value = round(product["price"] * quantity, 2)

        transactions.append({
            "transaction_id": transaction_id,
            "customer_id": cust["customer_id"],
            "product_id": product["product_id"],
            "quantity": quantity,
            "total_value": total_value,
            "transaction_date": order_date
        })

        transaction_id += 1

transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv("transactions.csv", index=False)
print("✅ transactions.csv")

# ============================
# 4. PRODUCT_VIEWS
# ============================
views = []
device_types = ["desktop", "mobile", "tablet"]

for view_id in range(1, N_VIEWS + 1):
    cust = customers_df.sample(1).iloc[0]

    if random.random() < 0.7:
        category = random.choice(cust["favorite_categories"])
        prod_pool = products_df[products_df["category"] == category]
    else:
        prod_pool = products_df

    product = prod_pool.sample(1).iloc[0]

    views.append({
        "view_id": view_id,
        "customer_id": cust["customer_id"],
        "product_id": product["product_id"],
        "view_datetime": START_DATE + timedelta(
            days=random.randint(0, 365),
            seconds=random.randint(0, 86400)
        ),
        "session_id": fake.uuid4(),
        "device_type": np.random.choice(device_types, p=[0.4, 0.5, 0.1])
    })

views_df = pd.DataFrame(views)
views_df.to_csv("product_views.csv", index=False)
print("✅ product_views.csv")

print("\n🚀 DADOS GERADOS COM CARRINHO REALISTA E CROSS-SELL")
