import sklearn.metrics
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import ML6
from sklearn.model_selection import GridSearchCV

# Define a new grid with RandomForestClassifier parameters
param_grid = {
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [None, 10, 20],
    'classifier__class_weight': [None, 'balanced']
}

# Create and fit the GridSearchCV model with the pipeline from ML6
model = GridSearchCV(ML6.pipeline, param_grid, cv=5)
model.fit(ML6.X_train, ML6.y_train)

# Make predictions
y_pred = model.predict(ML6.X_test)

print(sklearn.metrics.classification_report(ML6.y_test, y_pred))
conf_matrix = sklearn.metrics.confusion_matrix(ML6.y_test, y_pred)

plt.figure()   
sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='d')
plt.title('Confusion Matrix for Logistic Regression')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.show()

coefficients = model.best_estimator_.named_steps['classifier'].coef_[0]

numerical_feature_names = ML6.numerical_features
categorical_feature_names = list(model.best_estimator_.named_steps['preprocessor']
                                     .named_transformers_['cat']
                                     .named_steps['onehot']
                                     .get_feature_names_out(ML6.categorical_features))

feature_names = numerical_feature_names + categorical_feature_names
feature_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Coefficient': coefficients
}).sort_values(by='Coefficient', key=abs, ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Coefficient'].abs(), color='skyblue')
plt.gca().invert_yaxis()
plt.title('Feature Coefficient magnitudes for Logistic Regression model')
plt.xlabel('Coefficient Magnitude')
plt.show()

test_score = model.best_estimator_.score(ML6.X_test, ML6.y_test)
print(f"\nTest set accuracy: {test_score:.2%}")
