import streamlit as st
from backend import *
import plotly.express as px

st.title("Weather Forecast")

place = st.text_input("Enter the location:")

days = st.slider(
    "Forecast days", min_value=1, max_value=7, help="Select the number of forecast days"
)

option = st.selectbox("Select the data view", ("Temperature", "Sky"))

st.subheader(f"{option} for the next {days} days in {place}")

if place:
    filtered_data = get_data(place, days)

    if option == "Temperature":
        temperature = [item["main"]["temp"] for item in filtered_data]
        dates = [item["dt_txt"] for item in filtered_data]
        figure = px.line(
            x=dates, y=temperature, labels={"x": "Date", "y": "Temperature (C)"}
        )
        st.plotly_chart(figure)

    if option == "Sky":
        images = {
            "Clear": "./images/clear.png",
            "Clouds": "./images/cloud.png",
            "Rain": "./images/rain.png",
            "Snow": "./images/snow.png",
        }
        sky_conditions = [item["weather"][0]["main"] for item in filtered_data]
        image_paths = [images[condition] for condition in sky_conditions]
        st.image(image_paths, width=115)

