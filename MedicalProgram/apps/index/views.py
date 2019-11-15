from django.shortcuts import render
from administrator.models import FamilyDoctorVotes

# Create your views here.

def home(request):
    return render(request,"index/home.html",{})

def rating(request):
    votes = FamilyDoctorVotes.objects.order_by('-vote')
    return render(request,"index/rating.html",{"all_doctors":votes})