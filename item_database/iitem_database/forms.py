from django.forms import ModelForm
from django import forms
from iitem_database.models import UserItems, Item, Area, Creature

class AddUserItemForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddUserItemForm, self).__init__(*args, **kwargs)
		self.fields['itemID'].label = "Item name"
		self.fields['desc'].label = "Description"

	class Meta:
		model = UserItems
		fields = ('itemID', 'quantity')

class AddItemForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddItemForm, self).__init__(*args, **kwargs)
		self.fields['desc'].label = "Description"
		self.fields['typeID'].label = "Type"

	class Meta:
		model = Item
		fields = ('name', 'desc', 'typeID')

class AddAreaForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddAreaForm, self).__init__(*args, **kwargs)
		self.fields['desc'].label = "Description"

	class Meta:
		model = Area
		fields = ('name', 'desc')

class AddCreatureForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddCreatureForm, self).__init__(*args, **kwargs)
		self.fields['desc'].label = "Description"
		self.fields['dangerLevel'].label = "Danger level"

	class Meta:
		model = Creature
		fields = ('name', 'desc', 'dangerLevel', 'souls', 'unique', 'areas')