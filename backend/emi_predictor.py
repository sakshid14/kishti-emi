#!/usr/bin/env python
# coding: utf-8

# In[26]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.compose import ColumnTransformer
import numpy as np
from flask import Flask, request, jsonify
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, Request
from models import ProductDataInput



# In[27]:


# app = Flask(__name__)

# router = APIRouter()

app = FastAPI()
# app.include_router(router)

# In[2]:



# --- 1. Load the Dataset ---
try:
    df = pd.read_csv('profit_prediction_dataset.csv')
    print("Dataset loaded successfully.")
    print(f"Number of records: {len(df)}")
    print("\nDataset Head:")
    print(df.head())
    print("\nDataset Info:")
    df.info()
except FileNotFoundError:
    print("Error: 'profit_prediction_dataset.csv' not found.")
    print("Please make sure you have run the dataset generation script first.")
    exit()

# --- 2. Define Features (X) and Target (y) ---
# We'll use relevant features to predict the EMI contribution percentage.
# 'transaction_date' needs to be processed to extract temporal features.
# 'gross_profit_per_unit' and 'profit_percentage' are crucial as EMI contribution
# logic often depends on the actual profit.

# Drop 'record_id' and 'product_id' as they are identifiers, not predictive features.
# 'actual_selling_price', 'cost_price', 'base_selling_price', 'marketing_spend_per_unit',
# 'operational_cost_per_unit', 'discount_percentage', 'competitor_price' directly
# influence gross_profit_per_unit and profit_percentage.
# We include them as they provide granular information that the model can learn from,
# even if profit_percentage is also included.
features = [
    'product_category', 'cost_price', 'base_selling_price', 'season',
    'market_demand', 'marketing_spend_per_unit', 'operational_cost_per_unit',
    'discount_percentage', 'competitor_price', 'transaction_date',
    'actual_selling_price', 'gross_profit_per_unit', 'profit_percentage'
]
target = 'target_emi_contribution_percent_of_profit'

X = df[features]
y = df[target]

# --- 3. Feature Engineering for 'transaction_date' ---
X['transaction_date'] = pd.to_datetime(X['transaction_date'])
X['month'] = X['transaction_date'].dt.month
X['day_of_week'] = X['transaction_date'].dt.dayofweek # Monday=0, Sunday=6
X['day_of_year'] = X['transaction_date'].dt.dayofyear
X['week_of_year'] = X['transaction_date'].dt.isocalendar().week.astype(int) # Using isocalendar for week number
X['quarter'] = X['transaction_date'].dt.quarter
X['year'] = X['transaction_date'].dt.year # May capture trends over years
X = X.drop('transaction_date', axis=1) # Drop original date column

print("\nFeatures after date engineering:")
print(X.head())

# --- 4. Define Column Types for Preprocessing ---
categorical_features = ['product_category', 'season', 'market_demand']
numerical_features = [col for col in X.columns if col not in categorical_features]

print(f"\nCategorical Features: {categorical_features}")
print(f"Numerical Features: {numerical_features}")

# --- 5. Create Preprocessing Pipelines ---
# Numerical pipeline: Impute missing values (if any) and scale
numerical_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Categorical pipeline: Impute missing values (if any) and One-Hot Encode
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore')) # handle_unknown='ignore' for new categories in test set
])

# Create a preprocessor to apply different transformations to different columns
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# --- 6. Build the Full Model Pipeline ---
# The pipeline first preprocesses the data, then applies the RandomForestRegressor
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))])

# --- 7. Split Data into Training and Testing Sets ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTraining set size: {len(X_train)}")
print(f"Testing set size: {len(X_test)}")

# --- 8. Train the Model ---
print("\nTraining the model...")
model.fit(X_train, y_train)
print("Model training complete.")

# --- 9. Make Predictions ---
print("Making predictions on the test set...")
y_pred = model.predict(X_test)

# --- 10. Evaluate the Model ---
print("\n--- Model Evaluation ---")

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R2): {r2:.2f}")

# --- 11. Example Prediction (Optional) ---
print("\n--- Example Prediction ---")
# Let's take the first sample from the test set to demonstrate a prediction
example_data = X_test.iloc[0:1]
actual_emi = y_test.iloc[0]
predicted_emi = model.predict(example_data)[0]

print(f"Actual EMI Contribution for example: {actual_emi:.2f}%")
print(f"Predicted EMI Contribution for example: {predicted_emi:.2f}%")

