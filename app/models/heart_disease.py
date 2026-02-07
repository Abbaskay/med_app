import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Define paths
MODEL_PATH = os.path.join('app', 'models', 'heart_disease_model.joblib')
SCALER_PATH = os.path.join('app', 'models', 'heart_disease_scaler.joblib')
DATA_PATH = os.path.join('app', 'data', 'heart.csv')

def load_and_preprocess_data():
    """Load and preprocess the heart disease dataset"""
    # If the dataset doesn't exist, download it
    if not os.path.exists(DATA_PATH):
        # Using the UCI heart disease dataset
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
        column_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                         'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
        
        # Download and save the dataset
        heart_data = pd.read_csv(url, names=column_names)
        
        # Handle missing values (? in the original dataset)
        heart_data = heart_data.replace('?', np.nan)
        heart_data = heart_data.dropna()
        
        # Convert columns to appropriate data types
        for col in heart_data.columns:
            heart_data[col] = pd.to_numeric(heart_data[col])
        
        # Simplify the target variable (0 = no disease, 1 = disease)
        heart_data['target'] = heart_data['target'].apply(lambda x: 1 if x > 0 else 0)
        
        # Save processed data
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        heart_data.to_csv(DATA_PATH, index=False)
    else:
        heart_data = pd.read_csv(DATA_PATH)
    
    # Prepare features and target
    X = heart_data.drop('target', axis=1)
    y = heart_data['target']
    
    return X, y

def train_heart_disease_model():
    """Train a model to predict heart disease"""
    # Create directory for models if it doesn't exist
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Load and preprocess data
    X, y = load_and_preprocess_data()
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train a Random Forest classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Heart Disease Model Accuracy: {accuracy:.2f}")
    print(classification_report(y_test, y_pred))
    
    # Save the model and scaler
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    
    return model, scaler

def predict_heart_disease(input_data):
    """Predict heart disease probability based on input features"""
    # Load the model and scaler
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        model, scaler = train_heart_disease_model()
    else:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
    
    # Scale the input data
    input_scaled = scaler.transform(input_data)
    
    # Predict probability
    probabilities = model.predict_proba(input_scaled)[0]
    prediction = int(model.predict(input_scaled)[0])
    
    # Return prediction (0=No Heart Disease, 1=Heart Disease) and probability
    probability = probabilities[1] if prediction == 1 else probabilities[0]
    
    return prediction, round(float(probability * 100), 2) 