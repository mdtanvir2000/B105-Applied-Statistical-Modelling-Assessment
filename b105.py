# -*- coding: utf-8 -*-

import pandas as pd

# Load the dataset
file_path = '/content/clean_data.csv'  # Update with the correct path
data = pd.read_csv(file_path)

# Basic overview
print("Dataset Info:")
print(data.info())

print("\nDataset Preview:")
print(data.head())

# Summary statistics
print("\nSummary Statistics:")
print(data.describe())

"""Exploratory Data Analysis (EDA)"""

import matplotlib.pyplot as plt
import seaborn as sns

# Histograms for numerical features
data.hist(bins=30, figsize=(15, 10))
plt.suptitle('Distribution of Numerical Features')
plt.show()

# Boxplots for numerical features
for column in data.select_dtypes(include=['float64', 'int64']).columns:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x=data[column])
    plt.title(f'Boxplot for {column}')
    plt.show()

# Select only numerical columns
numerical_data = data.select_dtypes(include=['float64', 'int64'])

# Calculate the correlation matrix
correlation_matrix = numerical_data.corr()

# Plot the correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

"""Data Preprocessing"""

# Check missing values
print("Missing Values:")
print(data.isnull().sum())

# Handle missing values (example: mean/mode imputation)
for col in data.select_dtypes(include=['float64', 'int64']).columns:
    data[col].fillna(data[col].mean(), inplace=True)

for col in data.select_dtypes(include=['object']).columns:
    data[col].fillna(data[col].mode()[0], inplace=True)

# Detect and handle outliers using IQR
for col in data.select_dtypes(include=['float64', 'int64']).columns:
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]

from sklearn.preprocessing import LabelEncoder, StandardScaler

# Encode categorical variables
label_encoders = {}
for col in data.select_dtypes(include=['object']).columns:
    label_encoders[col] = LabelEncoder()
    data[col] = label_encoders[col].fit_transform(data[col])

# Scale numerical features
scaler = StandardScaler()
numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

# Preview processed data
print("\nProcessed Data Preview:")
print(data.head())

"""Split Dataset"""

# Define features (X) and target (y)
X = data.drop(columns=['Weekly_Sales'])  # Drop the target column from features
y = data['Weekly_Sales']  # Target variable

# Split into training and testing sets
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(f"Training Set Shape: {X_train.shape}")
print(f"Testing Set Shape: {X_test.shape}")

"""Statistical Testing"""

from scipy.stats import pearsonr

# Select numerical columns
numerical_columns = X.select_dtypes(include=['float64', 'int64']).columns

# Test correlations with the target variable
print("Pearson Correlation with Weekly_Sales:")
for col in numerical_columns:
    correlation, p_value = pearsonr(X[col], y)
    print(f"{col}: Correlation={correlation:.4f}, P-value={p_value:.4f}")

from scipy.stats import ttest_ind

# Group by a binary categorical variable
group1 = y[X['IsHoliday'] == 0]  # Non-holiday sales
group2 = y[X['IsHoliday'] == 1]  # Holiday sales

# Perform t-test
t_stat, p_value = ttest_ind(group1, group2)
print(f"T-test for IsHoliday: t-statistic={t_stat:.4f}, p-value={p_value:.4f}")

from scipy.stats import f_oneway

# Group by categorical variable
groups = [y[X['Type'] == value] for value in X['Type'].unique()]

# Perform ANOVA
f_stat, p_value = f_oneway(*groups)
print(f"ANOVA for Type: F-statistic={f_stat:.4f}, p-value={p_value:.4f}")

from scipy.stats import chi2_contingency

# Create a contingency table
contingency_table = pd.crosstab(X['IsHoliday'], X['Type'])

# Perform Chi-square test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)
print(f"Chi-square Test: chi2={chi2:.4f}, p-value={p_value:.4f}, degrees of freedom={dof}")

from scipy.stats import shapiro

# Test normality of the target variable
stat, p_value = shapiro(y)
print(f"Shapiro-Wilk Test for Normality: Statistic={stat:.4f}, P-value={p_value:.4f}")


from scipy.stats import levene

