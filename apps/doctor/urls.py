from django.urls import path

from . import views


app_name = "doctor"
urlpatterns = [
    path('home/',views.home,name = "home"),
    path('my_cards/',views.my_cards,name="my_cards"),
    path('card/<int:patient_id>/',views.card,name="card"),
    path('add_card_record/<int:patient_id>',views.add_card_record,name="add_card_record"),
    path('add_card_direction/<int:patient_id>',views.add_card_direction,name="add_card_direction"),
    path('add_patient/',views.add_patient,name="add_patient"),
    path('set_patient_dierection/<int:patient_id>/<int:visiting_id>',views.set_patient_dierection,name="set_patient_dierection"),
    path('add_analysis_direction/<int:patient_id>/',views.add_analysis_direction,name="add_analysis_direction"),
    path('set_analysis_direction/<int:patient_id>/<int:visiting_id>/',views.set_analysis_direction,name="set_analysis_direction")

]