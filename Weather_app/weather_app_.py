'''
The goal of this project is to create a weather app that shows
the current weather conditions and forecast for a specific location.
Here are the steps you can take to create this project:
    - Use the requests library to make an API call to a weather service
      (e.g. OpenWeatherMap) to retrieve the weather data
      for a specific location.
    - Use the json library to parse the JSON data returned by the API call.
    - Use the tkinter library to create a GUI for the app,
      including widgets such as labels, buttons and text boxes.
    - Use the Pillow library to display the weather icons.
    - Use the datetime library to display the current time and date.
'''

import requests
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageTk
import tkinter as tk


def get_weather_data():
    """Retrieve weather data from OpenWeatherMap API."""
    api_key = api_key_entry.get()
    lat = lat_entry.get()
    lon = lon_entry.get()
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        display_weather_data(data)
    except requests.exceptions.RequestException as error:
        handle_error(error)


def update_time():
    """Update the current time label every second."""
    current_time.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    current_time.after(1000, update_time)


def display_weather_data(data):
    """Display weather data in GUI."""
    weather_data = data["weather"][0]
    main = weather_data["main"]
    description = weather_data["description"]
    icon = weather_data["icon"]

    for widget in app.winfo_children():
        if (widget.winfo_class() == 'Label' and
                widget not in (api_key_label, lat_label, lon_label)):
            widget.pack_forget()

    update_time()
    current_time.pack()

    main_label = tk.Label(text=f"Main: {main}")
    main_label.pack()

    description_label = tk.Label(text=f"Description: {description}")
    description_label.pack()

    icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
    try:
        response = requests.get(icon_url)
        image = Image.open(BytesIO(response.content))
        image = image.resize((64, 64), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(image=photo)
        image_label.image = photo
        image_label.pack()
    except requests.exceptions.RequestException as error:
        handle_error(error)


def handle_error(error):
    if isinstance(error, requests.exceptions.Timeout):
        result_label.configure("The API request timed out.")
    elif isinstance(error, requests.exceptions.HTTPError):
        if error.response.status_code == 401:
            result_label.configure("Client error: Unauthorized.")
        else:
            result_label.configure(f"An HTTP error occurred: {error}")
    elif isinstance(error, requests.exceptions.RequestException):
        result_label.configure(f"An error occurred: {error}")


if __name__ == "__main__":
    app = tk.Tk()
    app.title("Weather App")
    app.geometry("400x400")

    api_key_label = tk.Label(text="API Key:")
    api_key_label.pack()

    api_key_entry = tk.Entry()
    api_key_entry.pack()

    lat_label = tk.Label(text="Latitude:")
    lat_label.pack()

    lat_entry = tk.Entry()
    lat_entry.pack()

    lon_label = tk.Label(text="Longitude:")
    lon_label.pack()

    lon_entry = tk.Entry()
    lon_entry.pack()

    result_label = tk.Label(text="")
    result_label.pack()

    current_time = tk.Label(text="", font=("Arial", 12))
    current_time.pack()
    update_time()

    get_weather_button = tk.Button(text="Get Weather", command=get_weather_data)
    get_weather_button.pack()

    app.mainloop()
