from flask import Flask, Response, render_template, request
from flask_cors import CORS
import requests
import json
from bs4 import BeautifulSoup
import re


app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def index():
    print(request.path)
    return render_template('index.html')


app.run(debug=True)