from django import forms

from administrator.models import Card

class AddCardRecordForm(forms.Form):
	

	class Meta:
		model = Card
		fields = [
			'content',
			'conclusion'
		]




