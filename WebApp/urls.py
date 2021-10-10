from django.contrib import admin
from django.urls import path
from WebApp import views
from WebApp.views import add_todo
urlpatterns = [
    path("",views.index,name="home"),
    path("about",views.about,name="about"),
    path("contact",views.contact,name="contact"),
    path("signin",views.signin,name="signin"),
    path("signup",views.signup,name="signup"),
    path("signout",views.signout,name="signout"),
    path("loggedin",views.loggedin,name="signout"),
    path("add-todo",views.add_todo,name="add-todo"),
    path("delete-todo/<int:id>",views.delete_todo,name="delete-todo"),
    path("change-status/<int:id>/<str:status>",views.change_status,name="change-status")
]