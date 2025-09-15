from arpit_restaurantAPP import app
from model.special_model import special_model
from flask import request
special_model  = special_model()

@app.route("/customer/recommendation/<cid>")

def recommendation_controller(cid):
    data =request.form
    return special_model.recommendation_model(cid,data)


