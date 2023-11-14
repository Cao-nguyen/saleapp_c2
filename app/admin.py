from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db
from app.models import Product, Category

admin = Admin(app=app, name="Quan ly ban hang", template_mode="bootstrap4")


class CategoryView(ModelView):
    column_display_pk = True
    column_list = ['name', 'products']


class ProductView(ModelView):
    column_display_pk = True
    column_filters = ['name', 'price']
    column_searchable_list = ['name']
    column_list = ['name', 'description', 'price', 'image', 'category']


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/statistics.html')


admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name="Thong ke"))
