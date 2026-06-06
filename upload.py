import pandas as pd
from sqlalchemy import create_engine, text

try:
    print("1. Loading your local flights.csv.csv file...")
    df = pd.read_csv('flights.csv.csv')

    print("2. Connecting to your Render database via External URL...")
    db_url = "postgresql+psycopg2://admin:8s8njfthGPcPfmihNoFGOvf7qkleaGu6@dpg-d8hgnof7f7vs73chs7ag-a.oregon-postgres.render.com/flights_9aks"
    engine = create_engine(db_url)

    print("3. Clearing table collisions...")
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS flight_data CASCADE;"))
        conn.commit()

    print("4. Uploading rows in high-speed batches to flight_data...")
    df.to_sql('flight_data', engine, if_exists='replace', index=False, chunksize=10000, method='multi')
    print("🎉 Data uploaded successfully! Your database is populated.")

except Exception as e:
    print(f"❌ An error occurred during upload: {e}")