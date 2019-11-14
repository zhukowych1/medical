from django.shortcuts import render,redirect
from .forms import AddCardRecordForm
from administrator.models import Doctor,Patient,Visitings,Word,LabolatoryVisitings,AnalysisTemplate,Profession,Card
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from itertools import chain
from django.core.signing import Signer
import operator
from datetime import timedelta,datetime,date
from django.utils import formats
import hashlib

def home(request):

	d = Doctor.objects.get(login=request.user.username)
	print(d.login)
	all_visitings = Visitings.objects.filter(docotor=d,patient__isnull=False)
	
	visiting_now = None
	now = timezone.now()
	for i in all_visitings:
			if i.if_in_time():
				
				visiting_now = i


	
	return render(request,"cabinet/ok.html",{"main_render":'doctor/doctor_home.html',
											 "menu_render":"doctor/doctor_menu.html",
											 "all_visitings":all_visitings,
											 "visiting_now":visiting_now,
											 "date_now":now})

def my_cards(request):
	doctor = Doctor.objects.get(login = request.user.username)
	patients1 = Patient.objects.filter(family_doctor=request.user.username)

	patients2 =Patient.objects.filter(directions__in=Directions.objects.filter(docotor= doctor))

	patients = patients1 | patients2
	print(patients)
	name = None
	if request.method == "POST":
		name = request.POST['patient_login']
		patients = patients.filter( name__contains=name)
	return render(request,"cabinet/ok.html",{"main_render":'doctor/doctor_cards.html',
											"menu_render":"doctor/doctor_menu.html",
											"patients":patients,
											"name":name
											})

def card(request,patient_id):


	d = Doctor.objects.get(login=request.user.username)
	a = Patient.objects.get(id=patient_id)
	types = Profession.objects.all()
	

	cards_all = a.card_set.order_by("-date")[:10]

	if request.method == "POST":
		date = request.POST['date'].split(".")
		doctor = request.POST['doctor_rank']

		if date[0] == "":
			if doctor == "Лаборант":
			
				cards_all = a.card_set.filter(content_type = 'analysis')

			else:
				print(2)
				cards_all = a.card_set.filter(doctor__rank = doctor)

		else:
			if doctor == "Лаборант":
				print(3)
				cards_all = a.card_set.filter(content_type = 'analysis',
											  date__year=date[2],
									  	      date__month=date[1],
									  	      date__day=date[0] ).order_by("-date")
			else:
				print(4)
				cards_all = a.card_set.filter(
										doctor__rank = doctor,
										date__year=date[2],
										date__month=date[1],
										date__day=date[0] ).order_by("-date")
	return render(request,"cabinet/ok.html",{"main_render":'doctor/doctor_card.html',
								  					"menu_render":"doctor/doctor_menu.html",
								  					"carsd_all":cards_all,
								  					"patient":a,
													"types":types})
def prew_hash(latest_card_record,d):
	to_hash = (str(latest_card_record.date)+
					   str(latest_card_record.patient)+ 
					   str(latest_card_record.doctor)+
					   str(latest_card_record.content_type) +
					   str(latest_card_record.second_title)+
					   str(latest_card_record.content)+
					   str(latest_card_record.conclusion)+
					   str(latest_card_record.doctor)+
					   str(latest_card_record.previous_hash)+
					   d.key

					)
	return hashlib.sha256(to_hash.encode()).hexdigest()	
	
def add_card_record(request,patient_id):
	a = Patient.objects.get(id=patient_id)
	d= Doctor.objects.get(login=request.user.username)




	try:
		latest_card_record = a.card_set.latest('id')
	except:
		latest_card_record = None

	words = Word.objects.all()
	date_n = timezone.now()



	if request.method == "POST":
		content = request.POST['content']
		conclusion = request.POST['conclusion']
		if latest_card_record == None:
			previous_hash = hashlib.sha256((d.key).encode()).hexdigest()
		else:

			previous_hash = prew_hash(latest_card_record,d)
			
	
		a.card_set.create(date=date_n,
					      content=content,
					      conclusion=conclusion,
					      second_title = "Діагноз",
						  content_type = "Запис",
						  previous_hash = previous_hash,
					      doctor = d)
		return HttpResponseRedirect(reverse("doctor:card",args=(patient_id,)))
		
	return render(request,"cabinet/ok.html",{"main_render":'doctor/doctor_add_card_record.html',
							  					"menu_render":"doctor/doctor_menu.html",
							  					"date_now":date_n,
							  					"patient":a,
												"words":words})		


