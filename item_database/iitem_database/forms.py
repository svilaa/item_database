from django.forms import ModelForm
from django import forms
from iitem_database.models import UserItems

class AddUserItemForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddUserItemForm, self).__init__(*args, **kwargs)
		self.fields['itemID'].label = "Item name"

	class Meta:
		model = UserItems
		fields = ('itemID', 'quantity')