# You can also create a new input for prediction
# new_product_data = pd.DataFrame([{
#     'product_category': 'Electronics',
#     'cost_price': 1000,
#     'base_selling_price': 1500,
#     'season': 'Summer',
#     'market_demand': 'High',
#     'marketing_spend_per_unit': 50,
#     'operational_cost_per_unit': 80,
#     'discount_percentage': 5,
#     'competitor_price': 1450,
#     'transaction_date': pd.Timestamp('2024-07-20'), # Will be converted to month, day_of_week etc.
#     'actual_selling_price': 1425,
#     'gross_profit_per_unit': 295,
#     'profit_percentage': 20.7
# }])
# # Ensure new data has same engineered features
# new_product_data['month'] = new_product_data['transaction_date'].dt.month
# new_product_data['day_of_week'] = new_product_data['transaction_date'].dt.dayofweek
# new_product_data['day_of_year'] = new_product_data['transaction_date'].dt.dayofyear
# new_product_data['week_of_year'] = new_product_data['transaction_date'].dt.isocalendar().week.astype(int)
# new_product_data['quarter'] = new_product_data['transaction_date'].dt.quarter
# new_product_data['year'] = new_product_data['transaction_date'].dt.year
# new_product_data = new_product_data.drop('transaction_date', axis=1)

# # Predict on new data
# # predicted_new_emi = model.predict(new_product_data)[0]
# # print(f"Predicted EMI Contribution for new product: {predicted_new_emi:.2f}%")


# In[6]:


# new_data_point2 = {
#     'product_category': 'Electronics',
#     'cost_price': 19000.00,
#     'base_selling_price': 21000.00,
#     'season': 'Summer', # Or 'Winter', 'Autumn', 'Spring', 'Festival', 'Monsoon'
#     'market_demand': 'High', # Or 'Low', 'Medium'
#     'marketing_spend_per_unit': 60.00,
#     'operational_cost_per_unit': 100.00,
#     'discount_percentage': 8.00,
#     'competitor_price': 20500.00,
#     'transaction_date': '2025-07-24', # This will be processed by the function
#     'actual_selling_price': 19320.00, # 1800 * (1 - 0.08)
#     'gross_profit_per_unit': 160.00, # 1656 - 1200 - 60 - 100
#     'profit_percentage': 0.83 # (296 / 1656) * 100
# }


# In[10]:


# new_data_point2 = {
#     'product_category': 'Electronics',
#     'cost_price': 60000.00,
#     'base_selling_price': 65000.00,
#     'season': 'Summer', # Or 'Winter', 'Autumn', 'Spring', 'Festival', 'Monsoon'
#     'market_demand': 'High', # Or 'Low', 'Medium'
#     'marketing_spend_per_unit': 0.00,
#     'operational_cost_per_unit': 10.00,
#     'discount_percentage': 5.00,
#     'competitor_price': 63000.00,
#     'transaction_date': '2025-07-24', # This will be processed by the function
#     'actual_selling_price': 61750.00, # 1800 * (1 - 0.08)
#     'gross_profit_per_unit': 1740.00, # 1656 - 1200 - 60 - 100
#     'profit_percentage': 2.8178 # (296 / 1656) * 100
# }


# In[18]:


# new_data_point2 = {
#     'product_category': 'Electronics',
#     'cost_price': 4000.00,
#     'base_selling_price': 5000.00,
#     'season': 'Summer', # Or 'Winter', 'Autumn', 'Spring', 'Festival', 'Monsoon'
#     'market_demand': 'High', # Or 'Low', 'Medium'
#     'marketing_spend_per_unit': 0.00,
#     'operational_cost_per_unit': 0.00,
#     'discount_percentage': 0.00,
#     'competitor_price': 5000.00,
#     'transaction_date': '2025-07-24', # This will be processed by the function
#     'actual_selling_price': 5000.00, # 1800 * (1 - 0.08)
#     'gross_profit_per_unit': 1000.00, # 1656 - 1200 - 60 - 100
#     'profit_percentage': 33.33 # (296 / 1656) * 100
# }


# In[22]:


