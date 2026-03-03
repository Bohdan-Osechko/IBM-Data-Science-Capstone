import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

# Функція для побудови матриці плутанини (необхідно для презентації)
def plot_confusion_matrix(y, y_predict, title):
    cm = confusion_matrix(y, y_predict)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='g', cmap='Blues')
    plt.xlabel('Передбачено (Predicted labels)')
    plt.ylabel('Реально (True labels)')
    plt.title(f'Confusion Matrix: {title}')
    plt.show()

# 1. Завантаження та підготовка даних
data = pd.read_csv('dataset_part_2.csv')
# Створюємо ознаки (One Hot Encoding)
features = data[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
X = pd.get_dummies(features)
Y = data['Class'].to_numpy()

# 2. Стандартизація
transform = preprocessing.StandardScaler()
X_scaled = transform.fit_transform(X)

# 3. Розподіл на Train/Test (тестова вибірка 20%)
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)

# 4. Налаштування моделей та Гіперпараметрів
# Logistic Regression
lr_params = {"C": [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
lr_cv = GridSearchCV(LogisticRegression(), lr_params, cv=10).fit(X_train, Y_train)

# SVM
svm_params = {'kernel': ['linear', 'rbf', 'poly', 'sigmoid'], 'C': [0.5, 1, 1.5]}
svm_cv = GridSearchCV(SVC(), svm_params, cv=10).fit(X_train, Y_train)

# Decision Tree
tree_params = {'criterion': ['gini', 'entropy'], 'splitter': ['best', 'random'], 'max_depth': [4, 8, 12]}
tree_cv = GridSearchCV(DecisionTreeClassifier(), tree_params, cv=10).fit(X_train, Y_train)

# KNN
knn_params = {'n_neighbors': [3, 5, 7, 10], 'algorithm': ['auto'], 'p': [1, 2]}
knn_cv = GridSearchCV(KNeighborsClassifier(), knn_params, cv=10).fit(X_train, Y_train)

# 5. Порівняння результатів
results = {
    "Logistic Regression": lr_cv.best_score_,
    "SVM": svm_cv.best_score_,
    "Decision Tree": tree_cv.best_score_,
    "KNN": knn_cv.best_score_
}

print("\n--- Точність моделей (Best Score) ---")
for name, score in results.items():
    print(f"{name}: {score:.4f}")

# 6. Визначення найкращої моделі на тестових даних
best_model_name = max(results, key=results.get)
print(f"\nНайкраща модель: {best_model_name}")

# 7. Візуалізація результатів для презентації
# Матриця для Logistic Regression (найчастіша вимога IBM)
yhat = lr_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat, "Logistic Regression")

# Стовпчикова діаграма точності
plt.bar(results.keys(), results.values(), color='skyblue')
plt.ylabel('Accuracy')
plt.title('Comparison of ML Models Performance')
plt.xticks(rotation=45)
plt.show()