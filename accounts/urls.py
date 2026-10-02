from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/",                     views.login_view,                    name="login"),
    path("register/",                  views.register_view,                 name="register"),
    path("initial-learning-language/", views.set_initial_learning_language, name="set_initial_learning_language"),
    path("account/edit/",              views.edit_account_view,             name="edit_account"),
    path("logout/",                    views.logout_view,                   name="logout")
]