# new_data_point2 = {
#     'product_category': 'diamond',
#     'cost_price': 20000.00,
#     'base_selling_price': 40000.00,
#     'season': 'Summer', # Or 'Winter', 'Autumn', 'Spring', 'Festival', 'Monsoon'
#     'market_demand': 'High', # Or 'Low', 'Medium'
#     'marketing_spend_per_unit': 0.00,
#     'operational_cost_per_unit': 222.00,
#     'discount_percentage': 25.00,
#     'competitor_price': 45000.00,
#     'transaction_date': '2025-07-24', # This will be processed by the function
#     'actual_selling_price': 30000.00, # 1800 * (1 - 0.08)
#     'gross_profit_per_unit': 9778.00, # 1656 - 1200 - 60 - 100
#     'profit_percentage': 32.5 # (296 / 1656) * 100
# }


# In[23]:


# new_data_point = pd.DataFrame([new_data_point2])


# In[24]:


# new_data_point['transaction_date'] = pd.to_datetime(new_data_point['transaction_date'])
# new_data_point['month'] = new_data_point['transaction_date'].dt.month
# new_data_point['day_of_week'] = new_data_point['transaction_date'].dt.dayofweek # Monday=0, Sunday=6
# new_data_point['day_of_year'] = new_data_point['transaction_date'].dt.dayofyear
# new_data_point['week_of_year'] = new_data_point['transaction_date'].dt.isocalendar().week.astype(int) # Using isocalendar for week number
# new_data_point['quarter'] = new_data_point['transaction_date'].dt.quarter
# new_data_point['year'] = new_data_point['transaction_date'].dt.year # May capture trends over years
# new_data_point = new_data_point.drop('transaction_date', axis=1) 


# predicted_emi = model.predict(new_data_point)[0]


# In[25]:


# predicted_emi


# In[28]:



# @app.post('/predict_emi')
def predict_emi(request: ProductDataInput):


    new_data_point2 = payload
    
    print(new_data_point2)
    
    # new_data_point2 = {
    #     'product_category': 'Electronics',
    #     'cost_price': 20000.00,
    #     'base_selling_price': 40000.00,
    #     'season': 'Summer', # Or 'Winter', 'Autumn', 'Spring', 'Festival', 'Monsoon'
    #     'market_demand': 'High', # Or 'Low', 'Medium'
    #     'marketing_spend_per_unit': 0.00,
    #     'operational_cost_per_unit': 222.00,
    #     'discount_percentage': 25.00,
    #     'competitor_price': 45000.00,
    #     'transaction_date': '2025-07-24', # This will be processed by the function
    #     'actual_selling_price': 30000.00, # 1800 * (1 - 0.08)
    #     'gross_profit_per_unit': 9778.00, # 1656 - 1200 - 60 - 100
    #     'profit_percentage': 32.5 # (296 / 1656) * 100
    # }
    
    
    
    # if not request.json:
    #     return jsonify({"error": "Please send JSON data"}), 400

    
    new_data_point = pd.DataFrame([new_data_point2])
    
    # new_data_point['actual_selling_price']=(1-(0.01*new_data_point['discount_percentage']))*new_data_point['base_selling_price']
    # new_data_point['gross_profit_per_unit']=df['actual_selling_price']-df['cost_price']-df['marketing_spend_per_unit']-df['operational_cost_per_unit']
    # new_data_point['profit_percentage']=(df['gross_profit_per_unit']/df['actual_selling_price'])*100

    new_data_point['transaction_date'] = pd.to_datetime(new_data_point['transaction_date'])
    new_data_point['month'] = new_data_point['transaction_date'].dt.month
    new_data_point['day_of_week'] = new_data_point['transaction_date'].dt.dayofweek # Monday=0, Sunday=6
    new_data_point['day_of_year'] = new_data_point['transaction_date'].dt.dayofyear
    new_data_point['week_of_year'] = new_data_point['transaction_date'].dt.isocalendar().week.astype(int) # Using isocalendar for week number
    new_data_point['quarter'] = new_data_point['transaction_date'].dt.quarter
    new_data_point['year'] = new_data_point['transaction_date'].dt.year # May capture trends over years
    new_data_point = new_data_point.drop('transaction_date', axis=1) 

    try:
        predicted_emi_contribution = model.predict(new_data_point)
        print("1", predicted_emi_contribution[0])
        return jsonify({
            "predicted_emi_contribution_percent_of_profit": (round(float(predicted_emi_contribution), 2) * new_data_point['gross_profit_per_unit'])/100
        })
    except Exception as e:
        # This catch-all is for issues during prediction (e.g., mismatch in columns after preprocessing)
        return jsonify({"error": f"Prediction failed: {e}. Ensure all required input features are present and correct."}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8010)


# In[ ]:




