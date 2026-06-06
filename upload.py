import pandas as pd
from sqlalchemy import create_engine

try:
    print("1. Loading your local flights.csv.csv file...")
    df = pd.read_csv('flights.csv.csv')

    print("2. Connecting to your Render database via External URL...")
    # This is your real, raw external connection string formatted for SQLAlchemy
    db_url = "postgresql+psycopg2://admin:8s8njfthGPcPfmihNoFGOvf7qkleaGu6@dpg-d8hgnof7f7vs73chs7ag-a.oregon-postgres.render.com/flights_9aks"
    engine = create_engine(db_url)

    print("3. Uploading rows to Render PostgreSQL (this might take a moment)...")
    df.to_sql('flights', engine, if_exists='replace', index=False)
    print("🎉 Data uploaded successfully! Your database is populated.")

except Exception as e:
    print(f"❌ An error occurred during upload: {e}")