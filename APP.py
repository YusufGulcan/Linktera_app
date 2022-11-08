import numpy as np
import pickle
from flask import Flask, request, render_template
from datetime import datetime
import calendar
import os

app = Flask("__name__")
model = open("lin_reg.pkl", "rb")
model = pickle.load(model)

@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/predictions", methods=["POST"])
def predict():
    Kredi = request.form["Kredi Stok"]
    Parity = request.form["EURO/TRY Paritesi"]
    Faiz = request.form["Faiz Orani"]
    OTV = request.form["OTV"]
    row = [
        round(float(OTV) ** -1, 10),
        round(float(Faiz) ** -1, 10),
        round(float(Parity) ** -1, 10),
        np.log(float(Kredi)),
    ]

    date = request.form["tarih"]
    date = str(date)
    date = datetime.strptime(date, "%Y-%m-%d")
    month_ = calendar.month_name[date.month]
    features_ = np.array(
        ["August", "December", "February", "January", "June", "November"]
    )
    extension = np.where(features_ == month_, 1, 0)
    row.extend(extension)

    prediction = model.predict([np.array(row)])[0]
    minimum_ = 22000
    if prediction < minimum_:                                         # Eger tahmin veri setinin minimum degerinden kucukse linear regresyonun sert hareketini azaltmak icin   
        smoothed_difference = np.sqrt((minimum_ - prediction) ** 2 / minimum_)            # yumusatici bir fonksiyon ile tahminlerin 0'a ve 0'in altina inmesini önlemeye calistim.
        prediction = int(minimum_ - smoothed_difference)

    prediction = int(max(0, prediction))

    return render_template("index.html", result=f" Tahmin edilen: {prediction}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)