def add_card_direction(request,patient_id):
	a = Patient.objects.get(id=patient_id)
	types = Profession.objects.filter()
	dates = []
	now = timezone.now()
	hours = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]


	for i in range(8):

		dates.append(timezone.now() + timedelta(1*i))

	visitings = None
	if request.method == "POST":

		doctor_type = request.POST['doctor_rank']
		dat = request.POST['date1'].split(".")

	

		visitings = Visitings.objects.filter(docotor__rank=doctor_type,
												date__year=dat[2],
												date__month=dat[1],
												date__day=dat[0],
												date__hour=request.POST['date2'],
												patient__isnull=True)

	return render(request,"cabinet/ok.html",{"main_render":'doctor/doctor_add_card_direction.html',
						  					"menu_render":"doctor/doctor_menu.html",
						  					"dates":dates,
						  					"types":types,
						  					"hours":hours,
						  					"visitings":visitings,
						  					"now":now,
						  					"patient":a})			

def search_doctor_acces(request,patient_id):
	patient = Patient.objects.get(id=patient_id)
	types = Profession.objects.filter()
	doctors = None
	if request.method == "POST":


		doctor_type = request.POST['doctor_type']

		doctors = Doctor.objects.filter(rank=doctor_type)

	return render(request,"cabinet/ok.html",{"main_render":'doctor/doctor_search_doctor_acces.html',
						  					"menu_render":"doctor/doctor_menu.html",
						  					"types":types,
						  					"patient":patient,
						  					"doctors":doctors})		




def set_patient_dierection(request,patient_id,visiting_id):
	p = Patient.objects.get(id=patient_id)
	d = Doctor.objects.get(login = request.user.username)
	try:
		latest_card_record = a.card_set.latest('id')
	except:
		latest_card_record = None
	v = Visitings.objects.get(id=visiting_id)
	if request.method == "POST":
		if latest_card_record == None:
			previous_hash = hashlib.sha256((d.key).encode()).hexdigest()
		else:
			previous_hash = prew_hash(latest_card_record,d)
		v.patient = p
		v.save()

		dierect = p.card_set.create(date=timezone.now(),
									previous_hash = previous_hash,
									content="Направлення до {} о {}".format(v.docotor.name,formats.date_format(v.date, "SHORT_DATETIME_FORMAT") ),
									second_title=None)


		return HttpResponseRedirect( reverse("doctor:card" ,args=(p.id,) ) )
	return render(request,"cabinet/ok.html",{"main_render":'doctor/doctor_aspect_dierection.html',
						  					"menu_render":"doctor/doctor_menu.html",
						  					"patient":p,
						  					"visiting":v
						  					})			
def add_patient(request):
	patients=None
	doctor_types = Word.objects.filter(type1="Тип лікаря")
	if request.method == "POST":
		name = request.POST['patient_name']

		patients = Patient.objects.filter(name__contains=name,family_doctor__isnull=True)

	
	return render(request,"cabinet/ok.html",{"main_render":'doctor/doctor_add_patient.html',
						  					"menu_render":"doctor/doctor_menu.html",
						  					"patients":patients,
						  					"types":doctor_types})		

def add_analysis_direction(request,patient_id):
	patient = Patient.objects.get(id = patient_id)
	dates = []
	now = timezone.now()
	hours = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
	for i in range(8):
		dates.append(timezone.now() + timedelta(1*i))
	visitings = None

	if request.method == "POST":
		dat = request.POST['date1'].split(".")

		visitings = LabolatoryVisitings.objects.filter(
												date__year=dat[2],
												date__month=dat[1],
												date__day=dat[0],
												date__hour=request.POST['date2'],
												patient__isnull=True)

	return render(request,"cabinet/ok.html",{"main_render":'doctor/doctor_add_analysis_direction.html',
						  					"menu_render":"doctor/doctor_menu.html",
						  					"patient":patient,
						  					"hours":hours,
						  					"dates":dates,
						  					"visitings":visitings,
						  					"now":now
											})		

def set_analysis_direction(request,patient_id,visiting_id):
	patient = Patient.objects.get(id = patient_id)
	visiting = LabolatoryVisitings.objects.get(id = visiting_id)
	temolates = AnalysisTemplate.objects.all()
	d = Doctor.objects.get(login = request.user.username)
	try:
		latest_card_record = a.card_set.latest('id')
	except:
		latest_card_record = None
	if request.method == "POST":
		list_of_analysis = request.POST["list"]
		visiting.patient = patient
		visiting.analys_type = list_of_analysis
		visiting.save()
		if latest_card_record == None:
			previous_hash = hashlib.sha256((d.key).encode()).hexdigest()
		else:
			previous_hash = prew_hash(latest_card_record,d)
		patient.card_set.create(date= timezone.now(),
						 content_type = "Направлення на аналізи",
						 second_title = None,
						 previous_hash = previous_hash,
						 content = "Направлення на аналізи"
						)
		return HttpResponseRedirect ( reverse("doctor:card",args=(patient.id,)) )


	return render(request,"cabinet/ok.html",{"main_render":'doctor/doctor_set_analysis_direction.html',
						  					"menu_render":"doctor/doctor_menu.html",
						  					"patient":patient,
						  					"visiting":visiting,
						  					"temolates":temolates

											})			
