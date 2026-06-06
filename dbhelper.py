import psycopg2

class DB:
    def __init__(self):
        try:
            # Internal Render database URL for live deployment
            self.conn = psycopg2.connect("postgresql://admin:8s8njfthGPcPfmihNoFGOvf7qkleaGu6@dpg-d8hgnof7f7vs73chs7ag-a/flights_9aks")
            self.mycursor = self.conn.cursor()
            print('Connection established')
        except Exception as e:
            print(f'Connection error: {e}')

    def fetch_city_names(self):
        city = []
        self.mycursor.execute("""
        SELECT DISTINCT(dest) FROM flight_data
        UNION
        SELECT DISTINCT(origin) FROM flight_data
        """)
        data = self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
        return city

    def fetch_all_flights(self, source, destination):
        self.mycursor.execute("""
        SELECT carrier, flight, dep_time, air_time, price FROM flight_data
        WHERE origin = %s AND dest = %s
        """, (source, destination))
        data = self.mycursor.fetchall()
        return data

    def fetch_airline_frequency(self):
        airline = []
        frequency = []
        self.mycursor.execute("""
        SELECT carrier, COUNT(*) FROM flight_data
        GROUP BY carrier
        """)
        data = self.mycursor.fetchall()
        for item in data:
            airline.append(item[0])
            frequency.append(item[1])
        return airline, frequency

    def busy_airport(self):
        city = []
        frequency = []
        self.mycursor.execute("""
        SELECT t.airport, COUNT(*) FROM (
            SELECT origin AS airport FROM flight_data
            UNION ALL
            SELECT dest AS airport FROM flight_data
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
        SELECT time_hour, COUNT(*) FROM flight_data
        GROUP BY time_hour
        """)
        data = self.mycursor.fetchall()
        for item in data:
            date.append(item[0])
            frequency.append(item[1])
        return date, frequency