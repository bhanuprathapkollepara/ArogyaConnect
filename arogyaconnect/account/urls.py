

from sys import path

from django.contrib.admin import views


urlspattern = [
    path("singup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
]