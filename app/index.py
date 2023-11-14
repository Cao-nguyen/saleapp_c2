from flask import Flask, render_template, request
from app import app
import dao


@app.route("/")
def index():
    kw = request.args.get('kw')
    return render_template("homesite.html", categories=dao.load_categories(), products=dao.load_products(kw))


if __name__ == "__main__":
    from app import admin
    app.run(debug=True)
