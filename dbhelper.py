import psycopg2

class DB:
    def __init__(self):
        # connect to the database
        try:
            # Using your Render Internal Database URL
            self.conn = psycopg2.connect("postgresql://admin:8s8njfthGPcPfmihNoFGOvf7qkleaGu6@dpg-d8hgnof7f7vs73chs7ag-a/flights_9aks")
            self.mycursor = self.conn.cursor()
            print('Connection established')
        except Exception as e:
            print(f'Connection error: {e}')

    def fetch_city_names(self):
        city = []
        self.mycursor.execute("""
        SELECT DISTINCT("Destination") FROM flights
        UNION
        SELECT DISTINCT("Source") FROM flights
        """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])

        return city

    def fetch_all_flights(self, source, destination):
        # Using secure parameterized inputs to prevent SQL errors with strings
        self.mycursor.execute("""
        SELECT "Airline", "Route", "Dep_Time", "Duration", "Price" FROM flights
        WHERE "Source" = %s AND "Destination" = %s
        """, (source, destination))

        data = self.mycursor.fetchall()
        return data

    def fetch_airline_frequency(self):
        airline = []
        frequency = []

        self.mycursor.execute("""
        SELECT "Airline", COUNT(*) FROM flights
        GROUP BY "Airline"
        """)

        data = self.mycursor.fetchall()

        for item in data:
            airline.append(item[0])
            frequency.append(item[1])

        return airline, frequency

    def busy_airport(self):
        city = []
        frequency = []

        # Standardized the inner column alias so GROUP BY works perfectly in Postgres
        self.mycursor.execute("""
        SELECT t.airport, COUNT(*) FROM (
            SELECT "Source" AS airport FROM flights
            UNION ALL
            SELECT "Destination" AS airport FROM flights
        ) t
        GROUP BY t.airport
        ORDER BY COUNT(*) DESC
        """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])
            frequency.append(item[1])

        return city, frequency

    def daily_frequency(self):
        date = []
        frequency = []

        self.mycursor.execute("""
        SELECT "Date_of_Journey", COUNT(*) FROM flights
        GROUP BY "Date_of_Journey"
        """)

        data = self.mycursor.fetchall()

        for item in data:
            date.append(item[0])
            frequency.append(item[1])

        return date, frequency