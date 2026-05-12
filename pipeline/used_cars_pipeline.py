import kagglehub
import pandas as pd
from pathlib import Path


def extract():
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    
    # https://www.kaggle.com/datasets/taeefnajib/used-car-price-prediction-dataset/data
    path = kagglehub.dataset_download("taeefnajib/used-car-price-prediction-dataset") + '/used_cars.csv'
    df = pd.read_csv(path)

    df.to_csv("data/raw/used_cars.csv", index=False)
    
    return df



def inspect(df):
    print(df.head())
    print(df.info())
    print(df.isnull().sum())
    print(df.describe(include="all"))



def transform(df):
    data = df.copy()

    # normalized columns
    data.columns = data.columns.str.lower().str.strip()

    data = data.rename(columns={ 
        "milage": "mileage",
        "model_year":"year",
    })


    # normalize values
    data["mileage"] = pd.to_numeric(
        data["mileage"]
            .astype(str)
            .str.replace(" mi.", "", regex=False)
            .str.replace(",", "",  regex=False),
        errors="coerce"
    )

    data["price"] = pd.to_numeric(
        data["price"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "",  regex=False),
        errors="coerce"
    )

    # handle missing values
    data["fuel_type"] = data["fuel_type"].fillna("Unknown")
    data["accident"] = data["accident"].fillna("Unknown")
    data["clean_title"] = data["clean_title"].fillna("Unknown")

    # normalize columns
    for col in [ "brand", "model", "fuel_type", "engine", "transmission", "ext_col", "int_col", "accident", "clean_title"]:
        data[col] = data[col].astype(str).str.strip()

    data = data.dropna(subset=["price", "mileage"])

    return data



def load(df):
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df.to_csv("data/processed/used_cars_cleaned.csv", index=False)



def main():

    raw_df = extract()
    inspect(raw_df)
    
    cleaned_df = transform(raw_df)

    load(cleaned_df)


if __name__ == "__main__":
    main()