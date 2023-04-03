import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import folium
from streamlit_folium import folium_static

load_dotenv()
api_key = os.getenv("API_KEY")

city_name = ["Paris","Marseille","Lyon","Toulouse","Nice","Nantes","Strasbourg","Montpellier","Bordeaux","Lille","Rennes","Reims","Le Havre","Saint-Etienne","Toulon","Grenoble","Dijon","Angers","Nîmes","Villeurbanne"]

@st.cache_data
def get_weather_data(city):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if geo_response.status_code == 200 and geo_data:
        lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        weather_response = requests.get(weather_url)

        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            return {
                "Longitude": weather_data["coord"]["lon"],
                "Latitude" : weather_data["coord"]["lat"],
                "Température": weather_data["main"]["temp"],
                "Température Min": weather_data["main"]["temp_min"],
                "Température Max": weather_data["main"]["temp_max"],
                "Température ressentie": weather_data["main"]["feels_like"],
                "Pression": weather_data["main"]["pressure"],
                "Humidité": weather_data["main"]["humidity"],
                "Vitesse du vent": weather_data["wind"]["speed"],
                "Direction du vent": weather_data["wind"]["deg"],
                "Levé du soleil": pd.to_datetime(weather_data["sys"]["sunrise"], unit="s"),
                "Coucher du soleil": pd.to_datetime(weather_data["sys"]["sunset"], unit="s")
            }
        else:
            st.error("Une erreur s'est produite lors de la requête à l'API OpenWeather")
    else:
        st.error("La ville spécifiée est introuvable ou une erreur s'est produite lors de la requête à l'API OpenWeather Geo.")


def main():
    st.title("Application météo")
    st.write("En temps réel")
    # latitude = 0
    # longitude = 0
    m = folium.Map(location=[46.227638, 2.213749],zoom_start=5)
    for city in city_name:
        weather_data = get_weather_data(city)
        latitude = weather_data["Latitude"]
        longitude = weather_data["Longitude"]
        popup_html = f"<h3>{city}</h3>"
        popup_html += "<table>"
        for key, value in weather_data.items():
            popup_html += f"<tr><td>{key}</td><td>{value}</td></tr>"
        popup_html += "</table>"
        folium.Marker(
            location = [latitude,longitude],
            popup = popup_html,
        ).add_to(m)
    

    folium_static(m)

if __name__ == "__main__":
    main()
