from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db
from app.models import Product, Category, UserRole
from flask import redirect
from flask_login import logout_user, current_user

admin = Admin(app=app, name="Quan ly ban hang", template_mode="bootstrap4")


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class CategoryView(AuthenticatedAdmin):
    column_display_pk = True
    column_list = ['name', 'products']


class ProductView(AuthenticatedAdmin):
    column_display_pk = True
    column_filters = ['name', 'price']
    column_searchable_list = ['name']
    column_list = ['name', 'description', 'price', 'image', 'category']


class StatsView(AuthenticatedUser):
    @expose('/')
    def index(self):
        return self.render('admin/statistics.html')


class LogoutView(AuthenticatedUser):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name="Thong ke"))
admin.add_view(LogoutView(name="Log out"))
