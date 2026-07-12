import pandas as pd

def engineer_features(df):
    df["benchmark_dev"] = df["spending_pct_gdp"] - 2.0
    df["spending_yoy_change"]= df.groupby("Country Code")["spending_pct_gdp"].diff()
    df["rolling_avg_spending"] = df.groupby("Country Code")["spending_pct_gdp"].rolling(window=3).mean().reset_index(level=0, drop=True)
    df["gdp_growth_rate"] = df.groupby("Country Code")["gdp"].pct_change() * 100
    df=df[df["year"] >= 1995]
    df["spending_pct_gdp_next_year"] = df.groupby("Country Code")["spending_pct_gdp"].shift(-1) #added this line to create a new column for next year's spending percentage of GDP
    return df


