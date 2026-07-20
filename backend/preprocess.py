import numpy as np
import pandas as pd


def preprocess_production(df, feature_columns):
    """
    Preprocess input data for the Production Forecast model.
    """

    df = df.copy()

    # Convert date
    if "DATEPRD" in df.columns:
        df["DATEPRD"] = pd.to_datetime(df["DATEPRD"])

        df["YEAR"] = df["DATEPRD"].dt.year
        df["MONTH"] = df["DATEPRD"].dt.month
        df["DAY"] = df["DATEPRD"].dt.day
        df["DAY_OF_WEEK"] = df["DATEPRD"].dt.dayofweek

    # Replace infinities
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Keep only required features
    X = df[feature_columns].copy()

    # Fill missing values
    X = X.fillna(X.median(numeric_only=True))

    return X