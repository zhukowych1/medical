from django.shortcuts import render
from administrator.models import Card

def home(request):
    #cards = Card.objects.all().count()
    cards = Card.objects.all().count()
    #print(1)
    return render(request,"cabinet/ok.html",{"main_render":'head-doctor/head-doctor_home.html',
                                            "menu_render":"head-doctor/head-doctor_menu.html",
                                            "count_of_cards":cards})	