# Test equal variance for holiday and non-holiday sales
stat, p_value = levene(group1, group2)
print(f"Levene Test for Homoscedasticity: Statistic={stat:.4f}, P-value={p_value:.4f}")

""" Model Building"""

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Train a Linear Regression Model (replace with your model choice)
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Model Performance: MSE={mse}, R²={r2}")

""" Linear Regression"""

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Initialize the model
lr_model = LinearRegression()

# Train the model
lr_model.fit(X_train, y_train)

# Predict on the test set
y_pred_lr = lr_model.predict(X_test)

# Evaluate the model
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

print(f"Linear Regression: MSE={mse_lr:.4f}, R²={r2_lr:.4f}")

"""Decision Tree Regression"""

from sklearn.tree import DecisionTreeRegressor

# Initialize the model
dt_model = DecisionTreeRegressor(random_state=42)

# Train the model
dt_model.fit(X_train, y_train)

# Predict on the test set
y_pred_dt = dt_model.predict(X_test)

# Evaluate the model
mse_dt = mean_squared_error(y_test, y_pred_dt)
r2_dt = r2_score(y_test, y_pred_dt)

print(f"Decision Tree Regression: MSE={mse_dt:.4f}, R²={r2_dt:.4f}")

""" Gradient Boosting Regression"""

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Initialize Gradient Boosting model
gb_model = GradientBoostingRegressor(random_state=42, n_estimators=100, learning_rate=0.1)

# Train the model
gb_model.fit(X_train, y_train)

# Predict on the test set
y_pred_gb = gb_model.predict(X_test)

# Evaluate the model
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)

print(f"Gradient Boosting Regression: MSE={mse_gb:.4f}, R²={r2_gb:.4f}")

"""Compare Model Performance"""

# Create a performance summary
performance = {
    "Model": ["Linear Regression", "Decision Tree","Gradient Boosting" ],
    "MSE": [mse_lr, mse_dt, mse_gb],
    "R²": [r2_lr, r2_dt, r2_gb]
}

import pandas as pd
performance_df = pd.DataFrame(performance)
print(performance_df)

"""Visualize Predictions"""

import matplotlib.pyplot as plt

# Actual vs Predicted for Gradient Boosting (best model)
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_gb, alpha=0.7, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', linewidth=2)
plt.title("Actual vs Predicted: Gradient Boosting")
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.show()

"""For Classification Tasks"""

# # Logistic Regression
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# # Initialize the model
# log_reg = LogisticRegression(random_state=42)

# # Train the model
# log_reg.fit(X_train, y_train)

# # Predict on the test set
# y_pred_log = log_reg.predict(X_test)

# # Evaluate the model
# accuracy = accuracy_score(y_test, y_pred_log)
# print(f"Logistic Regression Accuracy: {accuracy:.4f}")

# # Confusion Matrix and Classification Report
# print("Confusion Matrix:")
# print(confusion_matrix(y_test, y_pred_log))
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred_log))

# Define threshold for classification (e.g., median of Weekly_Sales)
threshold = y_train.median()

# Convert target variable into binary categories
y_train_class = (y_train >= threshold).astype(int)
y_test_class = (y_test >= threshold).astype(int)

print(f"Classes in Training Set: {y_train_class.unique()}")
print(f"Classes in Test Set: {y_test_class.unique()}")

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Initialize Logistic Regression
log_reg = LogisticRegression(random_state=42)

# Train the model
log_reg.fit(X_train, y_train_class)

# Predict on the test set
y_pred_log = log_reg.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test_class, y_pred_log)
print(f"Logistic Regression Accuracy: {accuracy:.4f}")

# Confusion Matrix and Classification Report
print("Confusion Matrix:")
print(confusion_matrix(y_test_class, y_pred_log))
print("\nClassification Report:")
print(classification_report(y_test_class, y_pred_log))

"""Feature Importances (Decision Tree or Gradient Boosting)"""

import seaborn as sns

# Feature importances for Gradient Boosting
feature_importance = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': gb_model.feature_importances_
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance)
plt.title('Feature Importance: Gradient Boosting')
plt.show()
