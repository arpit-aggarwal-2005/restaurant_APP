from arpit_restaurantAPP import app
from flask import request, make_response
from model.feedback_model import FeedbackModel
model = FeedbackModel()

@app.route("/feedback/add", methods=["POST"])
def add_feedback_controller():
    return model.add_feedback()

@app.route("/feedback/restaurant/<int:restaurant_id>", methods=["GET"])
def get_feedback_by_restaurant_controller(restaurant_id):
    model = FeedbackModel()
    return model.get_feedback_by_restaurant(restaurant_id)
