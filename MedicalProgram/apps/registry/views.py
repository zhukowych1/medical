from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from administrator.models import Patient,Registry,Doctor
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages

def home(request):
	r = Registry.objects.get(login = request.user.username)
	p = Patient.objects.all().count()
	p_r = Patient.objects.filter(family_doctor__isnull=False).count()
	p_n_r = p-p_r

	p_rv = round(p_r/(p/100),2)
	p_n_rv = round(100-p_rv,2)
	print(p_rv)

	return render(request,"cabinet/ok.html",{"main_render":'registry/registry_home.html',
											 "menu_render":"registry/registry_menu.html",
											 "patients":p,
											 "patients_confirmated":p_r,
											 "patients_not_confirmated":p_n_r,
											 "patients_confirmated_interest":str(p_rv),
											 "patients_not_confirmated_interest":str(p_n_rv)									 


											 })	

def search_patient(request):
	patients = Patient.objects.filter(family_doctor__isnull=True)
	if request.method == "POST":
		name = request.POST['patient_name']

		patients = Patient.objects.filter(name__contains= name,family_doctor__isnull=True)
	return render(request,"cabinet/ok.html",{"main_render":'registry/registry_search_patient.html',
											 "menu_render":"registry/registry_menu.html",
											 "patients":patients			 
											 })	


def confim_patient_data(request,patient_id):
	patient = Patient.objects.get(id=patient_id)

	user = User.objects.get(username = patient.login)
	doctors = Doctor.objects.filter(rank="Сімейний лікар")
	if request.method == "POST":
		name = request.POST['name']
		try:
			date = datetime(int(request.POST['year']),int(request.POST['month']),int(request.POST['day']))
		except:
			messages.error(request,"Неправило введена дата")
			return render(request,"cabinet/ok.html",{"main_render":'registry/registry_confim_patient_data.html',
														"menu_render":"registry/registry_menu.html",
														"patient":patient,
														"doctors":doctors 
														})				
		phone_number = request.POST['phone_number']
		addres = request.POST['addres']
		family_doctor = request.POST['family_doctor']
		patient.name= name
		patient.date_birth = date
		patient.phone_number = phone_number
		patient.address = addres
		patient.family_doctor = family_doctor
		patient.save()


		return HttpResponseRedirect( reverse("registry:home" ,args=()) )


	return render(request,"cabinet/ok.html",{"main_render":'registry/registry_confim_patient_data.html',
											 "menu_render":"registry/registry_menu.html",
											 "patient":patient,
											 "doctors":doctors 
											 })	
	