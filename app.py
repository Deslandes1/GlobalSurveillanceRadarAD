import requests
import streamlit as st
import pandas as pd
from datetime import datetime, timezone

def fetch_real_aircraft_data():
    """Fetch live aircraft data from the OpenSky Network API."""
    url = "https://opensky-network.org/api/states/all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        states = data.get("states", [])
        if not states:
            st.info("No live aircraft data received from OpenSky API.")
            return pd.DataFrame()
        # Convert to DataFrame for easy handling
        columns = [
            "icao24", "callsign", "origin_country", "time_position", "last_contact",
            "longitude", "latitude", "altitude", "on_ground", "velocity", "heading",
            "vertical_rate", "sensors"
        ]
        aircraft_df = pd.DataFrame(states, columns=columns)
        # Keep only relevant columns and aircraft with valid positions
        aircraft_df = aircraft_df[aircraft_df["longitude"].notna() & aircraft_df["latitude"].notna()]
        aircraft_df["callsign"] = aircraft_df["callsign"].str.strip()
        aircraft_df["last_contact_time"] = pd.to_datetime(aircraft_df["last_contact"], unit='s', utc=True)
        return aircraft_df
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching real-time flight data: {e}")
        return pd.DataFrame()
