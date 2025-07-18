from arpit_restaurantAPP import app
from flask import request, jsonify
from model.menu_model import menu_model
from model.dish_model import dish_model

# Create model instances
menu_obj = menu_model()
dish_obj = dish_model()

# Add menu
@app.route("/menu/add", methods=["POST"])
def add_menu_controller():
    data = request.form.to_dict()
    return menu_obj.add_menu(data)

# Get all menus
@app.route("/menu/getall", methods=["GET"])
def get_all_menus_controller():
    return menu_obj.get_all_menus()

# Get menus by restaurant
@app.route("/menu/restaurant/<rid>", methods=["GET"])
def get_menus_by_restaurant_controller(rid):
    return menu_obj.get_menus_by_restaurant(rid)

# Update menu
@app.route("/menu/update", methods=["PUT"])
def update_menu_controller():
    data = request.form.to_dict()
    return menu_obj.update_menu(data)

# Delete menu
@app.route("/menu/delete/<id>", methods=["DELETE"])
def delete_menu_controller(id):
    return menu_obj.delete_menu(id)

# Patch menu
@app.route("/menu/patch/<id>", methods=["PATCH"])
def patch_menu_controller(id):
    return menu_obj.patch_menu(id, request.form)




