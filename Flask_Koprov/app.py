from flask import Flask
from datetime import datetime
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def hello_RPI():
    return "Hello Flask!" + str('<br/>') + "add '/hello' to the link"

@app.route("/hello")
@app.route("/hello/<name>")
def second_fancy(name=None):
    return render_template("hello_there.html", name=name, date=datetime.now())

@app.route("/api/image")
def getimage():
    return app.send_static_file("IMG-20200529-WA0018.jpg")

@app.route("/api/rpisim")
def rpisim():
    temp = request.args.get('temp')
    press = request.args.get('pressure')
    hum = request.args.get('humidity')
    return render_template('rpidata.html', temp = temp, press=press, hum=hum)

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)