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
            type varchar(20),
            year int,
            category varchar(20),
            medium varchar(30),
            size_y int,
            size_x int,
            size_z int,
            price int);
        """
    )
    db_connection.commit()
except:
    pass

model = pickle.load(open("regression_model.pkl", "rb"))
enc_type = pickle.load(open("encoder_type", "rb"))
enc_category = pickle.load(open("encoder_category", "rb"))
enc_medium = pickle.load(open("encoder_medium", "rb"))
enc_condition = pickle.load(open("encoder_condition", "rb"))

app = Flask(__name__)


def process_data(data: json) -> List: # write function
    print(data)
    return data


@app.route("/price", methods=["POST"])
def price_predict() -> str:
    if request.method == "POST":
        db_connection.commit()
        try:
            try:
                features = process_data(request.data.decode('utf-8'))  # send dict
            except:
                return (
                    json.dumps({"error": "CHECK IF INPUT IS FORMATED CORRECTLY"}),
                    400,
                )
            predictions = model.predict(features)
            # Database filling
            return json.dumps({"predicted": predictions.tolist()}), 200
        except:
            return json.dumps({"error": "MODEL FAILED TO PREDICT THE PRICE"}), 400
    else:
        return json.dumps({"error": "METHOD NOT ALLOWED"}), 405


@app.route("/history/", methods=["GET"])
def history() -> str:
    if request.method == "GET":
        db_connection.commit()
        try:
            cur.execute(f"SELECT * FROM history ORDER BY id DESC LIMIT 10")
        except:
            return json.dumps({"error": "COULD NOT RETRIEVE RECORDS"}), 400
        rows = cur.fetchall()
        return json.dumps(
            [
                {
                    "type": rows[1],
                    "year": rows[2],
                    "category": rows[3],
                    "medium": rows[4],
                    "size_y": rows[5],
                    "size_x": rows[6],
                    "size_z": rows[7],
                    "price": rows[8],
                }
            ]
        )
    else:
        return json.dumps({"error": "METHOD NOT ALLOWED"}), 405


if __name__ == "__main__":
    app.run(debug=True)
