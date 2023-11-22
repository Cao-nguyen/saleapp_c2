import hashlib
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
    page = request.args.get('page')  # lay so trang

    cates = dao.load_categories()
    products = dao.load_products(kw, cate_id, page)

    pages = app.config["PAGE_SIZE"]
    total_products = dao.get_count_products()

    page_number = int(math.ceil(total_products/pages))
    return render_template("homesite.html", categories=cates, products=products, page_number=page_number)


@app.route("/admin/login", methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    print(str(hashlib.md5(str(password).strip().encode('utf-8')).hexdigest()))
    user = auth_user(username=username, password=password)

    if user:
        login_user(user=user)

    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


def auth_user(username, password):
    username = str(username).strip()
    password = str(hashlib.md5(str(password).strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()


if __name__ == "__main__":
    from app import admin

    app.run(debug=True)
