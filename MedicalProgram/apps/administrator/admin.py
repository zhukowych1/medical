from django.contrib import admin

from .models import Doctor,Patient,Visitings,Card

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Visitings)

admin.site.register(Card)

