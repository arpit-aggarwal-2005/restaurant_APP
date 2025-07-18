from arpit_restaurantAPP import app
from flask import request, send_file
from datetime import datetime
from model.customer_model import customer_model
from model.auth_model import auth_model

obj = customer_model()
auth = auth_model()

@app.route("/customer/getall")
@auth.auth_token("/customer/getall")
def customer_getall_controller():
    return obj.customer_getall_model()

@app.route("/customer/register", methods=["POST"])
def customer_addone_controller():
    data = request.form.to_dict()
    return obj.customer_addone_model(data)

@app.route("/customer/update", methods=["PUT"])
def customer_update_controller():
    data = request.form.to_dict()
    return obj.customer_update_model(data)

@app.route("/customer/delete/<id>", methods=["DELETE"])
def customer_delete_controller(id):
    return obj.customer_delete_model(id)

@app.route("/customer/patch/<id>", methods=["PATCH"])
def customer_patch_controller(id):
    return obj.customer_patch_model(id, request.form)

@app.route("/customer/getall/limit/<limit>/pages/<page>")
def customer_pagination_controller(limit, page):
    return obj.customer_pagination_model(limit, page)

@app.route("/customer/<uid>/upload", methods=['PUT'])
def customer_upload_controller(uid):
    file = request.files['avatar']
    fileName = file.filename
    timestamp = str(datetime.now().timestamp()).replace('.', '')
    extension = fileName.split('.')[-1]
    new_filename = f"{timestamp}.{extension}"
    file.save(f"uploads/{new_filename}")
    return obj.customer_upload_model(uid, new_filename)

@app.route("/upload/<filename>")
def get_file(filename):
    return send_file(f"uploads/{filename}")

@app.route("/customer/login", methods=['POST'])
def customer_login():
    data = request.form
    return obj.customer_login_model(data)
