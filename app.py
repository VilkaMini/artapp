from flask import Flask, request
from typing import List
import json
import pickle
import numpy as np
import psycopg2
import os

db_connection = psycopg2.connect(
    database=os.environ.get("DATABASE"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port="5432",
)
cur = db_connection.cursor()

try:
    cur.execute(
        """CREATE TABLE history(
            id serial primary key, 
            artist varchar(100), 
            type varchar(50),
            title varchar(200),
            year int,
            category varchar(100),
            medium varchar(100),
            size_y int,
            size_x int,
            size_z int,
            price int);
        """
    )
    db_connection.commit()
except:
    pass

SAVED_MODEL_PATH = "art_model.pkl"
model = pickle.load(open(SAVED_MODEL_PATH, "rb"))

app = Flask(__name__)


def process_data(data: dict) -> List:
    return data


@app.route("/price/", methods=["POST"])
def price_predict() -> str:
    if request.method == "POST":
        db_connection.commit()
        try:
            try:
                features = process_data(json.loads(request.data))  # send dict
            except:
                return (
                    json.dumps({"error": "CHECK IF INPUT IS FORMATED CORRECTLY"}),
                    400,
                )
            predictions = model.predict(features)
            return json.dumps({"predicted": predictions.tolist()}), 200
        except:
            return json.dumps({"error": "MODEL FAILED TO PREDICT THE PRICE"}), 400
    else:
        return json.dumps({"error": "METHOD NOT ALLOWED"}), 405


@app.route("/history/", methods=["GET"])
def history() -> str:
    if request.method == "GET":
        db_connection.commit()
        cur.execute(f"SELECT * FROM history ORDER BY id DESC LIMIT 10")
        rows = cur.fetchall()
        return json.dumps(
            [
                {
                    "artist": rows[1],
                    "type": rows[2],
                    "title": rows[3],
                    "year": rows[4],
                    "category": rows[5],
                    "medium": rows[6],
                    "size_y": rows[7],
                    "size_x": rows[8],
                    "size_z": rows[9],
                    "price": rows[10],
                }
            ]
        )
    else:
        return json.dumps({"error": "METHOD NOT ALLOWED"}), 405


if __name__ == "__main__":
    app.run(debug=True)
