from django.urls import path
from . import views
from .views import register

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register, name="register"),
    path("product/<int:pk>/", views.product, name="product"),
    path("category/<str:rjb>", views.category, name="category"),
    path("AdminPanel/", views.AdminPanel, name="AdminPanel"),
]
