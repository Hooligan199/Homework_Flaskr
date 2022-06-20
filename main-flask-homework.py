import random, string
import pandas as pd
import requests
from flask import Flask, request
from faker import Faker

app = Flask(__name__)
fake = Faker()

@app.route("/")
def start():
    return "<h1>Hello</h1>"

@app.route("/requirements/")
def greeting():
    with open("requirements.txt") as file:
        text = ""
        for line in file:
            text += f"<p><b>{line}</b></p>"
    return text

@app.route("/generate-users/")
def generator():
    double_string = ""
    amount = request.args.get('count', default=100, type=int)
    for _ in range(int(amount)):
        double_string += f"<p>{fake.name()} " \
                         f"{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(9))}" \
                         f"@gmail.com</p>"

    return double_string

@app.route("/mean/")
def calculated_csv():
    data = pd.read_csv("hw.csv")
    height_weight = pd.DataFrame(
        data, columns=['Height(Inches)', 'Weight(Pounds)']).values
    total_canti = 0
    total_kilo = 0
    for canti, kilo in height_weight:
        total_canti += canti
        total_kilo += kilo
    return f"<p>Средний вес = {round(total_kilo * 0.454 / 25000)}кг</p>" \
           f"<p>Средний рост(в см) = {round(total_canti * 2.54 / 25000)}см</p>"

@app.route("/space/")
def cosmonauts_online():
    try:
        answer = requests.get("http://api.open-notify.org/astros.json")
    except ConnectionError:
        return "<p>ConnectionError</p>"
    else:
        return f"<p>Сейчас в космосе находиться " \
               f"{answer.json()['number']} человек</p>"


if __name__ == '__main__':
    app.run(debug=True)