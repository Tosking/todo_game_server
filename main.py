#!/usr/bin/env python3
from flask import Flask
import API_recieve as api_rec

app = Flask(__name__)
app.register_blueprint(api_rec.app)

@app.route("/")
def hello():
    return "HEllo!"

if __name__ == "__main__":
    app.run(debug=True)
