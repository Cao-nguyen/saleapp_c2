from app.models import Product, Category, User


def load_categories():
    return Category.query.all()


def load_products(kw):
    products = Product.query
    if kw:
        products = products.filter(Product.name.contains(kw))
    return products.all()


def load_user(user_id):
    return User.query.get(user_id)
