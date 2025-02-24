from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "Put Your own API Key here man, Do Not Try to get mine"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city")
    if not city:
        return render_template("index.html", error="Please enter a city name!")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        if weather_data.get("cod") != 200:
            error_message = weather_data.get("message", "Unknown error")
            return render_template("index.html", error=f"Error: {error_message}")

        print("JSON:", weather_data)
        weather_details = {
            "city": weather_data["name"],
            "temperature": weather_data["main"]["temp"],
            "description": weather_data["weather"][0]["description"],
            "icon": weather_data["weather"][0]["icon"]
        }

        return render_template("weather.html", weather=weather_details)
    except requests.exceptions.RequestException as e:
        return render_template("index.html", error=f"Unable to fetch weather data: {e}")


if __name__ == "__main__":
    app.run(debug=True)
