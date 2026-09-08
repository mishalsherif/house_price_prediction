import json
import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "kerala_property_price_research_informed_5000.csv"
MODELS_DIR = ROOT / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)


def load_data(path):
    df = pd.read_csv(path)
    return df


def build_and_train(df):
    # Expected columns (will adapt to actual columns)
    target_col = "Price_INR"

    exclude_cols = ["Property_ID", "Price_Data_Type", "Research_Anchor_Rate_INR_per_sqft"]

    X = df.drop(columns=[target_col] + [c for c in exclude_cols if c in df.columns])
    y = df[target_col]

    # Features to use (ensure they exist)
    categorical_features = [
        f for f in [
            "District",
            "Locality",
            "Area_Type",
            "Property_Type",
            "Furnishing",
            "Road_Access",
            "Gated_Community",
        ] if f in X.columns
    ]

    numeric_features = [
        f for f in [
            "Area_sqft",
            "BHK",
            "Bathrooms",
            "Property_Age_Years",
            "Parking_Spaces",
            "Floor",
            "Distance_to_City_Center_km",
        ] if f in X.columns
    ]

    # Split before preprocessing to avoid leakage
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    # Column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                numeric_features,
            ),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            ),
        ],
        remainder="drop",
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("ridge", Ridge(alpha=1.0, random_state=42)),
        ]
    )

    model.fit(X_train, y_train)

    # Predictions and metrics
    y_pred = model.predict(X_test)
    r2 = float(r2_score(y_test, y_pred))
    mae = float(mean_absolute_error(y_test, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))

    # Save model
    model_path = MODELS_DIR / "kerala_house_price_model.pkl"
    joblib.dump(model, model_path)

    # Build metadata: district->localities, area type per locality, unique categorical lists
    metadata = {}
    metadata["model_path"] = str(model_path.name)
    metadata["model_name"] = "Ridge Regression"
    metadata["metrics"] = {"r2": r2, "mae": mae, "rmse": rmse}

    # District -> Localities mapping
    districts = {}
    if "District" in df.columns and "Locality" in df.columns:
        for d, group in df.groupby("District"):
            districts[d] = sorted(group["Locality"].dropna().unique().tolist())

    metadata["district_localities"] = districts

    # Area type mapping (locality -> most common Area_Type)
    locality_area = {}
    if "Locality" in df.columns and "Area_Type" in df.columns:
        for loc, g in df.groupby("Locality"):
            locality_area[loc] = g["Area_Type"].mode().iloc[0] if not g["Area_Type"].mode().empty else None

    metadata["locality_area_type"] = locality_area

    # Unique values for dropdowns
    for col in ["Property_Type", "Furnishing", "Road_Access", "Gated_Community", "Area_Type"]:
        if col in df.columns:
            metadata[col] = sorted(df[col].dropna().unique().tolist())

    # Basic dataset stats
    metadata["dataset_stats"] = {
        "total_properties": int(len(df)),
        "num_districts": int(len(metadata["district_localities"])),
        "num_localities": int(len(df["Locality"].dropna().unique())) if "Locality" in df.columns else None,
        "price_min": int(df["Price_INR"].min()),
        "price_max": int(df["Price_INR"].max()),
        "price_mean": float(df["Price_INR"].mean()),
    }

    # Save metadata
    metadata_path = MODELS_DIR / "metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("Training complete. Metrics:")
    print(f"R2: {r2:.4f}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"Saved model to: {model_path}")
    print(f"Saved metadata to: {metadata_path}")


def main():
    df = load_data(DATA_PATH)
    build_and_train(df)


if __name__ == "__main__":
    main()
