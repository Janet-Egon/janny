from django.urls import path
from . import views    # dot is for the current directory


urlpatterns = [
    path("signup", views.Signup.as_view()),
    path("login", views.Login.as_view()),
    path("create", views.CreatePost.as_view()),
    path("view", views.View.as_view()),
    path("update",views.Update.as_view()),
    path("delete",views.Delete.as_view()),
 ]


