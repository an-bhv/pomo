from django.urls import path
from . import views

app_name = "main"   


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register", views.register_request, name="register"),
    path("logout", views.logout_request, name= "logout"),
    path("login", views.login_request, name="login"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("like/",views.like_post,name='like_post'),
    path("search/",views.search_res,name='search_res'),

]