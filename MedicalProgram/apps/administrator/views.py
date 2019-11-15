from datetime import datetime,timedelta
from django.shortcuts import render,redirect
from django.contrib.postgres.fields import JSONField
from .models import (Doctor
					,Visitings,
					Profession,
					Word,
					Registry,
					AnalysisTemplate,
					LaboratoryAssistant,
					LabolatoryVisitings,
					)
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import auth,User
from django.utils import timezone
from django.contrib import messages
import random



ARRAY = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
 '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-']

def create_pass(lenght):
	return_string = ''
	for i in range(lenght):
		return_string += random.choice(ARRAY)
	return return_string


def home(request):

	doctors = None
	types = Profession.objects.all()
	laborants =None
	if request.method == "POST":

		doctor_name = request.POST['doctor_login']
		doctor_rank = request.POST['doctor_rank']
		doctors = Doctor.objects.filter(name__contains=doctor_name,
									   rank=doctor_rank)


		if doctor_name == "":
			doctors = Doctor.objects.filter(rank=doctor_rank)		
		
		if doctor_rank == "Лаборант":

			laborants = LaboratoryAssistant.objects.filter( 
					name__contains=doctor_name
				)
			print(laborants)

	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_home.html',
											 "menu_render":"administrator/administrator_menu.html",
											 "all_doctors":doctors,
											 "laborants":laborants,
											 "types":types})
def edit_doctor(request,doctor_id):
	doctor = Doctor.objects.get(id=doctor_id)
	types = Profession.objects.filter()	
	if request.method == "POST":
		name = request.POST['name']
		date = datetime(int(request.POST['year']),int(request.POST['month']),int(request.POST['day']))
		rank = request.POST['spec']
		doctor.name = name
		doctor.date_birth = date
		doctor.rank = rank
		doctor.save()
		return HttpResponseRedirect( reverse("administrator:home",args=()) )


	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_edit_doctor.html',
											 "menu_render":"administrator/administrator_menu.html",
											 "doctor":doctor,
											 "types":types})	
def edit_password(request,doctor_id):
	d = Doctor.objects.get(id=doctor_id)
	doctor = User.objects.get(username=d.login)
	if request.method == "POST":
		password1 = request.POST['password']
		password2 = request.POST['password2']
		if password1 == password2:

			doctor.set_password(password1)
			doctor.save()
			return HttpResponseRedirect( reverse("administrator:edit_doctor" , args=(d.id,)) )
	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_edit_password.html',
											 "menu_render":"administrator/administrator_menu.html",
											 "doctor":d,})		


def add_doctor(request):
	ranks = Profession.objects.all()

	if request.method == "POST":
		first_name = request.POST['first_name']
		last_name = request.POST['last_name'] + " " + request.POST['end_name']
		
		password1 = request.POST['password']
		password2 = request.POST['password2']
		rank = request.POST['spec']
	
		try:
			date = datetime(int(request.POST['year']),int(request.POST['month']),int(request.POST['day']))		
		except:
			messages.error(request,"Ви не правильно ввели дату")
		if password1 == password2:
			_type = Profession.objects.get(word=rank)
			if _type.casta == 'doctor':
			
				username = _type.casta + "_%03d" % (User.objects.latest('id').id+1)
				user = User.objects.create_user(username=username,password=password2,first_name=first_name,last_name=last_name)		
				user.save()
				d = Doctor(login=username,name=first_name+last_name,rank=rank,key=create_pass(33),date_birth=date)
				d.save()

				if rank == "Сімейний лікар":
					d.familydoctorvotes_set.create(vote=None)
			elif _type.casta == 'registry':
				username = _type.casta + "_%03d" % (User.objects.latest('id').id+1)
				user = User.objects.create_user(username=username,password=password2,first_name=first_name,last_name=last_name)		
				user.save()
				r  =Registry(login=username,name=request.POST['name'],date_birth=date)
				r.save()
			elif _type.casta == 'labolatory-assistant':
				username = _type.casta + "_%03d" % (User.objects.latest('id').id+1)
				user = User.objects.create_user(username=username,password=password2,first_name=first_name,last_name=last_name)		
				user.save()
				l  = LaboratoryAssistant(login=username,name=request.POST['name'],key=create_pass(10))
				l.save()		
			elif _type.casta == 'head-doctor':
				username = _type.casta + "_%03d" % (User.objects.latest('id').id+1)
				user = User.objects.create_user(username=username,password=password2,first_name=first_name,last_name=last_name)		
			return HttpResponseRedirect( reverse("administrator:add_doctor_information" , args=(user.id,)) )			
		else:
			messages.error(request,"Паролі не збігаються")
		
	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_add_doctor.html',
											"menu_render":"administrator/administrator_menu.html",
											"ranks":ranks
					
										})
def add_doctor_information(request,user_id):
	user = User.objects.get(id=user_id)

	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_add_employee_info.html',
											"menu_render":"administrator/administrator_menu.html",
											"user":user})	



