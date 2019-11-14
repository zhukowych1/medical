
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
	path('',include('index.urls')),
    path('accounts/',include('login.urls')),
    path('doctor/',include('doctor.urls',namespace="doctor")),
    path('patient/',include('patient.urls',namespace="patient")),
    path('administrator/',include('administrator.urls',namespace="administrator")),   
    path('registry/',include("registry.urls",namespace='registry')),
    path('labolatory-assistant/',include("labolatory-assistant.urls",namespace='labolatory-assistant')),
    path('head-doctor/',include('head-doctor.urls',namespace="head-doctor")),
    path('admin/', admin.site.urls)
]
