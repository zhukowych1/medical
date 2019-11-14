from django.urls import path

from . import views


app_name = "registry"
urlpatterns = [
	path('home/',views.home,name="home"),
	path('search_patients/',views.search_patient,name="search_patient"),
	path('confim_patient_data/<int:patient_id>',views.confim_patient_data,name="confim_patient_data")
]