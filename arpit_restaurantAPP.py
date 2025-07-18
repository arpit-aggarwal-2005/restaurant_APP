from flask import * 

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/")
def welcome():
    return jsonify({"message": "Restaurant API is running"})
from controller import * 


