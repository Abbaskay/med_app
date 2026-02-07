import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Define paths
MODEL_PATH = os.path.join('app', 'models', 'diabetes_model.joblib')
SCALER_PATH = os.path.join('app', 'models', 'diabetes_scaler.joblib')
DATA_PATH = os.path.join('app', 'data', 'diabetes.csv')

def load_and_preprocess_data():
    """Load and preprocess the diabetes dataset"""
    # If the dataset doesn't exist, download it
    if not os.path.exists(DATA_PATH):
        # Using the Pima Indians Diabetes dataset
        url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
        column_names = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
                        'insulin', 'bmi', 'diabetes_pedigree', 'age', 'outcome']
        
        # Download and save the dataset
        diabetes_data = pd.read_csv(url, names=column_names)
        
        # Handle missing values (0 in some columns represents missing data)
        # For numerical columns like blood pressure, 0 is not a valid value
        zero_not_accepted = ['glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi']
        for column in zero_not_accepted:
            diabetes_data[column] = diabetes_data[column].replace(0, np.nan)
            # Fill missing values with median
            diabetes_data[column] = diabetes_data[column].fillna(diabetes_data[column].median())
        
        # Save processed data
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        diabetes_data.to_csv(DATA_PATH, index=False)
    else:
        diabetes_data = pd.read_csv(DATA_PATH)
    
    # Prepare features and target
    X = diabetes_data.drop('outcome', axis=1)
    y = diabetes_data['outcome']
    
    return X, y

def train_diabetes_model():
    """Train a model to predict diabetes"""
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
    print(f"Diabetes Model Accuracy: {accuracy:.2f}")
    print(classification_report(y_test, y_pred))
    
    # Save the model and scaler
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    
    return model, scaler

def predict_diabetes(input_data):
    """Predict diabetes probability based on input features"""
    # Load the model and scaler
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        model, scaler = train_diabetes_model()
    else:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
    
    # Scale the input data
    input_scaled = scaler.transform(input_data)
    
    # Predict probability
    probabilities = model.predict_proba(input_scaled)[0]
    prediction = int(model.predict(input_scaled)[0])
    
    # Return prediction (0=No Diabetes, 1=Diabetes) and probability
    probability = probabilities[1] if prediction == 1 else probabilities[0]
    
    return prediction, round(float(probability * 100), 2) 