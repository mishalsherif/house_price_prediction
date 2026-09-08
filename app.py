import json
import os
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_from_directory
import joblib
import numpy as np

ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "models"
MODEL_PATH = MODELS_DIR / "kerala_house_price_model.pkl"
METADATA_PATH = MODELS_DIR / "metadata.json"

app = Flask(__name__, template_folder="templates", static_folder="static")

# load metadata (if present)
metadata = {}
if METADATA_PATH.exists():
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

# lazy load model
_model = None

def load_model():
    global _model
    if _model is None:
        if MODEL_PATH.exists():
            _model = joblib.load(MODEL_PATH)
        else:
            raise FileNotFoundError("Model not found. Train model first: python -m training.train_model")
    return _model


def format_inr(x: float) -> str:
    # Simple Indian grouping
    try:
        x = int(round(x))
    except Exception:
        return str(x)
    s = str(x)[::-1]
    parts = [s[:3]]
    s = s[3:]
    while s:
        parts.append(s[:2])
        s = s[2:]
    return "₹" + ",".join(parts)[::-1]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/metadata")
def get_metadata():
    # Return metadata for frontend dropdowns
    if METADATA_PATH.exists():
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify({"success": True, "metadata": data})
    return jsonify({"success": False, "error": "metadata not found"}), 404


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json()
    if not payload:
        return jsonify({"success": False, "error": "Invalid JSON payload"}), 400

    # Basic validation
    required = [
        "District",
        "Locality",
        "Area_Type",
        "Property_Type",
        "Area_sqft",
        "BHK",
        "Bathrooms",
        "Property_Age_Years",
        "Parking_Spaces",
        "Furnishing",
        "Floor",
        "Distance_to_City_Center_km",
        "Road_Access",
        "Gated_Community",
    ]

    for k in required:
        if k not in payload:
            return jsonify({"success": False, "error": f"Missing field: {k}"}), 400

    # Numeric checks
    try:
        area = float(payload["Area_sqft"])
        bhk = int(payload["BHK"])
        baths = int(payload["Bathrooms"])
        age = float(payload["Property_Age_Years"])
        parking = int(payload["Parking_Spaces"])
        dist = float(payload["Distance_to_City_Center_km"])
    except Exception as e:
        return jsonify({"success": False, "error": "Invalid numeric values"}), 400

    if area <= 0:
        return jsonify({"success": False, "error": "Area_sqft must be > 0"}), 400
    if bhk < 1:
        return jsonify({"success": False, "error": "BHK must be >= 1"}), 400
    if baths < 1:
        return jsonify({"success": False, "error": "Bathrooms must be >= 1"}), 400
    if age < 0:
        return jsonify({"success": False, "error": "Property_Age_Years cannot be negative"}), 400
    if parking < 0:
        return jsonify({"success": False, "error": "Parking_Spaces cannot be negative"}), 400
    if dist < 0:
        return jsonify({"success": False, "error": "Distance_to_City_Center_km cannot be negative"}), 400

    # Validate categorical membership where possible
    md = metadata or {}
    # District -> Locality check
    district_localities = md.get("district_localities", {})
    district = payload["District"]
    locality = payload["Locality"]
    if district_localities and district not in district_localities:
        return jsonify({"success": False, "error": "Unknown District"}), 400
    if district_localities and locality not in district_localities.get(district, []):
        return jsonify({"success": False, "error": "Locality does not belong to selected District"}), 400

    # Prepare input dataframe for model
    import pandas as pd

    input_df = pd.DataFrame([payload])

    # Load model
    try:
        model = load_model()
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    # Predict
    try:
        pred = model.predict(input_df)[0]
    except Exception as e:
        return jsonify({"success": False, "error": "Model prediction failed: " + str(e)}), 500

    formatted = format_inr(pred)

    resp = {
        "success": True,
        "price": float(pred),
        "formatted": formatted,
        "model": md.get("model_name", "Ridge Regression"),
        "r2": md.get("metrics", {}).get("r2"),
        "mae": md.get("metrics", {}).get("mae"),
        "rmse": md.get("metrics", {}).get("rmse"),
    }
    return jsonify(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
