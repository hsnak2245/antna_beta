import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic  # To calculate distances
from datetime import datetime, timedelta

# Define geofence center and radius (in km)
geofence_center = (25.2919, 51.4244)  # Example center: Doha
geofence_radius = 4  # Radius in kilometers

def check_for_help_request():
    try:
        with open("help_request.txt", "r") as file:
            content = file.read()
            if "Location: Latitude" in content:
                start_idx = content.index("Location: Latitude") + len("Location: Latitude")
                lat_lon_raw = content[start_idx:].strip().split(", Longitude: ")
                latitude = float(lat_lon_raw[0].lstrip(": ").strip())
                longitude = float(lat_lon_raw[1].lstrip(": ").strip())
                return content, (latitude, longitude)
            return content, None
    except FileNotFoundError:
        return None, None

# Simulate data for nearby live devices (e.g., emergency vehicles, drones, etc.)
def generate_live_device_data(help_location):
    device_1_location = help_location if help_location else [25.3786863, 51.4848558]  # Default location
    device_data = {
        'device': ['Emergency Vehicle 1', 'Emergency Vehicle 2', 'Drone 1', 'Drone 2'],
        'type': ['Vehicle', 'Vehicle', 'Drone', 'Drone'],
        'location': [
            device_1_location,  # Device 1 location
            [25.3548, 51.1839],  # Within geofence
            [25.2831, 51.5402],  # Outside geofence
            [25.3687, 51.5273]   # Within geofence
        ],
        'status': ['Active', 'Active', 'Inactive', 'Active'],
    }
    return pd.DataFrame(device_data)

# Check for new help request and extract location
help_message, help_location = check_for_help_request()

# Load the live devices data
live_devices_df = generate_live_device_data(help_location)

# Page configuration
st.set_page_config(page_title="First Responder Portal", page_icon="🚑", layout="wide")

# Load custom CSS
def load_css(file_name):
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading CSS file: {e}")

load_css('styles.css')

# Sidebar Content (similar to the customer portal)
with st.sidebar:
    st.markdown("""
        <div class="title-block">
            <h1>🚑 First Responder Portal</h1>
            <p><span class="status-indicator status-active"></span>Active Monitoring</p>
        </div>
    """, unsafe_allow_html=True)

# Main Body Content
st.title("First Responder Dashboard")
st.subheader("📍 Live Devices Nearby")

# Create map
m = folium.Map(location=geofence_center, zoom_start=12, tiles="cartodbpositron")

# Add geofence circle to the map
folium.Circle(
    location=geofence_center,
    radius=geofence_radius * 1000,  # Convert km to meters
    color='blue',
    fill=True,
    fill_opacity=0.2,
    popup="Geofence Area"
).add_to(m)

# Add markers for live devices
for _, device in live_devices_df.iterrows():
    device_location = device['location']
    status_color = 'green' if device['status'] == 'Active' else 'gray'
    folium.Marker(
        location=device_location,
        popup=f"<b>{device['device']}</b><br>Type: {device['type']}<br>Status: {device['status']}",
        icon=folium.Icon(color=status_color)
    ).add_to(m)

    # Check if the device is outside the geofence
    distance_from_center = geodesic(geofence_center, device_location).km
    if distance_from_center > geofence_radius:
        st.error(f"⚠️ {device['device']} has moved out of the geofence! (Distance: {distance_from_center:.2f} km)")

# Add a marker for the help location if available
if help_message:
    st.warning(f"New request: {help_message}")
    if help_location:
        folium.Marker(
            location=help_location,
            popup="Help Request Location",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

# Render the map with dynamic sizing
st_folium(m, width=1000, height=500)

# Additional action section
st.subheader("🛑 Actions")
if st.button("Acknowledge Devices"):
    st.success("Acknowledged all active devices nearby. Action taken!")

# Check for new help request
if help_message:
    st.warning(f"New request: {help_message}")  # Show the help request message
else:
    st.info("No new help requests at the moment.")  # Show if there's no new request
