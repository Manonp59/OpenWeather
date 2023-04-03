import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import folium
from streamlit_folium import folium_static
import datetime

load_dotenv()
api_key = os.getenv("API_KEY")

# city_name = ["Paris","Marseille","Lyon","Toulouse","Nice","Nantes","Strasbourg","Montpellier","Bordeaux","Lille","Rennes","Reims","Le Havre","Saint-Etienne","Toulon","Grenoble","Dijon","Angers","Nîmes","Villeurbanne"]

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
                "Latitude":weather_data["coord"]["lat"],
                "Longitude":weather_data["coord"]["lon"],
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


@st.cache_data
def get_weather_data_previsions(city):
    weather_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    previsions = {}
    for item in weather_data['list']:
        dt = item['dt_txt']
        temperature = item['main']['temp']
        feels_like = item['main']['feels_like']
        temp_min = item['main']['temp_min']
        temp_max = item['main']['temp_max']
        pressure = item['main']['pressure']
        humidity = item['main']['humidity']
        previsions[dt] = {
            "Température": temperature,
            "Ressenti": feels_like,
            "Temp min": temp_min,
            "Temp max": temp_max,
            "Pression": pressure,
            "Humidité": humidity
        }
    return previsions





def temps_reel():
    st.title("Météo en temps réel")

    city = st.text_input("Entrez le nom de la ville")

    if st.button("Afficher les données météorologiques"):
        weather_data = get_weather_data(city)
        if weather_data:
            st.write(f"Données météorologiques pour {city}")
            style = [{"selector": "table", "props": [("max-width", "100%")]}]
            df = pd.DataFrame.from_dict(weather_data, orient="index", columns=["Valeur"])
            st.write(df.style.set_table_styles(style))
        else:
            st.error("Impossible de récupérer les données météorologiques")
            
    m = folium.Map(location=[46.227638, 2.213749],zoom_start=5)

    weather_data = get_weather_data(city)
    latitude = weather_data["Latitude"]
    longitude = weather_data["Longitude"]
    folium.Marker(
    location = [latitude,longitude],
    popup = city,).add_to(m)
    

    folium_static(m)
    

def previsions():
    st.title("Prévisions")

    city = st.text_input("Entrez le nom de la ville")

    if st.button("Afficher les données météorologiques"):
        weather_data = get_weather_data_previsions(city)
        if weather_data is not None:
            st.write(f"Données météorologiques pour {city}")
            st.dataframe(weather_data)
        else:
            st.error("Impossible de récupérer les données météorologiques")
            
    m = folium.Map(location=[46.227638, 2.213749],zoom_start=5)

    weather_data = get_weather_data(city)
    latitude = weather_data["Latitude"]
    longitude = weather_data["Longitude"]
    folium.Marker(
    location = [latitude,longitude],
    popup = city,).add_to(m)
    

    folium_static(m)

            

if __name__ == "__main__":
    # Créer des onglets
    tabs = ["En temps réel", "Prévisions"]
    page = st.sidebar.selectbox("Sélectionner une page", tabs)

    # Générer un identifiant unique pour chaque page
    selected_page = hash(page)

    # Définir les paramètres d'URL pour chaque page
    params = {"page": selected_page}

    # Mettre à jour l'URL avec les paramètres sélectionnés
    st.experimental_set_query_params(**params)

    # Afficher le contenu de la page sélectionnée
    if page == "En temps réel":
        temps_reel()
    elif page == "Prévisions":
        previsions()


    