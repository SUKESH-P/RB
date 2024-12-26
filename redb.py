pip install mysql.connector
import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu

# Function to load routes from CSV files
def load_routes(file_mapping):
    routes = {}
    for state, file_name in file_mapping.items():
        try:
            df = pd.read_csv(file_name)
            routes[state] = df["Route_name"].tolist()
        except FileNotFoundError:
            st.warning(f"File {file_name} not found for {state}.")
            routes[state] = []
    return routes

# Database connection function
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Amphi@55",
            database="RED_BUS_DETAILS"
        )
    except mysql.connector.Error as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Query execution function
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
            return pd.DataFrame(results, columns=columns)
        except mysql.connector.Error as e:
            st.error(f"Error fetching data: {e}")
            return pd.DataFrame()
        finally:
            conn.close()

# File mapping for routes
file_mapping = {
    "Kerala": "df_k.csv",
    "Andhra Pradesh": "df_a.csv",
    "Telangana": "df_t.csv",
    "Karnataka": "df_kt.csv",
    "Rajasthan": "df_r.csv",
    "Sikkim": "df_sb.csv",
    "Haryana": "df_h.csv",
    "Assam": "df_as.csv",
    "Uttar Pradesh": "df_up.csv",
    "West Bengal": "df_wb.csv"
}

# Load routes
state_routes = load_routes(file_mapping)

# Streamlit app configuration
st.set_page_config(layout="wide")

# Sidebar navigation
web = option_menu(
    menu_title="OnlineBus",
    options=["Home", "States and Routes"],
    icons=["house", "info_circle"],
    orientation="horizontal"
)

# Home page
if web == "Home":
    st.title("Redbus Data Scraping")
    st.subheader(":blue[Domain:] Transportation")
    st.subheader(":blue[Objective:]")
    st.markdown("Provides Comprehensive solution for bus information.")
    st.subheader(":blue[Overview:]")
    st.markdown("- Selenium is used for Web scraping.")
    st.markdown("- Data processing is done using Pandas.")
    st.subheader(":blue[Skills Used:]")
    st.markdown("Selenium, Python, Pandas, MySQL, Streamlit")

# States and Routes page
elif web == "States and Routes":
    state = st.selectbox("Select a State", list(state_routes.keys()))
    route = st.selectbox("Select a Route", state_routes[state])
    fare_range = st.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))

    if st.button("Fetch Details"):
        with st.spinner("Fetching bus details..."):
            bus_data = fetch_bus_details(route, fare_range)
            if not bus_data.empty:
                st.dataframe(bus_data)
            else:
                st.warning("No bus details found for the selected criteria.")

