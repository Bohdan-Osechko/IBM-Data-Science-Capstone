import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import requests

# ==========================================
# 0. ЗАВАНТАЖЕННЯ ТА ПІДГОТОВКА ДАНИХ
# ==========================================
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"
response = requests.get(URL)
response.raise_for_status()
csv_content = io.StringIO(response.text)
df = pd.read_csv(csv_content)

# Підготовка даних
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

print('Дані завантажено!')

# ==========================================
# 1. ВІЗУАЛІЗАЦІЇ
# ==========================================

# 1.1: Графік ліній (Продажі за роками)
df_line = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_line, x='Year', y='Automobile_Sales')
plt.title('Зміна середніх продажів автомобілів за роками')
plt.grid(True)
plt.show()

# 1.2: Графік ліній (Реклама vs Продажі без рецесії)
df_no_recession = df[df['Recession'] == 0]
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_no_recession, x='Year', y='Automobile_Sales', label='Sales')
sns.lineplot(data=df_no_recession, x='Year', y='Advertising_Expenditure', label='Ads', color='red')
plt.title('Продажі та витрати на рекламу (без рецесії)')
plt.show()

# 1.3: Стовпчиковий графік (Типи авто: Рецесія vs Без рецесії)
df_bar = df.groupby(['Vehicle_Type', 'Recession'])['Automobile_Sales'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(data=df_bar, x='Vehicle_Type', y='Automobile_Sales', hue='Recession')
plt.title('Середні продажі за типом авто: Рецесія vs Без рецесії')
plt.xticks(rotation=45)
plt.show()

# 1.4: Субграфіки (ВВП: Рецесія vs Без рецесії)
df_recession = df[df['Recession'] == 1]
fig, axs = plt.subplots(1, 2, figsize=(15, 6))
sns.lineplot(data=df_recession, x='Year', y='GDP', ax=axs[0], color='red')
axs[0].set_title('ВВП під час рецесії')
sns.lineplot(data=df_no_recession, x='Year', y='GDP', ax=axs[1], color='blue')
axs[1].set_title('ВВП без рецесії')
plt.tight_layout()
plt.show()

# 1.5: Бульбашковий графік (Сезонність під час рецесії)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_recession, x='Month', y='Automobile_Sales', 
                size='Seasonality_Weight', hue='Seasonality_Weight', 
                sizes=(20, 200), alpha=0.5)
plt.title('Вплив сезонності на продажі під час рецесії')
plt.show()

# 1.6: Графік розсіювання (Ціна vs Продажі під час рецесії)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_recession, x='Price', y='Automobile_Sales')
plt.title('Кореляція: Ціна vs Продажі під час рецесії')
plt.show()

# 1.7: Кругова діаграма (Частка витрат на рекламу)
recession_ads = df.groupby('Recession')['Advertising_Expenditure'].sum()
plt.figure(figsize=(8, 8))
plt.pie(recession_ads, labels=['Без рецесії', 'Рецесія'], autopct='%1.1f%%', startangle=90)
plt.title('Частка витрат на рекламу: Рецесія vs Без рецесії')
plt.show()

# 1.8: Кругова діаграма (Реклама за типом авто під час рецесії)
df_recession_type = df_recession.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
plt.figure(figsize=(8, 8))
plt.pie(df_recession_type, labels=df_recession_type.index, autopct='%1.1f%%', startangle=90)
plt.title('Витрати на рекламу за типом авто під час рецесії')
plt.show()

# 1.9: Комбінований графік (Безробіття та Продажі під час рецесії)
df_unemp = df_recession.groupby('Vehicle_Type')[['unemployment_rate', 'Automobile_Sales']].mean().reset_index()
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(df_unemp['Vehicle_Type'], df_unemp['unemployment_rate'], color='lightgrey', label='Безробіття')
ax1.set_ylabel('Середній рівень безробіття')
ax2 = ax1.twinx()
ax2.plot(df_unemp['Vehicle_Type'], df_unemp['Automobile_Sales'], color='red', marker='o', label='Продажі')
ax2.set_ylabel('Середні продажі', color='red')
plt.title('Вплив безробіття на продажі за типами авто (Рецесія)')
plt.show()