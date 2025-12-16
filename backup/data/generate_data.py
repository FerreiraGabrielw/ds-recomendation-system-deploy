import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from faker import Faker

# ============================
# CONFIGURAÇÕES INICIAIS
# ============================

fake = Faker("pt_BR")
random.seed(42)
np.random.seed(42)

# Quantidades de registros
N_CUSTOMERS = 1000
N_PRODUCTS = 300
N_TRANSACTIONS = 8000
N_VIEWS = 20000

# Período de datas para compras e visualizações (último ano)
NOW = datetime.now()
START_DATE = NOW - timedelta(days=365)

# ============================
# 1. GERAR CUSTOMERS
# ============================

print("Gerando customers...")

customer_rows = []

for customer_id in range(1, N_CUSTOMERS + 1):
    name = fake.name()
    email = fake.unique.email()
    gender = np.random.choice(["M", "F", "O"], p=[0.48, 0.48, 0.04])
    age = np.random.randint(18, 65)
    city = fake.city()
    state = fake.estado_sigla()
    registration_date = fake.date_time_between(start_date="-2y", end_date="now")

    customer_rows.append(
        {
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "gender": gender,
            "age": age,
            "city": city,
            "state": state,
            "registration_date": registration_date,
        }
    )

customers_df = pd.DataFrame(customer_rows)

# Salvar CSV
customers_df.to_csv("customers.csv", index=False)
print("customers.csv gerado com sucesso! Registros:", len(customers_df))


# ============================
# 2. GERAR PRODUCTS
# ============================

print("Gerando products...")

categories = ["Roupas", "Calçados", "Acessórios", "Eletrônicos", "Casa"]
brands_by_category = {
    "Roupas": ["Nike", "Adidas", "Puma", "Reserva"],
    "Calçados": ["Nike", "Adidas", "Puma", "Mizuno"],
    "Acessórios": ["Rayban", "Oakley", "Apple", "Samsung"],
    "Eletrônicos": ["Apple", "Samsung", "LG", "Sony"],
    "Casa": ["Tramontina", "Brastemp", "Electrolux"],
}

product_rows = []

for product_id in range(1, N_PRODUCTS + 1):
    category = random.choice(categories)
    brand = random.choice(brands_by_category[category])
    # Nome do produto com categoria + marca + uma palavra aleatória
    name = f"{category} {brand} {fake.word().capitalize()}"
    price = round(random.uniform(30, 1500), 2)
    created_at = fake.date_time_between(start_date="-1y", end_date="now")
    is_active = 1  # todos ativos por enquanto

    product_rows.append(
        {
            "product_id": product_id,
            "name": name,
            "category": category,
            "brand": brand,
            "price": price,
            "created_at": created_at,
            "is_active": is_active,
        }
    )

products_df = pd.DataFrame(product_rows)

# Salvar CSV
products_df.to_csv("products.csv", index=False)
print("products.csv gerado com sucesso! Registros:", len(products_df))


# ============================
# 3. GERAR TRANSACTIONS
# ============================

print("Gerando transactions...")

transaction_rows = []

# Vamos criar um "gostinho" de comportamento:
# - Idades menores tendem mais a Roupas/Calçados
# - Idades maiores tendem mais a Casa/Eletrônicos
def escolher_categoria_por_idade(age):
    if age < 25:
        return np.random.choice(
            ["Roupas", "Calçados", "Acessórios", "Eletrônicos"],
            p=[0.35, 0.35, 0.15, 0.15],
        )
    elif age < 40:
        return np.random.choice(
            ["Roupas", "Calçados", "Eletrônicos", "Casa"],
            p=[0.25, 0.25, 0.30, 0.20],
        )
    else:
        return np.random.choice(
            ["Eletrônicos", "Casa", "Roupas"],
            p=[0.40, 0.40, 0.20],
        )

for transaction_id in range(1, N_TRANSACTIONS + 1):
    # escolher um cliente
    cust = customers_df.sample(1).iloc[0]
    customer_id = int(cust["customer_id"])
    age = int(cust["age"])

    # categoria preferida pela idade
    category = escolher_categoria_por_idade(age)

    # restringir produtos àquela categoria
    prod_sample = products_df[products_df["category"] == category]
    if prod_sample.empty:
        prod_sample = products_df  # fallback

    product = prod_sample.sample(1).iloc[0]
    product_id = int(product["product_id"])
    price = float(product["price"])

    quantity = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
    total_value = round(price * quantity, 2)

    # data aleatória no último ano
    delta_days = random.randint(0, 365)
    delta_seconds = random.randint(0, 24 * 3600 - 1)
    transaction_date = START_DATE + timedelta(days=delta_days, seconds=delta_seconds)

    transaction_rows.append(
        {
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "product_id": product_id,
            "quantity": quantity,
            "total_value": total_value,
            "transaction_date": transaction_date,
        }
    )

transactions_df = pd.DataFrame(transaction_rows)

# Salvar CSV
transactions_df.to_csv("transactions.csv", index=False)
print("transactions.csv gerado com sucesso! Registros:", len(transactions_df))


# ============================
# 4. GERAR PRODUCT_VIEWS
# ============================

print("Gerando product_views...")

view_rows = []

device_types = ["desktop", "mobile", "tablet"]

for view_id in range(1, N_VIEWS + 1):
    cust = customers_df.sample(1).iloc[0]
    customer_id = int(cust["customer_id"])

    product = products_df.sample(1).iloc[0]
    product_id = int(product["product_id"])

    delta_days = random.randint(0, 365)
    delta_seconds = random.randint(0, 24 * 3600 - 1)
    view_datetime = START_DATE + timedelta(days=delta_days, seconds=delta_seconds)

    device_type = np.random.choice(device_types, p=[0.4, 0.5, 0.1])
    session_id = fake.uuid4()

    view_rows.append(
        {
            "view_id": view_id,
            "customer_id": customer_id,
            "product_id": product_id,
            "view_datetime": view_datetime,
            "session_id": session_id,
            "device_type": device_type,
        }
    )

views_df = pd.DataFrame(view_rows)

# Salvar CSV
views_df.to_csv("product_views.csv", index=False)
print("product_views.csv gerado com sucesso! Registros:", len(views_df))

print("\n✅ Todos os CSVs foram gerados na pasta atual:")
print(" - customers.csv")
print(" - products.csv")
print(" - transactions.csv")
print(" - product_views.csv")
