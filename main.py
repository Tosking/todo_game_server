#!/usr/bin/env python3

from flask import Flask
from flask_cors import CORS
import API_recieve as api_rec
from flask_jwt_extended import JWTManager
from config import Config as cfg

app = Flask(__name__)
cors = CORS(app)
app.config["JWT_SECRET_KEY"] = cfg.SECRET_KEY
app.config['CORS_HEADERS'] = 'Content-Type'

jwt = JWTManager(app)
app.register_blueprint(api_rec.app)

if __name__ == "__main__":
    app.run(debug=True)
