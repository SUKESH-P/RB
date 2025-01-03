def fetch_bus_details(route_name, fare_range):
    price_conditions = {
        "50-1000": "Price BETWEEN 50 AND 1000",
        "1000-2000": "Price BETWEEN 1000 AND 2000",
        "2000 and above": "Price > 2000"
    }

    query = f"""
        SELECT * FROM bus_details
        WHERE {price_conditions[fare_range]} AND Route_name=%s
        ORDER BY Price DESC
    """

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (route_name,))
            results = cursor.fetchall()
            columns = ["ID", "Bus_name", "Bus_type", "Start_time", "End_time",
                       "Total_duration", "Price", "Seats_Available", "Ratings",
                       "Route_link", "Route_name"]
            if results:  # Check if the query returned results
                return pd.DataFrame(results, columns=columns)
            else:
                return pd.DataFrame()  # Return an empty DataFrame if no results
        except mysql.connector.Error as e:
            st.error(f"Error fetching data: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    else:
        return pd.DataFrame()  # Return an empty DataFrame if the connection fails
