import pandas as pd
import os
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
    
    filtered_df = df[df["Country"].isin(nato_members)]
    df_sipri = filtered_df.drop(columns=["Notes"])
    df_sipri= pd.melt(df_sipri, id_vars=["Country"], var_name="year", value_name="spending_pct_gdp")
    df_sipri["year"] = pd.to_numeric(df_sipri["year"], errors="coerce")
    df_sipri["spending_pct_gdp"] = pd.to_numeric(df_sipri["spending_pct_gdp"], errors="coerce")
    df_sipri["spending_pct_gdp"] = df_sipri["spending_pct_gdp"] * 100
    df_sipri= df_sipri.dropna(subset=["spending_pct_gdp"])
    df_sipri= df_sipri[df_sipri["year"] >= 2000]   
    
    return df_sipri

if __name__ == "__main__":
    df = load_sipri()
    print(df.head())
    print(df.shape)