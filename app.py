from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from app.models.heart_disease import train_heart_disease_model, predict_heart_disease
from app.models.diabetes import train_diabetes_model, predict_diabetes

# Get the absolute path to the templates directory
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app', 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'predictive-health-analytics-secret-key')
app.config['UPLOAD_FOLDER'] = 'app/data/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize and train models
def initialize_models():
    train_heart_disease_model()
    train_diabetes_model()

# Add the current date to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/heart-disease')
def heart_disease():
    return render_template('heart_disease.html')

@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')

@app.route('/predict/heart-disease', methods=['POST'])
def predict_heart():
    if request.method == 'POST':
        # Get form data
        age = float(request.form['age'])
        sex = int(request.form['sex'])
        cp = int(request.form['cp'])
        trestbps = float(request.form['trestbps'])
        chol = float(request.form['chol'])
        fbs = int(request.form['fbs'])
        restecg = int(request.form['restecg'])
        thalach = float(request.form['thalach'])
        exang = int(request.form['exang'])
        oldpeak = float(request.form['oldpeak'])
        slope = int(request.form['slope'])
        ca = int(request.form['ca'])
        thal = int(request.form['thal'])
        
        # Prepare input data
        input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, 
                               thalach, exang, oldpeak, slope, ca, thal]])
        
        # Make prediction
        prediction, probability = predict_heart_disease(input_data)
        
        return render_template('heart_disease_result.html', 
                              prediction=prediction,
                              probability=probability)

@app.route('/predict/diabetes', methods=['POST'])
def predict_diab():
    if request.method == 'POST':
        # Get form data
        pregnancies = float(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        blood_pressure = float(request.form['bloodpressure'])
        skin_thickness = float(request.form['skinthickness'])
        insulin = float(request.form['insulin'])
        bmi = float(request.form['bmi'])
        diabetes_pedigree = float(request.form['diabetespedigree'])
        age = float(request.form['age'])
        
        # Prepare input data
        input_data = np.array([[pregnancies, glucose, blood_pressure, 
                               skin_thickness, insulin, bmi, 
                               diabetes_pedigree, age]])
        
        # Make prediction
        prediction, probability = predict_diabetes(input_data)
        
        return render_template('diabetes_result.html', 
                              prediction=prediction,
                              probability=probability)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    # Initialize models before running the app (Local development only)
    # in production, models should be pre-trained or trained via a separate build step
    if os.environ.get('FLASK_ENV') == 'development':
        initialize_models()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 