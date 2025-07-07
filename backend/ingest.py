import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
CSV_PATH = os.getenv("CSV_PATH")

def clean_column_names(columns):
    return [col.strip().replace(" ", "_").replace("/", "_").lower() for col in columns]

def main():
    # Connect to Mongo
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Load CSV
    df = pd.read_csv(CSV_PATH)

    # Clean column names
    df.columns = clean_column_names(df.columns)

    # Drop existing data (optional)
    collection.delete_many({})

    # Convert to dicts and insert
    records = df.to_dict(orient="records")
    collection.insert_many(records)
    print(f"Inserted {len(records)} threats into MongoDB.")

if __name__ == "__main__":
    main()
