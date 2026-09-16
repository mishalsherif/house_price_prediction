# KeralaPriceAI

A machine learning-based web application for predicting residential property prices across Kerala, India.

KeralaPriceAI uses property characteristics such as location, area, BHK, bathrooms, property age, parking, furnishing, road access, gated community status, and distance from the city center to estimate the expected property price.

## Overview

Property prices in Kerala vary significantly depending on location, property characteristics, accessibility, and surrounding infrastructure. KeralaPriceAI provides a simple interface where users can enter property details and receive an estimated price using a trained machine learning model.

The project combines:

* Machine Learning
* Data preprocessing
* Feature engineering
* Flask
* HTML, CSS and JavaScript
* Scikit-learn
* Pandas and NumPy
* Model serialization with Joblib

## Key Features

* Kerala-focused property price prediction
* District and locality-based selection
* Dynamic locality dropdowns
* Machine learning prediction using Ridge Regression
* Numerical and categorical feature preprocessing
* One-hot encoding for categorical variables
* Feature scaling using StandardScaler
* REST API endpoint for predictions
* Input validation
* Indian Rupee price formatting
* Model evaluation using R², MAE and RMSE
* Dataset analysis utilities
* Ready for deployment using Gunicorn and Render

## Machine Learning Approach

The project uses a supervised regression approach.

### Algorithm

**Ridge Regression**

Ridge Regression was selected to predict continuous property prices while helping control the effect of correlated features through L2 regularization.

### Preprocessing

The machine learning pipeline consists of:

1. Separating numerical and categorical features
2. Standardizing numerical features using `StandardScaler`
3. Encoding categorical features using `OneHotEncoder`
4. Combining the processed features using `ColumnTransformer`
5. Training the Ridge Regression model
6. Evaluating predictions on a separate test set
7. Saving the complete pipeline using Joblib

The dataset is divided into:

* 80% training data
* 20% testing data

A fixed random state is used to make the training process reproducible.

## Input Features

The model uses the following property attributes:

### Location Features

* District
* Locality
* Area Type
* Distance to City Center

### Property Features

* Property Type
* Area in square feet
* BHK
* Number of Bathrooms
* Property Age
* Floor
* Parking Spaces

### Additional Features

* Furnishing
* Road Access
* Gated Community

## Dataset

The project includes a research-informed synthetic dataset containing **5,000 Kerala property records**.

The primary dataset is:

`data/kerala_property_price_research_informed_5000.csv`

An additional locality price reference file is included:

`data/kerala_locality_price_reference_2026.csv`

### Important Note

The dataset is research-informed and synthetic. It is intended for machine learning development, experimentation, demonstration, and educational purposes.

Therefore, the predictions should be treated as **indicative estimates rather than official market valuations or real-estate appraisals**.

## Project Structure

```text
kerala-house-price-prediction/
│
├── analysis/
│   └── dataset_analysis.py
│
├── data/
│   ├── kerala_locality_price_reference_2026.csv
│   └── kerala_property_price_research_informed_5000.csv
│
├── models/
│   ├── kerala_house_price_model.pkl
│   └── metadata.json
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── templates/
│   └── index.html
│
├── tests/
│   └── check_metadata_dropdowns.py
│
├── training/
│   └── train_model.py
│
├── app.py
├── requirements.txt
├── render.yaml
├── runtime.txt
└── README.md
```

## Application Architecture

```text
User
  |
  v
Web Interface
  |
  v
Flask Application
  |
  +------ /metadata
  |
  +------ /predict
             |
             v
      Pre-trained ML Pipeline
             |
             v
       Ridge Regression
             |
             v
      Estimated Property Price
```

## API

The application provides a prediction endpoint:

```text
POST /predict
```

The endpoint accepts property information in JSON format and returns the predicted price along with model evaluation metrics.

Example request:

```json
{
  "District": "Ernakulam",
  "Locality": "Kakkanad",
  "Area_Type": "Urban",
  "Property_Type": "Apartment",
  "Area_sqft": 1500,
  "BHK": 3,
  "Bathrooms": 3,
  "Property_Age_Years": 5,
  "Parking_Spaces": 2,
  "Furnishing": "Semi-Furnished",
  "Floor": 5,
  "Distance_to_City_Center_km": 8,
  "Road_Access": "Good",
  "Gated_Community": "Yes"
}
```

Example response:

```json
{
  "success": true,
  "price": 7500000,
  "formatted": "₹75,00,000",
  "model": "Ridge Regression"
}
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/kerala-house-price-prediction.git
cd kerala-house-price-prediction
```

Replace `your-username` with your GitHub username.

### 2. Create a virtual environment

For Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Train the Model

To train the model from the provided dataset:

```bash
python training/train_model.py
```

This generates:

```text
models/kerala_house_price_model.pkl
models/metadata.json
```

The training script also calculates:

* R² Score
* Mean Absolute Error
* Root Mean Squared Error

## Run the Application

Start the Flask server:

```bash
python app.py
```

The application will be available at:

```text
http://localhost:5000
```

Open the address in your browser to use the prediction system.

## Model Evaluation

The model is evaluated using three standard regression metrics.

### R² Score

Measures how well the model explains variation in property prices.

Higher values generally indicate a better fit.

### Mean Absolute Error

Measures the average absolute difference between the predicted and actual prices.

Lower values indicate smaller prediction errors.

### Root Mean Squared Error

Measures prediction error while giving greater weight to larger errors.

Lower values indicate better predictive performance.

The latest evaluation values are automatically stored in:

```text
models/metadata.json
```

This makes the README independent of hard-coded model metrics that may change after retraining.

## Data Analysis

The project includes a dataset analysis script:

```bash
python analysis/dataset_analysis.py
```

This script can be used to inspect the dataset and generate summary information for understanding property price patterns and feature distributions.

## Technologies Used

| Technology   | Purpose                         |
| ------------ | ------------------------------- |
| Python       | Core programming language       |
| Flask        | Backend web framework           |
| Scikit-learn | Machine learning                |
| Pandas       | Data processing                 |
| NumPy        | Numerical computation           |
| Matplotlib   | Data analysis and visualization |
| Joblib       | Model serialization             |
| HTML         | Web structure                   |
| CSS          | User interface styling          |
| JavaScript   | Frontend interaction            |
| Gunicorn     | Production server               |
| Render       | Deployment                      |

## Future Improvements

Potential improvements for future versions include:

* Training with real-world property transaction data
* Adding more property-related features
* Comparing multiple regression algorithms
* Hyperparameter optimization
* Cross-validation
* Advanced location-based feature engineering
* Interactive price visualization
* Map-based property selection
* Historical price trend analysis
* Model explainability using SHAP
* Automated model retraining
* Database integration
* User authentication and saved predictions

## Limitations

This project is primarily designed for educational and demonstration purposes.

The current dataset is synthetic and research-informed, so the predictions may not represent actual market prices for individual properties.

Property prices can also change based on factors that are not included in the dataset, including:

* Exact property condition
* Land value
* Building quality
* Neighborhood development
* Current market demand
* Property documentation
* Nearby facilities
* Road and transportation improvements
* Economic conditions

For real-world property transactions, professional valuation and current market data should be considered.

## Project Purpose

KeralaPriceAI was developed as a practical machine learning project to demonstrate the complete workflow of building and deploying a regression-based prediction system.

The project covers the process from:

```text
Dataset
   ↓
Data Preprocessing
   ↓
Feature Selection
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Model Serialization
   ↓
Flask API
   ↓
Web Interface
   ↓
Property Price Prediction
```

## License

This project is intended for educational and research purposes.

You may modify and extend the project for learning and experimentation.
