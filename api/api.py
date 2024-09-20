import pandas as pd
from flask import Flask
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200"])

@app.route("/phones")
def phones():
    phones = pd.read_csv('../data_preparation/phones.csv')
    return phones.to_json(orient="records")

@app.route("/phone", methods=['POST'])
def phone():
    data = request.get_json()
    print(data)
    id = data['id']
    phones = pd.read_csv('../data_preparation/phones.csv')
    phone = phones[phones['id'] == int(id)]
    return phone.to_json(orient="records")

@app.route("/phones_data")
def phones_data():
    phones = pd.read_csv('../data_cleaning/cleaned_data_dropna.csv')
    return phones.to_json(orient="records")