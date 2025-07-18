from arpit_restaurantAPP import app
from flask import request
from model.dish_model import dish_model

dish = dish_model()

# Add new dish
@app.route("/dish/add", methods=["POST"])
def add_dish_controller():
    data = request.form.to_dict()
    return dish.add_dish(data)

# Get all dishes
@app.route("/dish/getall", methods=["GET"])
def get_all_dishes_controller():
    return dish.get_all_dishes()

@app.route("/dish/update", methods=["PUT"])
def update_dish_controller():
    data = request.form.to_dict()
    return dish.update_dish(data)

# ✅ Delete a dish by ID
@app.route("/dish/delete/<id>", methods=["DELETE"])
def delete_dish_controller(id):
    return dish.delete_dish(id)

# ✅ Patch (partial update) a dish by ID
@app.route("/dish/patch/<id>", methods=["PATCH"])
def patch_dish_controller(id):
    data = request.form.to_dict()
    return dish.patch_dish(id, data)

# ✅ Get all dishes for a menu
@app.route("/menu/<menu_id>/dishes", methods=["GET"])
def get_dishes_by_menu(menu_id):
    return dish.get_dishes_by_menu(menu_id)