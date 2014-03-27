from django.forms import ModelForm
from django import forms
from iitem_database.models import UserItems

class AddUserItemForm(ModelForm):
	class Meta:
		model = UserItems
		fields = ('userID', 'itemID', 'quantity')