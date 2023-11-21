import math
from flask import render_template, request, redirect, session, jsonify
from app import app, login
import dao
from flask_login import login_user
from app.models import User


@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    cates = dao.load_categories()
    products = dao.load_products(kw, cate_id)

    return render_template("homesite.html", categories=cates, products=products)


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == 'GET':
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(username == username, password == password).first()
        if user:
            login_user(user=user)
    return redirect("/admin")


@app.route('/api/cart', methods=["POST"])
def app_cart():
    cart = session.get('cart')
    if cart is None:
        cart = {}

    data = request.json
    id = str(data.get("id"))

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }
    session['cart'] = cart

    return jsonify({
        "total_quantity": 10,
        'total_price': 100
    })


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    from app import admin

    app.run(debug=True)
