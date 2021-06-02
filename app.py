from flask import Flask, request
import json
import pickle
import numpy as np
import psycopg2
import os
import pandas as pd

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


def process_data(data: dict) -> pd.DataFrame:
    try:
        df = pd.DataFrame({"year": [data["year"]]})
    except:
        return {"error": "CHECK IF YEAR FIELD IS PROVIDED AND CORRECT"}
    try:
        df["size_y"] = data["size_y"]
        df["size_x"] = data["size_x"]
        df["size_z"] = data["size_z"]
    except:
        return {"error": "CHECK IF ALL SIZES FIELDS ARE PROVIDED AND CORRECT"}
    try:
        df[["enc_type_1", "enc_type_2"]] = enc_type.transform(
            np.array(data["type"]).reshape(-1, 1)
        )
    except:
        return {"error": "CHECK IF TYPE FIELD IS PROVIDED AND CORRECT"}
    try:
        df[
            [
                "enc_category_1",
                "enc_category_2",
                "enc_category_3",
                "enc_category_4",
                "enc_category_5",
            ]
        ] = enc_category.transform(np.array(data["category"]).reshape(-1, 1))
    except:
        return {"error": "CHECK IF CATEGORY FIELD IS PROVIDED AND CORRECT"}
    try:
        df[
            [
                "enc_medium_1",
                "enc_medium_2",
                "enc_medium_3",
                "enc_medium_4",
                "enc_medium_5",
                "enc_medium_6",
                "enc_medium_7",
                "enc_medium_8",
                "enc_medium_9",
                "enc_medium_10",
                "enc_medium_11",
                "enc_medium_12",
                "enc_medium_13",
                "enc_medium_14",
                "enc_medium_15",
            ]
        ] = enc_medium.transform(np.array(data["medium"]).reshape(-1, 1))
    except:
        return {"error": "CHECK IF MEDIUM FIELD IS PROVIDED AND CORRECT"}
    try:
        df[
            [
                "enc_condition_1",
                "enc_condition_2",
                "enc_condition_3",
                "enc_condition_4",
                "enc_condition_5",
            ]
        ] = enc_condition.transform(np.array(data["condition"]).reshape(-1, 1))
    except:
        return {"error": "CHECK IF CONDITION FIELD IS PROVIDED AND CORRECT"}
    return df


@app.route("/price", methods=["POST"])
def price_predict() -> str:
    if request.method == "POST":
        db_connection.commit()
        try:
            try:
                data = json.loads(request.data.decode("utf-8"))
                features = process_data(data)
                if "error" in features.keys():
                    return (
                        json.dumps({"error": features["error"]}),
                        400,
                    )
            except:
                return (
                    json.dumps({"error": "CHECK IF INPUT IS FORMATED CORRECTLY"}),
                    400,
                )
            predictions = model.predict(features)
            # Database filling
            try:
                cur.execute(f"""
                             INSERT INTO history(type, year, category, medium, size_y, size_x, size_z, price)
                             VALUES ('{data['type']}', {data['year']}, '{data['category']}', '{data['medium']}', {data['size_y']}, {data['size_x']}, {data['size_z']}, {predictions[0]})
                             """)
                db_connection.commit()
            except Exception as e:
                print(e)
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
        print(rows)
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
