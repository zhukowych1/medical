from django.urls import path

from . import views


app_name = "administrator"
urlpatterns = [
    path('home/',views.home,name = "home"),
    path('add_docotor/',views.add_doctor,name="add_docotor"),
    path('add_doctor_information/<int:user_id>',views.add_doctor_information,name="add_doctor_information"),
    path('edit_doctor/<int:doctor_id>',views.edit_doctor,name="edit_doctor"),
    path('edit_password/<int:doctor_id>',views.edit_password,name="edit_password"),
    path('vocabulary/',views.vocabulary_settings,name="vocabulary"),
    path('add_word/',views.add_word,name="add_word"),
    path('add_profession/',views.add_profession,name="add_profession"),
    path('schedule/',views.schedule,name="schedule"),
    path('set_schedule/<str:user>',views.visiting_template_schedule,name="set_schedule"),
    path('analysis_templates',views.analysis_templates,name="analysis_templates"),
    path('create_analysis_templates/<str:name>/<int:count_of_rows>/',views.create_analysis_templates,name="create_analysis_templates"),
    path('delete_analysis_template/<int:analysis_id>',views.delete_analysis_template,name="delete_analysis_template")
]