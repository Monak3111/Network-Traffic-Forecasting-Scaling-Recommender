# Network-Traffic-Forecasting-Scaling-Recommender
A full-stack web application that simulates and visualizes network bandwidth usage. The project provides historical traffic data along with future bandwidth forecasts through an interactive dashboard.

## Tech Stack

* **Frontend:** React + Vite
* **Backend:** FastAPI (Python)
* **Machine Learning:** XGBoost
* **Data Processing:** Pandas, NumPy
* **Deployment:** Render

## Features

* View historical network bandwidth data
* Generate bandwidth forecasts
* Interactive charts for data visualization
* REST API built with FastAPI
* Responsive React-based user interface

## Project Structure

```
backend/
├── data/
├── models/
├── forecasting.py
├── main.py

frontend/
├── src/
├── public/
└── package.json
```

## Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend will be available at:

```
http://127.0.0.1:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on:

```
http://localhost:5173
```

## Deployment

The application is deployed using **Render**. The frontend communicates with the deployed FastAPI backend through REST API endpoints.

## Future Improvements

* Real-time bandwidth monitoring
* User authentication
* Support for multiple forecasting models
* Export forecasts and reports

## Author

Developed as a full-stack project using React, FastAPI, and XGBoost to demonstrate network traffic forecasting and data visualization.
