from flask import Flask, request, jsonify
import os
import requests
import json
import geojson
from shapely.geometry import shape
import traceback
import logging

app = Flask(__name__)

username = os.environ["GBDX_USER"]
password = os.environ["GBDX_PASSWORD"]

@app.route("/search", methods=["POST"])
def search():
    try:
        inputGeojson = request.get_json(force=True)
        searchCatlogs(inputGeojson)
        return jsonify(inputGeojson)
    except Exception:
        logging.error(traceback.format_exc())
        response = jsonify({"message": "An internal server error occurred, error details are logged."})
        response.status_code = 500
        return response

def searchCatlogs(inputGeojson):
    for feature in inputGeojson["features"]:
        aoi = shape(feature["geometry"])
        response = requests.post("https://geobigdata.io/catalog/v2/search",
            headers = {"Authorization": "Bearer " + getAccessToken(), "Content-Type": "application/json"},
            data = json.dumps({"searchAreaWkt": aoi.wkt}))
        searchResult = response.json()
        catalogs = [catalog["properties"] for catalog in searchResult["results"]]
        feature["properties"]["catalogs"] = catalogs

def getAccessToken():
    response = requests.post("https://geobigdata.io/auth/v1/oauth/token/",
        headers = {"Authorization": "Bearer", "Content-Type": "application/json"},
        data = json.dumps({"grant_type": "password", "username": username, "password": password}))
    token = response.json()
    return token["access_token"]

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
