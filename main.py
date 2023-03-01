#!/usr/bin/env python3

from flask import Flask
import API_recieve as api_rec
from flask_jwt_extended import JWTManager
from config import Config as cfg
app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = cfg.SECRET_KEY

jwt = JWTManager(app)
app.register_blueprint(api_rec.app)

@app.route("/")
def hello():
    return "HEllo!"

if __name__ == "__main__":
    app.run(debug=True)
