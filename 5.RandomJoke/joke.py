from flask import Blueprint, render_template, url_for, request, redirect, jsonify
import requests


joke_bp = Blueprint("joke", __name__)
API = "Get Your OWN API KEY Bro"  # API Ninjas Api Key
URL = "https://api.api-ninjas.com/v1/jokes"

@joke_bp.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        response = requests.get(URL, headers={"X-Api-Key": API})
        if response.status_code == 200:
            joke = response.json()[0]["joke"]
            return jsonify({"joke": joke})
        else:
            return jsonify({"error": f"Error: {response.status_code}, {response.text}"})
    return render_template("index.html")