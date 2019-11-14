from django.shortcuts import render,redirect
from administrator.models import Patient,Visitings,Doctor,Profession,FamilyDoctorVotes
from django.utils import timezone
from datetime import timedelta,datetime,date
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
	a = Patient.objects.get(login=request.user.username)
	now  = timezone.now()
	try:
		visiting_ = a.visitings_set.all()
	except Visitings.DoesNonExist:
		visiting_ = None
	visiting = None
	if visiting_ != None:
		for i in visiting_:
			if i.if_in_time():
				visiting = i
				broke
	all_visitings = a.visitings_set.all()

	return render(request,"cabinet/ok.html",{"main_render":'patient/patient_home.html',
											 "menu_render":"patient/patient_menu.html",
											 "my_visitings":visiting,
											 "all_visitings":all_visitings
											 })
def vote_algoritm(name):

	all_sum = Patient.objects.filter(family_doctor = name).count()
	sum = 0
	for i in range(10):
		sum += Patient.objects.filter(family_doctor = name,vote=i).count() * i
	
	all_sum_ = round(sum/all_sum,1)

	return all_sum_
	

	

def vote(request):
	patient = Patient.objects.get(login=request.user.username)
	balls = [1,2,3,4,5,6,7,8,9,10]
	if request.method == "POST":
		vote1 = request.POST['vote1']
		vote2 = request.POST['vote2']
		_vote_ = round((int(vote1) + int(vote2))/2,1)
		d= Doctor.objects.get(login = patient.family_doctor)
		vote = FamilyDoctorVotes.objects.get(doctor=d)
		if vote.vote == None:
		

			patient.can_vote = False
			patient.vote = _vote_
			patient.save()

			_vote_ = vote_algoritm(patient.family_doctor)

			vote.save()

			return HttpResponseRedirect( reverse( "patient:home",args=() ) )
		else:
			vote.vote = round((vote.vote + _vote_)/2,1)
			patient.can_vote = False
			patient.vote = _vote_
			patient.save()
			vote.save()
			return HttpResponseRedirect( reverse( "patient:home",args=() ) )
	return render(request,"cabinet/ok.html",{"main_render":'patient/patients_vote.html',
								  			"menu_render":"patient/patient_menu.html",
											"balls":balls,
											"patient":patient
											})

def my_card(request):

	a = Patient.objects.get(login=request.user.username)
	types = Profession.objects.all()
	

	cards_all = a.card_set.order_by("-date")[:10]

	if request.method == "POST":
		date = request.POST['date'].split(".")
		doctor = request.POST['doctor_rank']

		if date[0] == "":
			if doctor == "Лаборант":
			
				cards_all = a.card_set.filter(content_type = 'analysis')

			else:
			
				cards_all = a.card_set.filter(doctor__rank = doctor)

		else:
			if doctor == "Лаборант":
			
				cards_all = a.card_set.filter(content_type = 'analysis',
											  date__year=date[2],
									  	      date__month=date[1],
									  	      date__day=date[0] ).order_by("-date")
			else:
				
				cards_all = a.card_set.filter(
										doctor__rank = doctor,
										date__year=date[2],
										date__month=date[1],
										date__day=date[0] ).order_by("-date")
	return render(request,"cabinet/ok.html",{"main_render":'patient/patient_my_card.html',
								  					"menu_render":"patient/patient_menu.html",
								  					"carsd_all":cards_all,
								  					"patient":a,
													"types":types})

		



def reserve(request):
	p = Patient.objects.get(login=request.user.username)
	d = Doctor.objects.get(login=p.family_doctor)
	v = None#Visitings.objects.filter(docotor=d)

	curr_day = timezone.now()
	days = []
	for i in range(8):
		
		days.append([curr_day + timedelta(i), (curr_day + timedelta(i)).strftime("%Y.%m.%d") ])




	return render(request,"cabinet/ok.html",{"main_render":'patient/patient_reserve.html',
											 "menu_render":"patient/patient_menu.html",
											 "days":days})
def get_day_visiting(request,date):

	visitings =Visitings.objects.filter(date__contains=datetime.strptime(date, "%Y.%m.%d").date())

	return render(request,"cabinet/ok.html",{"main_render":'patient/patiens_get_day_visitings.html',
											 "menu_render":"patient/patient_menu.html",
											 "visitings":visitings,
											 "date":date})	




def visiting(request,visitings_id):
	p = Patient.objects.get(login=request.user.username)
	d = Doctor.objects.get(login=p.family_doctor)
	v = Visitings.objects.get(id=visitings_id)
	v.patient = p
	p.can_vote = True
	p.save()
	v.save()
	return redirect("patient:reserve")




