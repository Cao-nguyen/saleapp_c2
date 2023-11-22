from app.models import Product, Category, User
from app import app
import hashlib


def load_categories():
    return Category.query.all()


def load_products(kw=None, cate_id=None, page=None):
    products = Product.query
    if kw:
        products = products.filter(Product.name.contains(kw))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE"]
        start = (page - 1) * page_size
        return products.slice(start, start + page_size)

    return products.slice(0, 6)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_count_products():
    return Product.query.count()