def vocabulary_settings(request):

	words = None
	profession = None
	if request.method == "POST":
		word =request.POST['word']
		profession = Profession.objects.filter(word__contains = word)
		words = Word.objects.filter(word__contains = word)


	
	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_vocabulary_settings.html',
											"menu_render":"administrator/administrator_menu.html",
											"words":words,
											"professions":profession})

def add_word(request):

	if request.method == "POST":
		word1 = request.POST['word1']
		word2 = request.POST['word2']
		code = request.POST['word_code']
		if word1==word2:
			w = Word(word=word1,code = code)
			w.save()
			return HttpResponseRedirect ( reverse("administrator:vocabulary",args=()) )
	 
	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_add_word.html',
											 "menu_render":"administrator/administrator_menu.html",
											})		
def add_profession(request):
	if request.method == "POST":
		profession1 = request.POST['profession1']
		profession2 = request.POST['profession2']
		code = request.POST['profession_code']
		casta = request.POST['cast']
		if profession1==profession1:
			p = Profession(word=profession1,code = code,casta=casta)
			p.save()
			return HttpResponseRedirect( reverse("administrator:vocabulary" ,args=() ) )
	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_add_profession.html',
											 "menu_render":"administrator/administrator_menu.html",
											})			





def schedule(request):

	doctors = None
	laborants = None
	if request.method == "POST":
		name = request.POST['d_name']
		doctors = Doctor.objects.filter(name__contains=name)
		laborants = LaboratoryAssistant.objects.filter(name__contains=name)

  		
	

	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_schedule.html',
											"menu_render":"administrator/administrator_menu.html",
											"doctors":doctors,
											"laborants":laborants
											})

def visiting_template_schedule(request,user):
	type_ = user.split("_")
	if type_[0] == 'doctor':
		employee = Doctor.objects.get(login=user)
	else:
		employee = LaboratoryAssistant.objects.get(login=user)



	hours = [8,9,10,11,12,13,14,15,16,17,18,19,20]
	days = [["1 - й","z1","d1"],
			["2 - й","z2","d2"],
			["3 - й","z3","d3"],
			["4 - й","z4","d4"],
			["5 - й","z5","d5"] ]
	if request.method == "POST":
		data = []
		obj = []
		time_start = request.POST['date'].split(".")
		time_for_one = timedelta(minutes = int( request.POST['time_for'] ) )
		for i in range(len(days)):
			
			hour_start = timedelta(hours = int(request.POST[ days[i][1] ]) )
			
			hour_end = timedelta(hours = int(request.POST[ days[i][2] ]) )

			if hour_end - hour_start != timedelta(hours=0,minutes=0,seconds=0):
				index = (hour_end-hour_start)//timedelta(minutes=15)

				hour_start_add = datetime(int(time_start[2]), int(time_start[1]), int(time_start[0]) )+ timedelta(i)
		
				for e in range(index):
					if type_[0] == 'doctor':
						obj.append(Visitings(
									docotor=employee,
									patient = None,
									date = hour_start_add + hour_start +time_for_one*e
								)								
						)	
					else:
				
						obj.append(LabolatoryVisitings(
									laborant=employee,
									date = hour_start_add + hour_start +time_for_one*e
								)								
						)	
				if type_[0] == 'doctor':			
					Visitings.objects.bulk_create(obj)
				else:
					LabolatoryVisitings.objects.bulk_create(obj)
		return redirect ( "administrator:schedule" )
	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_set_schedule.html',
											"menu_render":"administrator/administrator_menu.html",
											"employee":employee,
											"hours":hours,
											"days":days
											})	


################################# ВІДДІЛ АНАЛІЗІВ #######################################################



def analysis_templates(request):
	analysis = AnalysisTemplate.objects.all()
	if request.method == "POST":
		name = request.POST['name']
		rows = request.POST['rows']
		return HttpResponseRedirect( reverse("administrator:create_analysis_templates" , args=(name,rows)) )

	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_analysis_templates.html',
											"menu_render":"administrator/administrator_menu.html",
											"analysis":analysis
											})		


def create_analysis_templates(request,name,count_of_rows):
	rows = []
	for i in range(count_of_rows):
		rows.append(str(i+1))

	if request.method == "POST":
		name = request.POST['name']
		code = request.POST['code']
		rows_results = ''
		for i in range(len(rows)):
			rows_results += '|'+ request.POST[str(i+1)] + "/#|"

		print(rows_results)
		AnalysisTemplate.objects.create(
							name = name,
							code = code,
							template = rows_results
						)
		
		return HttpResponseRedirect (reverse("administrator:analysis_templates",args = ()))



	return render(request,"cabinet/ok.html",{"main_render":'administrator/administrator_create_analysis_templates.html',
											"menu_render":"administrator/administrator_menu.html",
											"analysis_name":name,
											"count_of_rows":count_of_rows,	
											"rows":rows,

											})		

def delete_analysis_template(request,analysis_id):
	analysis = AnalysisTemplate.objects.get(id = analysis_id)
	analysis.delete()
	return HttpResponseRedirect( reverse("administrator:analysis_templates" ,args=() ) )