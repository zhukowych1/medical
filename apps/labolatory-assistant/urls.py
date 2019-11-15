from django.urls import path

from . import views
app_name = "labolatory-assistant"
urlpatterns = [
	path('home/',views.home,name="home"),
	path('set_analysis_results/',views.set_analysis_results,name="set_analysis_results"),
	path('list_of_analysis/<int:visiting_id>',views.list_of_analysis,name="list_of_analysis"),
	path('set_analys/<int:visiting_id>/<str:analys>',views.set_analys,name="set_analys"),	

]