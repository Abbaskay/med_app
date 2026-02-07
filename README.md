# HealthPredict - AI Medical Risk Assessment

HealthPredict is a modern, AI-powered web application designed to assess the risk of **Heart Disease** and **Diabetes**. Built with Flask and Scikit-Learn, it features a premium, responsive UI and uses machine learning models trained on clinical datasets to provide instant risk probability scores.

<img width="1792" height="1120" alt="Screenshot 2026-02-07 at 3 50 57 PM" src="https://github.com/user-attachments/assets/db0fff4e-df1d-4b21-921a-823a70d9dc8f" />

Dashboard of the app



##  Features

-   **Heart Disease Prediction**: Analyzes 13 clinical markers (age, CP, trestbps, chol, etc.) to estimate cardiovascular risk.
-   **Diabetes Risk Assessment**: Uses standard parameters (glucose, BMI, insulin, etc.) to predict Type 2 Diabetes probability.
-   **Premium UI/UX**:
    -   Fully responsive design with a "Medical Blue" & Teal theme.
    -   Glassmorphism header and smooth animations.
    -   Interactive risk gauges and actionable health recommendations.
-   **Secure & Private**: All data is processed locally within the session; no personal health info is permanently stored.

##  Tech Stack

-   **Backend**: Python, Flask, Gunicorn
-   **ML/Data**: Scikit-learn, Pandas, NumPy, Joblib
-   **Frontend**: HTML5, CSS3 (Custom Design System), JavaScript (Chart.js for visualizations)
-   **Deploy**: Ready for Render.com

##  Installation & Local Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/medapp.git
    cd medapp
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**:
    ```bash
    # Development mode (auto-trains models if missing)
    python app.py
    ```
    
    Or use Gunicorn (Production simulation):
    ```bash
    gunicorn app:app
    ```

5.  **Access the app**:
    Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

##  Deployment

This project is configured for seamless deployment on **Render.com**.

See [DEPLOY.md](DEPLOY.md) for detailed step-by-step deployment instructions.

##  Models & Datasets

-   **Heart Disease**: Trained on the [Cleveland Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/heart+disease).
-   **Diabetes**: Trained on the [Pima Indians Diabetes Database](https://www.kaggle.com/uciml/pima-indians-diabetes-database).

##  License

This project is open-source and available under the [MIT License](LICENSE).

---
*Disclaimer: HealthPredict is an educational tool and demonstration of AI in healthcare. It is not a substitute for professional medical diagnosis or treatment.*
