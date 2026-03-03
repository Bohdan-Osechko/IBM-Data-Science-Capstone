import sys
import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd
import time

# --- Допоміжні функції для обробки даних ---
def date_time(table_cells):
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    out=''.join([bv for i,bv in enumerate(table_cells.strings) if i%2==0][0:-1])
    return out

def landing_status(table_cells):
    return [i for i in table_cells.strings][0]

def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        pos = mass.find("kg")
        new_mass = mass[0:pos+2] if pos != -1 else mass
    else:
        new_mass = 0
    return new_mass

def extract_column_from_header(row):
    if (row.br): row.br.extract()
    if row.a: row.a.extract()
    if row.sup: row.sup.extract()
    column_name = ' '.join(row.contents)
    if not(column_name.strip().isdigit()):
        return column_name.strip()

# --- Основна логіка ---
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

print("Спроба отримати дані з Вікіпедії...")
try:
    response = requests.get(static_url, headers=headers, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        print("Успішне підключення!")
    else:
        print(f"Помилка 403/404. Спробуйте завантажити сторінку вручну як 'spacex.html'")
        # Спроба відкрити локальний файл, якщо запит не вдався
        with open("spacex.html", "r", encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            print("Використовується локальний файл spacex.html")
except Exception as e:
    print(f"Помилка: {e}. Переконайтеся, що файл spacex.html лежить у папці зі скриптом.")
    sys.exit()

# Пошук таблиць
tables = soup.find_all('table', {'class': 'wikitable'})
launch_table = tables[2] # Таблиця запусків Falcon 9
rows = launch_table.find_all('tr')

# Збір даних
launch_data = []
for row in rows[1:]:
    cells = row.find_all('td')
    if len(cells) < 5:
        continue
    
    dt_list = date_time(cells[0])
    launch_data.append({
        'Date': dt_list[0] if dt_list else None,
        'Time': dt_list[1] if len(dt_list) > 1 else None,
        'Booster Version': booster_version(cells[1]),
        'Launch Site': cells[2].text.strip(),
        'Payload': cells[3].text.strip(),
        'Payload Mass': get_mass(cells[3]),
        'Orbit': cells[4].text.strip(),
        'Customer': cells[5].text.strip() if len(cells) > 5 else None,
        'Landing Status': landing_status(cells[8]) if len(cells) > 8 else "Unknown"
    })

# Створення та збереження результатів
df = pd.DataFrame(launch_data)
print("\n--- Результати скрапінгу ---")
print(df.head())

df.to_csv('spacex_web_scraped.csv', index=False)
print("\nФайл 'spacex_web_scraped.csv' успішно збережено для Критерію 1.7!")