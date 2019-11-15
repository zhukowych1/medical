from django.shortcuts import render
from django.utils import timezone
from administrator.models import LaboratoryAssistant,LabolatoryVisitings,AnalysisTemplate,Card
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
	l = LaboratoryAssistant.objects.get(login = request.user.username)
	
	v = LabolatoryVisitings.objects.filter(laborant = l,patient__isnull = False)
	viting_now = None
	for i in range(len(v)):
		if v[i].if_in_time():
			viting_now = v[i]

	return render(request,"cabinet/ok.html",{"main_render":'labolatory-assistant/labolatory-assistant_home.html',
											"menu_render":"labolatory-assistant/labolatory-assistant_menu.html",
											"viting_now":viting_now})	

def set_analysis_results(request):
	analysis = LabolatoryVisitings.objects.filter(patient__isnull=False)
	return render(request,"cabinet/ok.html",{"main_render":'labolatory-assistant/labolatory-assistant_set_analysis_results.html',
											"menu_render":"labolatory-assistant/labolatory-assistant_menu.html",
											"analysis":analysis})	

def list_of_analysis(request,visiting_id):
	analysis = LabolatoryVisitings.objects.get(id=visiting_id)	
	if analysis.analys_type == "":
		analysis.delete()
		return HttpResponseRedirect( reverse( "labolatory-assistant:set_analysis_results" ,args =() ) )
	analysis_types = analysis.analys_type.split("|")

	analysis_types2 = []
	for i in range(len(analysis_types)):
		if analysis_types[i] != "":
			analysis_types2.append(analysis_types[i])
	return render(request,"cabinet/ok.html",{"main_render":'labolatory-assistant/labolatory-assistant_list_of_analysis.html',
											"menu_render":"labolatory-assistant/labolatory-assistant_menu.html",
											"analysis":analysis,
											"analysis_types":analysis_types2})		

def set_analys(request,visiting_id,analys):
	analysis = LabolatoryVisitings.objects.get(id=visiting_id)	
	template = AnalysisTemplate.objects.get(name = analys)

	a = template.template.split("|")
	

	return_list = []
	for i in range(len(a)):
		if a[i] != '':
		
			return_list.append(a[i][0:len(a[i])-2])
	if request.method == "POST":
		b = template.template

		for i in return_list:

			
			b = b.replace("#",request.POST[i],1)

		analysis.patient.card_set.create(
								date = timezone.now(),
								content_type = "analysis",
								second_title = template.name,
								content = b,
								conclusion = None
							)

		analysis.analys_type = analysis.analys_type .replace( template.name+"|" , '',1 )


		analysis.save()
		return HttpResponseRedirect( reverse( "labolatory-assistant:list_of_analysis" ,args = (analysis.id,) ) )
	



	return render(request,"cabinet/ok.html",{"main_render":'labolatory-assistant/labolatory-assistant_set_analys.html',
											"menu_render":"labolatory-assistant/labolatory-assistant_menu.html",
											"analysis":analysis,
											"analysis_type":analys,
											"fields":return_list
											})			