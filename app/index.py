from flask import render_template, request, redirect
from app import app, login
import dao
from flask_login import login_user
from app.models import User

@app.route("/")
def index():
    kw = request.args.get('kw')
    return render_template("homesite.html", categories=dao.load_categories(), products=dao.load_products(kw))


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(username == username, password == password).first()
        if user:
            login_user(user=user)
    return redirect("/admin")


@login.user_loader
def get_user(user_id):
    return dao.load_user(user_id)


if __name__ == "__main__":
    from app import admin

    app.run(debug=True)
