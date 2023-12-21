from flask import Flask, render_template, request
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def index():
    print(request.path)
    return render_template('index.html')


app.run(debug=True)
