import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "kerala_property_price_research_informed_5000.csv"
OUT = ROOT / "analysis" / "analysis_results.json"


def run():
    df = pd.read_csv(DATA_PATH)
    stats = {}
    stats['total_properties'] = int(len(df))
    stats['num_districts'] = int(df['District'].nunique())
    stats['num_localities'] = int(df['Locality'].nunique())
    stats['price_mean'] = float(df['Price_INR'].mean())
    stats['price_min'] = int(df['Price_INR'].min())
    stats['price_max'] = int(df['Price_INR'].max())

    # Average price by district
    stats['avg_price_by_district'] = df.groupby('District')['Price_INR'].mean().sort_values(ascending=False).round(2).to_dict()
    stats['avg_price_by_area_type'] = df.groupby('Area_Type')['Price_INR'].mean().round(2).to_dict()
    stats['count_by_district'] = df['District'].value_counts().to_dict()
    stats['top10_localities_by_price'] = df.groupby('Locality')['Price_INR'].mean().sort_values(ascending=False).head(10).round(2).to_dict()

    OUT.write_text(json.dumps(stats, indent=2))
    print('Wrote analysis results to', OUT)

if __name__=='__main__':
    run()
