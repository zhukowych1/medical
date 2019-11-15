import datetime
from django.db import models
from fernet_fields import EncryptedCharField,EncryptedTextField
from django.core.exceptions import ValidationError

from django.utils import timezone



class Doctor(models.Model):
	login = models.CharField(max_length=20)
	name = models.CharField(max_length=50)
	rank = models.CharField(max_length=50)

	key = EncryptedCharField(max_length=3, null= True)
	date_birth = models.DateTimeField(null=True)
	class Meta:
		verbose_name = 'Лікар'
		verbose_name_plural = 'Лікарі'

class FamilyDoctorVotes(models.Model):
	vote = models.FloatField(null=True)
	doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)

class Patient(models.Model):
	login = models.CharField(max_length=20)
	name = models.CharField(max_length=50)
	family_doctor = models.CharField(null=True,max_length=20)
	phone_number = models.CharField(max_length=20,null=True)
	email = models.CharField(max_length=40)
	address = models.TextField(null=True)
	date_birth = models.DateTimeField(null=True)
	vote = models.IntegerField(null=True)
	can_vote = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Пацієнт'
		verbose_name_plural = 'Пацієнти'	

class Registry(models.Model):
	login = models.CharField(max_length=20)
	name = models.CharField(max_length=50)
	date_birth = models.DateTimeField(null=True)
	address = models.TextField(null=True)
	class Meta:
		verbose_name = 'Реєстратор'
		verbose_name_plural = 'Реєстратори'	

class AnalysisTemplate(models.Model):
	name = models.CharField(max_length=30)
	code = models.CharField(max_length=10)
	template = models.TextField()


class LaboratoryAssistant(models.Model):
	login = models.CharField(max_length=20)
	name = models.CharField(max_length=50)
	key = models.CharField(max_length=10)
		



class Visitings(models.Model):
	docotor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
	date = models.DateTimeField()
	is_in = models.BooleanField(default=False)
	if_go = models.BooleanField(default=True)

	def update_is_in(self):
		self.is_in = True
	def update_if_go(self):
		self.if_go =False
	def if_in_time(self):
		if timezone.now() >= self.date and timezone.now() < self.date + datetime.timedelta(minutes=15):
			return True
		
		else:
			return False
	class Meta:
		verbose_name = 'Прийом'
		verbose_name_plural = 'Прийоми'


class LabolatoryVisitings(models.Model):
	laborant = models.ForeignKey(LaboratoryAssistant,on_delete=models.CASCADE,null=True)
	patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null = True,default=None)
	date = models.DateTimeField(null=True,default=None)
	analys_type = models.TextField(null=True,default=None)
	is_prow = models.BooleanField(null=True,default=None)	
	def if_in_time(self):
		if timezone.now() >= self.date and timezone.now() < self.date + datetime.timedelta(minutes=15):
			return True
		
		else:
			return False		

class Card(models.Model):
	date = models.DateTimeField()
	patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
	content_type = models.CharField(max_length=30,null=True)
	second_title  = models.CharField(max_length=30,null=True)
	content = EncryptedTextField('Текст запису')
	conclusion = EncryptedTextField('Заключення',max_length=100,null=True)
	doctor = models.ForeignKey(Doctor or LaboratoryAssistant,on_delete=models.CASCADE,null=True)
	previous_hash = models.CharField(max_length = 50,null=True)
	class Meta:
		verbose_name = 'Картка'
		verbose_name_plural = 'Картка'
	def analysis_split(self):
		return_list = []
		b = self.content.split("|")
		for i in range(len(b)):
		    if b[i] != '':
		        return_list.append(b[i].split("/"))		
		return return_list
	def create(self):
		raise ValidationError("Не Правильно")

class Word(models.Model):
	word = models.CharField(max_length=100)
	code = models.CharField(max_length=16,null=True)
	class Meta:
		verbose_name = 'Слово'
		verbose_name_plural = 'Слова'

class Profession(models.Model):
	word = models.CharField(max_length=100)
	code = models.CharField(max_length = 16)
	casta = models.CharField(max_length=30)










	


	
