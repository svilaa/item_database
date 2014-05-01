from django.forms import ModelForm
from django import forms
from iitem_database.models import UserItems, Item, Area, Creature

class AddUserItemForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddUserItemForm, self).__init__(*args, **kwargs)
		self.fields['itemID'].label = "Item name"

	class Meta:
		model = UserItems
		fields = ('itemID', 'quantity')

class AddItemForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddItemForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Item

class AddAreaForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddAreaForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Area

class AddCreatureForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddCreatureForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Creature