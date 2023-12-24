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

    page_number = int(math.ceil(total_products / pages))
    return render_template("Homesite.html", categories=cates, products=products,
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
            "image": data.get("image"),
            "quantity": 1
        }

    session['cart'] = cart
    return jsonify(utils.count_product(cart))


@app.route('/api/cart/<product_id>', methods=['delete'])
def remove_product(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart

    return jsonify(utils.count_product(cart))


@app.route('/api/cart/<product_id>', methods=['put'])
def update_product(product_id):
    cart = session['cart']
    if cart and product_id in cart:
        quantity = request.json.get("quantity")
        cart[product_id]['quantity'] = int(quantity)

    session['cart'] = cart
    return jsonify({
        "count_cart": utils.count_product(cart),
        "quantity_update": cart[product_id]['quantity']
    })


@app.route('/cart')
def cart_detail():
    return render_template('Cart.html')


@app.context_processor
def common_resp():
    return {
        'categories': dao.load_categories(),
        'cart': utils.count_product(session.get('cart'))
    }


if __name__ == "__main__":
    from app import admin

    app.run(debug=True)
