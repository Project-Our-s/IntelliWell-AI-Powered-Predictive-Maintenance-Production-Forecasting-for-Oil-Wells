# IntelliWell-AI-Powered-Predictive-Maintenance-Production-Forecasting-for-Oil-Wells
## 📌 Overview

IntelliWell is an AI-powered decision support system developed for the petroleum industry to improve well monitoring, production forecasting, and predictive maintenance.

The system combines Machine Learning, Business Intelligence, and Web Technologies to analyze historical well data, detect pressure anomalies, forecast future production, and provide actionable maintenance recommendations through interactive dashboards.

## 🎯 Objectives
* Predict future oil production using Machine Learning.
* Detect pressure anomalies using unsupervised learning.
* Assess overall well health.
* Generate AI-based maintenance recommendations.
* Build interactive Business Intelligence dashboards.
* Develop an AI prediction simulator using Flask and Streamlit.

## 🛠️ Technology Stack
### Programming
* Python
### Machine Learning
* Scikit-learn
* Random Forest Regressor
* Isolation Forest
### Data Processing
* Pandas
* NumPy
### Visualization
* Matplotlib
### Business Intelligence
* Microsoft Power BI
### Database
* PostgreSQL
### Web Application
* Flask
* Streamlit

## 📂 Project Structure
```
IntelliWell/
│
├── datasets/
│
├── notebooks/
│   ├── Notebook 1 - Production Forecasting.ipynb
│   ├── Notebook 2 - Pressure Anomaly Detection.ipynb
│   ├── Notebook 3 - Well Health Assessment.ipynb
│   ├── Notebook 4 - Future Forecast Generator.ipynb
│
├── backend/
│   ├── app.py
│   ├── routes.py
│   ├── services.py
│   ├── preprocess.py
│   ├── model_loader.py
│   ├── config.py
│
├── frontend/
│   ├── Home.py
│   ├── pages/
│
├── powerbi/
│   ├── IntelliWell.pbix
│
├── sql/
│   ├── Database.sql
│
├── models/
│   ├── production_model.pkl
│   ├── pressure_model.pkl
│   ├── pressure_scaler.pkl
│
├── outputs/
│   ├── future_forecast.csv
│   ├── pressure_anomaly_results.csv
│   ├── well_health_results.csv
│   ├── IntelliWell_Final_Report.csv
│
└── README.md
```
## 📊 Machine Learning Pipeline
```
Historical Well Data
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Random Forest
(Production Forecast)
        │
        ▼
Isolation Forest
(Pressure Anomaly Detection)
        │
        ▼
Well Health Assessment
        │
        ▼
Future Forecast Generator
        │
        ▼
Power BI + Streamlit
```
## 🤖 Machine Learning Models
#### Production Forecasting

Algorithm :
```
Random Forest Regressor
```
Purpose

* Predict future production
* Estimate production decline
* Support production planning

### Pressure Anomaly Detection

Algorithm
```
Isolation Forest
```
Purpose

* Detect abnormal pressure conditions
* Identify potential equipment failures
* Support predictive maintenance

## ❤️ Well Health Assessment

### The health score combines

* Production Performance
* Pressure Stability
* Operational Status

### The system classifies wells into

* Healthy
* Monitor
* Warning
* Critical

and automatically generates maintenance recommendations.

## 📈 Power BI Dashboards
### 1. Executive Overview

Overall KPIs

* Total Production
* Total Wells
* Average Health Score
* Production Trends
### 2. Production Analytics
* Production Trends
* Well Performance
* Field Performance
* Production Distribution
### 3. Pressure Anomaly Analytics
* Pressure Trends
* Anomaly Detection
* Severity Distribution
* Pressure Monitoring
### 4. Well Health Analytics
* Health Scores
* Operational Status
* Maintenance Recommendations
* Risk Assessment
### 5. Operational Intelligence
* Overall Operational Insights
* Performance Comparison
* Executive Reporting
### 6. Future Forecast Analytics
* Future Production Trend
* Expected Anomalies
* Forecast Confidence
* Forecast Health Score
### 7. AI Prediction Simulator

Interactive dashboard allowing users to select

* Forecast Day
* Well
* Field
* Facility

and instantly view

* Predicted Production
* Expected Anomalies
* Well Health Score
* Forecast Confidence
* AI Recommendation

## 🌐 Web Application

The Streamlit application provides an interactive AI interface for:

* Uploading well datasets
* Running production forecasting
* Detecting pressure anomalies
* Viewing well health reports
* Exploring AI-generated predictions

The backend is powered by Flask REST APIs.

## 🗄️ Database

PostgreSQL is used for storing:

* Production Data
* Pressure Data
* Anomaly Results
* Well Health Results
* Forecast Results

 ## 📈 Future Forecasting

The future forecasting engine simulates

* Production decline
* Pressure degradation
* Operational variations

for forecasting horizons ranging from 1 to 365 days. 

## 🚀 Features
* AI-based Production Forecasting
* Pressure Anomaly Detection
* Predictive Maintenance
* Well Health Assessment
* Future Forecast Simulation
* Business Intelligence Dashboards
* Interactive AI Prediction Simulator
* REST API Integration
* SQL Database Integration

  ## 🔮 Future Enhancements
* Real-time IoT sensor integration
* Live production monitoring
* Cloud deployment
* Automated alert notifications
* Deep Learning forecasting models
* Explainable AI (SHAP/LIME)
* Digital Twin integration
* Mobile dashboard support
