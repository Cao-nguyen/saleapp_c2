import hashlib
import math
from flask import render_template, request, redirect, session, jsonify
from app import app, login
import dao, utils
from flask_login import login_user
from app.models import User


# home site
@app.route("/", methods=["get"])
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')  # lay so trang

    cates = dao.load_categories()
    products = dao.load_products(kw, cate_id, page)

    pages = app.config["PAGE_SIZE"]
    total_products = dao.get_count_products()

    cart_count = session['cart']
    if cart_count is None:
        cart_count = 0
    else:
        cart_count = utils.count_product(cart_count)

    page_number = int(math.ceil(total_products / pages))
    return render_template("Homesite.html", cart_count=cart_count, categories=cates, products=products,
                           page_number=page_number)


# login admin
@app.route("/admin/login", methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    print(str(hashlib.md5(str(password).strip().encode('utf-8')).hexdigest()))
    user = auth_user(username=username, password=password)

    if user:
        login_user(user=user)

    return redirect('/admin')


# dua user da authenticate vao session -> current_user
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


def auth_user(username, password):
    username = str(username).strip()
    password = str(hashlib.md5(str(password).strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()


@app.route("/login")
def user_login():
    return render_template("Login.html")


@app.route("/api/cart", methods=["post"])
def add_cart():
    data = request.json
    cart = session.get('cart')

    if cart is None:
        cart = {}
    product_id = str(data.get('id'))
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            "id": product_id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart
    return jsonify(utils.count_product(cart))


if __name__ == "__main__":
    from app import admin

    app.run(debug=True)
