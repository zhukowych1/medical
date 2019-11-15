from django.urls import path

from . import views


app_name = "login"
urlpatterns = [
    path('',views.login,name = "login"),
    path('logout',views.logout,name="log_out"),
    path('register',views.register,name="register"),
    path('info/',views.info,name="info")
]
