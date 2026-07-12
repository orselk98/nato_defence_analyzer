import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

def train_model(df):
    df = df.dropna(subset=["gdp_growth_rate", "rolling_avg_spending", "benchmark_dev", "spending_yoy_change", "spending_pct_gdp_next_year"])
    X = df[["gdp_growth_rate", "rolling_avg_spending", "benchmark_dev", "spending_yoy_change"]]
    y = df["spending_pct_gdp_next_year"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return model, mae, r2
