from django.urls import path

from . import views

app_name = "patient"
urlpatterns = [
	path("home/",views.home,name="home"),
	path('my_card/',views.my_card,name="my_card"),
	path('reserve/',views.reserve,name="reserve"),
	path('get_day_visitings/<str:date>/',views.get_day_visiting,name="get_day_visitings"),
	path('set_visiting/<int:visitings_id>/',views.visiting,name="create_visiting"),
	path('vote/',views.vote,name="vote"),


]