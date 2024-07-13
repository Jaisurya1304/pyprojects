import requests
import streamlit as st

api_key = "fM1gDKJe9xOoekmbkxNIDeb9VXfRwjMALm1eE4l4"

url = "https://api.nasa.gov/planetary/apod?"\
      f"api_key={api_key}"

r1=requests.get(url)
data=r1.json()

title=data["title"]
imageurl=data["url"]
desp=data["explanation"]

imgfp="img.jpg"
r2=requests.get(imageurl)
with open(imgfp,'wb') as f:
    f.write(r2.content)

st.title(title)
st.image(imgfp)
st.write(desp)