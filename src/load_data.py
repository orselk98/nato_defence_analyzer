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
    
if __name__ == "__main__":
    df_sipri = load_sipri()
    print("SIPRI:", df_sipri.shape)
    print(df_sipri.head())
    
    df_wb = load_world_bank()
    print("World Bank:", df_wb.shape)
    print(df_wb.head())