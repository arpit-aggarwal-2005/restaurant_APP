from arpit_restaurantAPP import app
from flask import request
from model.restaurant_model import restaurant_model
from model.dish_model import dish_model
dish = dish_model()
rest_obj = restaurant_model()


@app.route("/restaurant/add", methods=["POST"])
def restaurant_add_controller():
    data = request.form.to_dict()
    return rest_obj.add_restaurant(data)


@app.route("/restaurant/getall", methods=["GET"])
def restaurant_getall_controller():
    return rest_obj.get_all_restaurants()


@app.route("/restaurant/owner/<owner_id>", methods=["GET"])
def restaurant_by_owner_controller(owner_id):
    return rest_obj.get_restaurants_by_owner(owner_id)

# 🔹 Update entire restaurant (name, cuisine, location, owner_id)
@app.route("/restaurant/update", methods=["PUT"])
def restaurant_update_controller():
    data = request.form.to_dict()
    return rest_obj.update_restaurant(data)

# 🔹 Delete restaurant by ID
@app.route("/restaurant/delete/<id>", methods=["DELETE"])
def restaurant_delete_controller(id):
    return rest_obj.delete_restaurant(id)
@app.route("/restaurant/patch/<id>", methods=["PATCH"])
def restaurant_patch_controller(id):
    return rest_obj.patch_restaurant(id, request.form)
@app.route("/restaurant/<restaurant_id>/dishes", methods=["GET"])
def get_dishes_by_restaurant_controller(restaurant_id):
    return dish.get_all_dishes_by_restaurant_id(restaurant_id)
@app.route("/restaurant/get_report/<rid>")
def get_report_controller(rid):
    return rest_obj.get_report_model(rid)

