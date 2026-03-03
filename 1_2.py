import pandas as pd
import sqlite3

# 1. Завантаження даних SpaceX (твій файл)
df = pd.read_csv("dataset_part_2.csv")

# 2. Створення підключення до бази даних у пам'яті
conn = sqlite3.connect(':memory:')
df.to_sql('SPACEXTABLE', conn, index=False, if_exists='replace')

def run_query(query, title):
    print(f"\n--- {title} ---")
    result = pd.read_sql(query, conn)
    print(result)
    return result

# ПУНКТ 1.12: Унікальні назви стартових майданчиків
run_query("SELECT DISTINCT LaunchSite FROM SPACEXTABLE", "Унікальні майданчики")

# ПУНКТ 1.9: Загальна кількість успішних та невдалих запусків
run_query("SELECT Class, COUNT(*) as Count FROM SPACEXTABLE GROUP BY Class", "Статистика успіху (1=Успіх, 0=Невдача)")

# ПУНКТ 1.12: Середня маса вантажу для кожного майданчика
run_query("""
    SELECT LaunchSite, AVG(PayloadMass) as AveragePayload 
    FROM SPACEXTABLE 
    GROUP BY LaunchSite
""", "Середня маса вантажу за майданчиками")

# ПУНКТ 1.12: Успішність запусків у певному часовому проміжку
run_query("""
    SELECT Class, COUNT(*) 
    FROM SPACEXTABLE 
    WHERE FlightNumber BETWEEN 1 AND 20 
    GROUP BY Class
""", "Успішність перших 20 запусків")

conn.close()