import pandas as pd
import os
from features import engineer_features
from model import train_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")

def load_sipri():
    df = pd.read_excel(os.path.join(RAW_DATA_PATH, "SIPRI-Milex-data-1949-2025_v1.2.xlsx"), sheet_name="Share of GDP",skiprows=5)
    nato_members = ["Albania","Finland","Lithuania","Romania","Belgium",
                "France","Luxembourg","Slovakia","Bulgaria","Germany",
                "Montenegro","Slovenia","Canada","Greece","Netherlands","Spain",
                "Croatia","Hungary","North Macedonia","Sweden","Czechia","Iceland","Norway",
                "Türkiye","Denmark","Italy","Poland","United Kingdom","Estonia",
                "Latvia","Portugal","United States of America"]
    iso_mapping = {
        "Albania": "ALB",
        "Belgium": "BEL",
        "Bulgaria": "BGR",
        "Canada": "CAN",
        "Croatia": "HRV",
        "Czechia": "CZE",
        "Denmark": "DNK",
        "Estonia": "EST",
        "Finland": "FIN",
        "France": "FRA",
        "Germany": "DEU",
        "Greece": "GRC",
        "Hungary": "HUN",
        "Iceland": "ISL",
        "Italy": "ITA",
        "Latvia": "LVA",
        "Lithuania": "LTU",
        "Luxembourg": "LUX",
        "Montenegro": "MNE",
        "Netherlands": "NLD",
        "North Macedonia": "MKD",
        "Norway": "NOR",
        "Poland": "POL",
        "Portugal": "PRT",
        "Romania": "ROU",
        "Slovakia": "SVK",
        "Slovenia": "SVN",
        "Spain": "ESP",
        "Sweden": "SWE",
        'Türkiye': 'TUR',
        'United Kingdom': 'GBR',
        'United States of America': 'USA'

    }
    
    filtered_df = df[df["Country"].isin(nato_members)]
    df_sipri = filtered_df.drop(columns=["Notes"])
    df_sipri= pd.melt(df_sipri, id_vars=["Country"], var_name="year", value_name="spending_pct_gdp")
    df_sipri["Country Code"] = df_sipri["Country"].map(iso_mapping)
    df_sipri["year"] = pd.to_numeric(df_sipri["year"], errors="coerce")
    df_sipri["spending_pct_gdp"] = pd.to_numeric(df_sipri["spending_pct_gdp"], errors="coerce")
    df_sipri["spending_pct_gdp"] = df_sipri["spending_pct_gdp"] * 100
    df_sipri= df_sipri.dropna(subset=["spending_pct_gdp"])
    df_sipri= df_sipri[df_sipri["year"] >= 1995]   
    
    return df_sipri



def load_world_bank():
    df = pd.read_excel(os.path.join(RAW_DATA_PATH,"API_NY.GDP.MKTP.CD_DS2_en_excel_v2_121619.xls"), sheet_name="Data", skiprows=3)
    nato_members = [
    "ALB", "BEL", "BGR", "CAN", "HRV", "CZE", "DNK", "EST", 
    "FIN", "FRA", "DEU", "GRC", "HUN", "ISL", "ITA", "LVA", 
    "LTU", "LUX", "MNE", "NLD", "MKD", "NOR", "POL", "PRT", 
    "ROU", "SVK", "SVN", "ESP", "SWE", "TUR", "GBR", "USA"
]
    filtered_df = df[df["Country Code"].isin(nato_members)]
    df_world_bank = filtered_df.drop(columns=["Indicator Name", "Indicator Code"])
    df_world_bank = pd.melt(df_world_bank, id_vars=["Country Name", "Country Code"], var_name="year", value_name="gdp")
    df_world_bank["year"] = pd.to_numeric(df_world_bank["year"], errors="coerce")
    df_world_bank["gdp"] = pd.to_numeric(df_world_bank["gdp"], errors="coerce")
    df_world_bank = df_world_bank.dropna(subset=["gdp"])
    df_world_bank = df_world_bank[df_world_bank["year"] >= 2000]

    return df_world_bank

def merge_datasets():
    return pd.merge(load_sipri(), load_world_bank(), on=["Country Code", "year"], how="inner").drop(columns=["Country"])

if __name__ == "__main__":
    df_sipri = load_sipri()
    print("SIPRI:", df_sipri.shape)
    print(df_sipri.head())
    
    df_wb = load_world_bank()
    print("World Bank:", df_wb.shape)
    print(df_wb.head())

    df_merged = merge_datasets()
    print("Merged:", df_merged.shape)
    print(df_merged.head())
    print(df_merged.columns.tolist())

    df_merged = merge_datasets()
    df_features = engineer_features(df_merged)
    print(df_features.shape)
    print(df_features.columns.tolist())
    print(df_features.head(20))

    print(df_features[df_features["year"] == 2001].head(10))
    print(df_features[df_features["year"] == 2002].head(5))

    model, mae, r2 = train_model(df_features)
    print(f"MAE: {mae:.4f}")
    print(f"R2: {r2:.4f}")