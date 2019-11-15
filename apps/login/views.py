from django.shortcuts import render
from django.contrib.auth.models import auth,User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


from administrator.models import Patient,Doctor

def login(request):
	print(1)
	if request.method == 'POST':
	

		username = request.POST['login']
		passw = request.POST['password']
		print(username,passw)
		user = auth.authenticate(request,username=username,password=passw)
		print(user)
		if user is not None:
			
			if user.username.split("_")[0] == "patient":
				p = Patient.objects.get(login = user.username)
				if p.family_doctor == None:
					return render(request,"login/info.html",{})	
				else:
					auth.login(request,user)
					r = user.username.split("_")[0]
					redirect_url = request.GET.get('next',str(r)+':home')
					return HttpResponseRedirect( reverse(redirect_url , args=()) )
			else:
				auth.login(request,user)
				r = user.username.split("_")[0]
				redirect_url = request.GET.get('next',str(r)+':home')
				return HttpResponseRedirect( reverse(redirect_url , args=()) )
		else:
			messages.error(request,"Неправильний пароль або логін")


	return render(request,"login/login.html")

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect( reverse("login:login",args=()) )

def register(request):
	username = "patient" + "_%03d" % (User.objects.latest('id').id+1)
	if request.method == "POST":
		first_name = request.POST['name'].split(" ")[0]
		last_name = request.POST['name'].split(" ")[1] + " " + request.POST['name'].split(" ")[2]
		password1 = request.POST['password']
		password2 = request.POST['password2']
		
		

		
		if password1 == password2:
			user = User.objects.create_user(username=username,password=password1,first_name=first_name,last_name=last_name)		
			user.save()


			p = Patient(login=username,name=request.POST['name'],family_doctor=None,email="lalal@gmail.com")
			p.save()

			return HttpResponseRedirect( reverse("login:info" , args=()) )
		else:
			messages.error(request,"Паролі не збігаються")
	return render(request,"login/register.html",{'username':username})

def info(request):
	return render(request,"login/info.html",{})	