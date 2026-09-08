# KeralaPriceAI

KeralaPriceAI is a Kerala-focused house price prediction web app. It trains a Ridge Regression model on the provided research-informed synthetic dataset and serves a simple Flask web UI and API to estimate property prices.

Features
- Preprocessing pipeline with OneHotEncoder + StandardScaler
- Ridge Regression model (scikit-learn)
- Dynamic District → Locality dropdowns derived from dataset
- Frontend with prediction form and result card
- Dataset analysis script producing summary statistics

Quickstart

1. Create and activate virtualenv

Windows:

```
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Train model

```
python training/train_model.py
```

This creates `models/kerala_house_price_model.pkl` and `models/metadata.json`.

4. Run the app

```
python app.py
```

Open http://localhost:5000

Project structure
- `app.py` — Flask backend and /predict API
- `training/train_model.py` — training script that preprocesses, trains and saves model + metadata
- `data/kerala_property_price_research_informed_5000.csv` — provided dataset
- `models/` — model and metadata output
- `templates/index.html` — frontend template
- `static/` — CSS and JS
- `analysis/dataset_analysis.py` — dataset summary + charts helper

Limitations & Notes
- Dataset is research-informed synthetic; predictions are indicative only.
- Road Access and categorical options are read from the CSV dynamically.

