-- load_data_local.sql
-- Script para importar CSVs gerados para o DB ecommerce_db usando LOAD DATA LOCAL INFILE
-- Ajuste usuário / senha ao executar o cliente mysql (veja instruções no README abaixo)

USE ecommerce_db;

-- 1) Desabilitar checagens de FK temporariamente para facilitar import
SET FOREIGN_KEY_CHECKS = 0;

-- 2) Importar customers.csv
LOAD DATA LOCAL INFILE 'G:/Documentos/1. CarreiraProfissional/CientistaDeDados/ProjetosDataScience/ProductRecomendation/ds-recomendation-system-deploy/data/customers.csv'
INTO TABLE customers
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
ESCAPED BY '\\'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(customer_id, name, email, gender, age, city, state, @registration_date)
SET registration_date = STR_TO_DATE(@registration_date, '%Y-%m-%d %H:%i:%s');

-- 3) Importar products.csv
LOAD DATA LOCAL INFILE 'G:/Documentos/1. CarreiraProfissional/CientistaDeDados/ProjetosDataScience/ProductRecomendation/ds-recomendation-system-deploy/data/products.csv'
INTO TABLE products
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
ESCAPED BY '\\'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(product_id, name, category, brand, price, @created_at, is_active)
SET created_at = STR_TO_DATE(@created_at, '%Y-%m-%d %H:%i:%s');

-- 4) Importar transactions.csv
LOAD DATA LOCAL INFILE 'G:/Documentos/1. CarreiraProfissional/CientistaDeDados/ProjetosDataScience/ProductRecomendation/ds-recomendation-system-deploy/data/transactions.csv'
INTO TABLE transactions
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
ESCAPED BY '\\'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(transaction_id, customer_id, product_id, quantity, total_value, @transaction_date)
SET transaction_date = STR_TO_DATE(@transaction_date, '%Y-%m-%d %H:%i:%s');

-- 5) Importar product_views.csv
LOAD DATA LOCAL INFILE 'G:/Documentos/1. CarreiraProfissional/CientistaDeDados/ProjetosDataScience/ProductRecomendation/ds-recomendation-system-deploy/data/product_views.csv'
INTO TABLE product_views
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
ESCAPED BY '\\'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(view_id, customer_id, product_id, @view_datetime, session_id, device_type)
SET view_datetime = STR_TO_DATE(@view_datetime, '%Y-%m-%d %H:%i:%s');

-- 6) Ajustar AUTO_INCREMENT para cada tabela (define próximo valor = max_id + 1)
-- customers
SET @m = (SELECT COALESCE(MAX(customer_id),0) + 1 FROM customers);
SET @s = CONCAT('ALTER TABLE customers AUTO_INCREMENT = ', @m);
PREPARE stmt FROM @s; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- products
SET @m = (SELECT COALESCE(MAX(product_id),0) + 1 FROM products);
SET @s = CONCAT('ALTER TABLE products AUTO_INCREMENT = ', @m);
PREPARE stmt FROM @s; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- transactions
SET @m = (SELECT COALESCE(MAX(transaction_id),0) + 1 FROM transactions);
SET @s = CONCAT('ALTER TABLE transactions AUTO_INCREMENT = ', @m);
PREPARE stmt FROM @s; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- product_views
SET @m = (SELECT COALESCE(MAX(view_id),0) + 1 FROM product_views);
SET @s = CONCAT('ALTER TABLE product_views AUTO_INCREMENT = ', @m);
PREPARE stmt FROM @s; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 7) Reabilitar checagens de FK
SET FOREIGN_KEY_CHECKS = 1;

-- 8) Verificações básicas
SELECT 'counts' AS item, COUNT(*) AS n FROM customers;
SELECT 'counts' AS item, COUNT(*) AS n FROM products;
SELECT 'counts' AS item, COUNT(*) AS n FROM transactions;
SELECT 'counts' AS item, COUNT(*) AS n FROM product_views;

-- 9) Top 10 produtos vendidos (sanity check)
SELECT p.product_id, p.name, p.category, SUM(t.quantity) AS total_qty
FROM transactions t
JOIN products p ON t.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_qty DESC
LIMIT 10;
