from django.urls import path

from . import views


app_name = "head-doctor"
urlpatterns = [
    path('home/',views.home,name='home')

]