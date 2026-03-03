import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
import sklearn.model_selection
from sklearn.metrics import r2_score

# Завантаження даних
df = pd.read_csv('kc_house_data.csv')

# 1.1 Відобразити типи даних кожного стовпця
print("--- 1.1 Dtypes ---")
print(df.dtypes)

# 1.2 Видалити стовпці "id" та "Unnamed: 0"
columns_to_drop = ['id', 'Unnamed: 0']
# Залишаємо тільки ті, що є в DataFrame
existing_columns = [col for col in columns_to_drop if col in df.columns]
df.drop(existing_columns, axis=1, inplace=True)
print("\n--- 1.2 Describe ---")
print(df.describe())

# 1.3 value_counts() для поверхів та перетворення у DataFrame
print("\n--- 1.3 Value Counts ---")
floor_counts = df['floors'].value_counts().to_frame()
print(floor_counts)

# 1.4 seaborn boxplot для порівняння цін (waterfront)
plt.figure(figsize=(10, 6))
sns.boxplot(x='waterfront', y='price', data=df)
plt.title('Ціна будинку в залежності від виду на набережну')
plt.show() # 

# 1.5 seaborn regplot для кореляції sqft_above та price
plt.figure(figsize=(10, 6))
sns.regplot(x='sqft_above', y='price', data=df)
plt.title('Кореляція між sqft_above та ціною')
plt.show() # 

# Підготовка даних для ML (розділення на ознаки та цільову змінну)
X = df[['sqft_living']]
y = df['price']

# 1.6 Лінійна регресія (sqft_living -> price)
lm = LinearRegression()
lm.fit(X, y)
print(f"\n--- 1.6 R^2 (sqft_living): {lm.score(X, y):.4f}")

# 1.7 Лінійна регресія з кількома ознаками
features = ["floors", "waterfront", "lat", "bedrooms", "sqft_basement",
            "view", "bathrooms", "sqft_living15", "sqft_above", "grade",
           "sqft_living"]
X_multi = df[features]
lm_multi = LinearRegression()
lm_multi.fit(X_multi, y)
print(f"--- 1.7 R^2 (multi-feature): {lm_multi.score(X_multi, y):.4f}")

# 1.8 Створення та підготовка конвеєра (pipeline)
Input = [('scale', StandardScaler()), ('polynomial', PolynomialFeatures(degree=2)), ('model', LinearRegression())]
pipe = Pipeline(Input)
pipe.fit(X_multi, y)
print(f"--- 1.8 R^2 (pipeline): {pipe.score(X_multi, y):.4f}")

# Розділення даних на тренувальні та тестові для Ridge
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X_multi, y, test_size=0.15, random_state=1)

# 1.9 Ridge регресія (alpha=0.1)
RidgeModel = Ridge(alpha=0.1)
RidgeModel.fit(x_train, y_train)
yhat_ridge = RidgeModel.predict(x_test)
print(f"--- 1.9 R^2 (Ridge Test): {r2_score(y_test, yhat_ridge):.4f}")

# 1.10 Поліном 2-го порядку + Ridge
pr = PolynomialFeatures(degree=2)
x_train_pr = pr.fit_transform(x_train)
x_test_pr = pr.fit_transform(x_test)
RidgeModel_pr = Ridge(alpha=0.1)
RidgeModel_pr.fit(x_train_pr, y_train)
yhat_pr = RidgeModel_pr.predict(x_test_pr)
print(f"--- 1.10 R^2 (Polynomial Ridge Test): {r2_score(y_test, yhat_pr):.4f}")