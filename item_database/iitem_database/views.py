# Create your views here.
import json as jsn
from datetime import date
from xml.etree.ElementTree import Element, SubElement, tostring

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from iitem_database.models import ItemClass, Area, Creature, Item, Found, UserItems, Drops, Encountered, ItemReview
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, render_to_response, get_object_or_404

from iitem_database.forms import AddUserItemForm, AddItemForm, AddAreaForm, \
								 AddCreatureForm, AddDropForItemForm, AddDropForCreatureForm, \
								 AddFoundForItemForm, AddFoundForAreaForm, AddEncounteredForCreatureForm, \
								 AddEncounteredForAreaForm, ReviewItemForm
from django.contrib.auth import logout

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, permissions
from iitem_database.permissions import IsOwnerOrReadOnly
from iitem_database.serializers import ItemClassSerializer, AreaSerializer, CreatureSerializer, \
										ItemSerializer, FoundSerializer, UserItemsSerializer, DropsSerializer, \
										UserSerializer, EncounteredSerializer, ItemReviewSerializer

from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

html = 'html'
json = 'json'
xml = 'xml'

format_error = "Format not found."

json_indent_level = 4

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class CheckIsOwnerMixin(object):
    def get_object(self, *args, **kwargs):
        obj = super(CheckIsOwnerMixin, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj


def register(request):
	"""
	  Permits new users to enter in the application through a formulary
	"""
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/")
	else:
		form = UserCreationForm()
	return render_to_response("registration/register.html",
		{'form': form},
		context_instance=RequestContext(request))

def mainpage(request):
	"""
	  The / page. Can reaches all the models of the application except
	  the user page
	"""
	template = get_template('mainpage.html')
	variables = Context({
		'titlehead': 'Item database',
		'pagetitle': 'Welcome',
		'user': request.user,
		})
	output = template.render(variables)
	return HttpResponse(output)

def check_object_user_owner(request, obj):
	"""
	  Proves that the current user is the creator of obj
	"""
	if not obj.user == request.user:
		raise PermissionDenied

def get_user(request, username):
	"""
	  Return the current user if really is it, else, throws an exception
	  and the page won't be served
	"""
	try:
		user = User.objects.get(username=username)
		if not user == request.user:
			raise PermissionDenied
	except:
		raise Http404('User not found.')
	return user

@login_required()
def review(request, pk):
    item = Item.objects.get(id=pk)
    new_review = ItemReview(
        rating=request.POST['rating'],
        comment=request.POST['comment'],
        user=request.user,
        item=item)
    new_review.save()
    return HttpResponseRedirect(item.get_absolute_url())

@login_required(login_url='/login/')
def userpage(request, username, format=html):
	"""
	  Shows the items that this user has
	"""
	
	user = get_user(request, username)

	userItems = UserItems.objects.filter(userID=user.id)

	if format == html:
		template = get_template('userpage.html')
		variables = Context({
			'user': user,
			'userItems': userItems,
			})
		output = template.render(variables)
		return HttpResponse(output)
	elif format == json:
		json_response = {}
		json_response['User ID'] = user.id
		json_response['User Name'] = user.username
		json_response['User Items'] = \
			[ {'Item ID' : userItem.itemID.id, 
			   'Item Name' : userItem.itemID.name, 
			   'Quantity' : userItem.quantity } for userItem in userItems ]
		return HttpResponse(jsn.dumps(json_response, indent=json_indent_level, separators=(',', ' : ')), 
			content_type="application/json")
	elif format == xml:
		data = Element('User')
		SubElement(data, 'User_ID').text = str(user.id)
		SubElement(data, 'User_Name').text = user.username
		user_items = SubElement(data, 'User_Items')
		for userItem in userItems:
			item_object = SubElement(user_items, 'Item')
			SubElement(item_object, 'Item_ID').text = str(userItem.itemID.id)
			SubElement(item_object, 'Item_Name').text = userItem.itemID.name
			SubElement(item_object, 'Quantity').text = str(userItem.quantity)		

		return HttpResponse(tostring(data), content_type="application/xml")
	else:
		return HttpResponseNotFound(format_error)


@login_required(login_url='/login/')
def addUserItem(request, username):
	"""
	  Request the user to select a item and a quantity.
	  This data will be show in his item list.
	"""

	user = get_user(request, username)

	if request.method == 'POST':
		itemForm = AddUserItemForm(request.POST)
		
		if itemForm.is_valid():
			item = itemForm.save(commit=False)
			item.userID = user
			if not UserItems.objects.filter(userID=request.user).filter(itemID=item.itemID).exists():
				item.save()
			return HttpResponseRedirect('/user/'+user.username+".html")
	else:
		itemForm = AddUserItemForm()
	return render(request, 'formPage.html', 
		{'form': itemForm, 'content' : 'Add user item',
		 'value': 'Add'},
		context_instance=RequestContext(request))


@login_required(login_url='/login/')
def deleteUserItem(request, username, item):
	"""
	  Deletes the selected item of a user
	"""
	user = get_user(request, username)
	item = UserItems.objects.get(userID=user.id, itemID=item).delete()
	return HttpResponseRedirect('/user/'+username+'.html')

@login_required(login_url='/login/')
def quantityUserItem(request, username, item, quantity):
	"""
	  Modifies the number of a concrete item by the increment/decrement quantity
	"""
	user = get_user(request, username)
	item = UserItems.objects.get(userID=user.id, itemID=item)
	item.quantity+=int(quantity)
	if item.quantity >= 0:
		item.save()
	return HttpResponseRedirect('/user/'+username+'.html')

class ItemCreate(LoginRequiredMixin, CreateView):
	model = Item
	template_name = 'formPage.html'
	form_class = AddItemForm

	def get_context_data(self, **kwargs):
		context = super(ItemCreate, self).get_context_data(**kwargs)
		context['content'] = 'Add item'
		context['value'] = 'Add' 
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(ItemCreate, self).form_valid(form)

class AreaCreate(LoginRequiredMixin, CreateView):
	model = Area
	template_name = 'areaForm.html'
	form_class = AddAreaForm

	def get_context_data(self, **kwargs):
		context = super(AreaCreate, self).get_context_data(**kwargs)
		context['content'] = 'Add area'
		context['value'] = 'Add' 
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(AreaCreate, self).form_valid(form)

class CreatureCreate(LoginRequiredMixin, CreateView):
	model = Creature
	template_name = 'creatureForm.html'
	form_class = AddCreatureForm

	def get_context_data(self, **kwargs):
		context = super(CreatureCreate, self).get_context_data(**kwargs)
		context['content'] = 'Add creature'
		context['value'] = 'Add' 
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(CreatureCreate, self).form_valid(form)

@login_required(login_url='/login/')
def deleteItem(request, itemID):
	item = Item.objects.get(id=itemID)
	check_object_user_owner(request, item)
	item.delete()
	return HttpResponseRedirect('/items.html')

@login_required(login_url='/login/')
def deleteArea(request, areaID):
	area = Area.objects.get(id=areaID)
	check_object_user_owner(request, area)
	area.delete()
	return HttpResponseRedirect('/areas.html')

@login_required(login_url='/login/')
def deleteCreature(request, creatureID):
	creature = Creature.objects.get(id=creatureID)
	check_object_user_owner(request, creature)
	creature.delete()
	return HttpResponseRedirect('/creatures.html')

class EditItem(LoginRequiredMixin, CheckIsOwnerMixin, UpdateView):
	model = Item
	form_class = AddItemForm
	template_name = 'formPage.html'

	def get_context_data(self, **kwargs):
		context = super(EditItem, self).get_context_data(**kwargs)
		context['content'] = 'Edit item'
		context['value'] = 'Update' 
		return context

class EditArea(LoginRequiredMixin, CheckIsOwnerMixin, UpdateView):
	model = Area
	form_class = AddAreaForm
	template_name = 'areaForm.html'

	def get_context_data(self, **kwargs):
		context = super(EditArea, self).get_context_data(**kwargs)
		context['content'] = 'Edit area'
		context['value'] = 'Update' 
		return context

class EditCreature(LoginRequiredMixin, CheckIsOwnerMixin, UpdateView):
	model = Creature
	form_class = AddCreatureForm
	template_name = 'creatureForm.html'

	def get_context_data(self, **kwargs):
		context = super(EditCreature, self).get_context_data(**kwargs)
		context['content'] = 'Edit creature'
		context['value'] = 'Update' 
		return context

@login_required(login_url='/login/')
def addDropForItem(request, itemID):
	"""
	  Permits the addition of a drop using the item page
	"""
	item = Item.objects.get(id=itemID)
	if request.method == 'POST':
		dropForm = AddDropForItemForm(request.POST)
		if dropForm.is_valid():
			drop = dropForm.save(commit=False)
			drop.itemID = item
			if not Drops.objects.filter(itemID=itemID).filter(creatureID=drop.creatureID).exists():
				drop.save()
			return HttpResponseRedirect('/items/'+itemID+'.html')
	else:
		dropForm = AddDropForItemForm()
	return render(request, 'formPage.html', 
		{'form': dropForm, 'content' : 'Add drop',
		 'value': 'Add'},
		context_instance=RequestContext(request))

@login_required(login_url='/login/')
def addDropForCreature(request, creatureID):
	"""
	  Permits the addition of a drop using the creature page
	"""
	creature = Creature.objects.get(id=creatureID)
	if request.method == 'POST':
		dropForm = AddDropForCreatureForm(request.POST)
		if dropForm.is_valid():
			drop = dropForm.save(commit=False)
			drop.creatureID = creature
			if not Drops.objects.filter(creatureID=creatureID).filter(itemID=drop.itemID).exists():
				drop.save()
			return HttpResponseRedirect('/creatures/'+creatureID+'.html')
	else:
		dropForm = AddDropForCreatureForm()
	return render(request, 'formPage.html', 
		{'form': dropForm, 'content' : 'Add drop',
		 'value': 'Add'},
		context_instance=RequestContext(request))

@login_required(login_url='/login/')
def deleteDrop(request, dropID):
	drop = Drops.objects.get(id=dropID).delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login/')
def addFoundForItem(request, itemID):
	"""
	  Permits the addition of a found using the item page
	"""
	item = Item.objects.get(id=itemID)
	if request.method == 'POST':
		foundForm = AddFoundForItemForm(request.POST)
		if foundForm.is_valid():
			found = foundForm.save(commit=False)
			found.itemID = item
			if not Found.objects.filter(itemID=itemID).filter(areaID=found.areaID).exists():
				found.save()
			return HttpResponseRedirect('/items/'+itemID+'.html')
	else:
		foundForm = AddFoundForItemForm()
	return render(request, 'formPage.html', 
		{'form': foundForm, 'content' : 'Add area found',
		 'value': 'Add'},
		context_instance=RequestContext(request))

@login_required(login_url='/login/')
def addFoundForArea(request, areaID):
	"""
	  Permits the addition of a found using the area page
	"""
	area = Area.objects.get(id=areaID)
	if request.method == 'POST':
		foundForm = AddFoundForAreaForm(request.POST)
		if foundForm.is_valid():
			found = foundForm.save(commit=False)
			found.areaID = area
			if not Found.objects.filter(areaID=areaID).filter(itemID=found.itemID).exists():
				found.save()
			return HttpResponseRedirect('/areas/'+areaID+'.html')
	else:
		foundForm = AddFoundForAreaForm()
	return render(request, 'formPage.html', 
		{'form': foundForm, 'content' : 'Add item found',
		 'value': 'Add'},
		context_instance=RequestContext(request))

@login_required(login_url='/login/')
def deleteFound(request, foundID):
	found = Found.objects.get(id=foundID).delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def addEncounteredForCreature(request, creatureID):
	"""
	  Permits the addition of an encountered using the creature page
	"""
	creature = Creature.objects.get(id=creatureID)
	if request.method == 'POST':
		encounteredForm = AddEncounteredForCreatureForm(request.POST)
		if encounteredForm.is_valid():
			encountered = encounteredForm.save(commit=False)
			encountered.creatureID = creature
			if not Encountered.objects.filter(creatureID=creatureID).filter(areaID=encountered.areaID).exists():
				encountered.save()
			return HttpResponseRedirect('/creatures/'+creatureID+'.html')
	else:
		encounteredForm = AddEncounteredForCreatureForm()
	return render(request, 'formPage.html', 
		{'form': AddEncounteredForCreatureForm, 'content' : 'Add area',
		 'value': 'Add'},
		context_instance=RequestContext(request))

@login_required(login_url='/login/')
def addEncounteredForArea(request, areaID):
	"""
	  Permits the addition of an encountered using the area page
	"""
	area = Area.objects.get(id=areaID)
	if request.method == 'POST':
		encounteredForm = AddEncounteredForAreaForm(request.POST)
		if encounteredForm.is_valid():
			encountered = encounteredForm.save(commit=False)
			encountered.areaID = area
			if not Encountered.objects.filter(areaID=areaID).filter(creatureID=encountered.creatureID).exists():
				encountered.save()
			return HttpResponseRedirect('/areas/'+areaID+'.html')
	else:
		encounteredForm = AddEncounteredForAreaForm()
	return render(request, 'formPage.html', 
		{'form': AddEncounteredForAreaForm, 'content' : 'Add creature',
		 'value': 'Add'},
		context_instance=RequestContext(request))


@login_required(login_url='/login/')
def deleteEncountered(request, encounteredID):
	encountered = Encountered.objects.get(id=encounteredID).delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def createList(request, typeList, titlehead, listUrl, format):
	"""
	  A function that create a list in terms of its parameters
	   typeList: the class of the objects
	   titlehead: the header that will be showed in the page
	   listUrl: permits the creation of the route
	   format: the type of page that will be renderized
	"""
	lis = typeList.objects.all()
	if format == html:
		template = get_template('list.html')
		variables = Context({
			'titlehead': titlehead,
			'element_list': lis,
			'listUrl': listUrl,
			'user': request.user
			})
		output = template.render(variables)
		return HttpResponse(output)
	elif format == json:
		json_response = {}
		elem_type = lis[0].__class__.__name__
		json_response[titlehead] = [ { (elem_type + ' ID') : elem.id , elem_type + ' Name' : elem.name } for elem in lis ]
		return HttpResponse(jsn.dumps(json_response, indent=json_indent_level, separators=(',', ' : ')), 
			content_type="application/json")
	elif format == xml:
		data = Element(listUrl.title())
		className = typeList.__name__
		for list_element in lis:
			element_object = SubElement(data, className.title())
			SubElement(element_object, className+'_ID').text = str(list_element.id)
			SubElement(element_object, className+'_Name').text = list_element.name	

		return HttpResponse(tostring(data), content_type="application/xml")
	else:
		return HttpResponseNotFound(format_error)

def itemClassListPage(request, format=html):
	"""
	  Shows the list of item classes in the application
	"""
	return createList(request, ItemClass, 'Item classes', 'itemclasses', format)

def areaListPage(request, format=html):
	"""
	  Shows the list of areas in the application
	"""
	return createList(request, Area, 'Areas', 'areas', format)

def creatureListPage(request, format=html):
	"""
	  Shows the list of creatures in the application
	"""
	return createList(request, Creature, 'Creatures', 'creatures', format)

def itemListPage(request, format=html):
	"""
	  Shows the list of items in the application
	"""
	return createList(request, Item, 'Items', 'items', format)

def itemPage(request, itemID, format=html):
	"""
	  Shows a specific item characterized by his name, description,
	  type, areas that can be found and creatures that drop it.
	"""
	try:
		item = Item.objects.get(id=itemID)
	except:
		raise Http404('Item not found.')

	areas = Area.objects.filter(found__itemID=item.id)
	founds = Found.objects.filter(itemID=item.id)
	drops = Drops.objects.filter(itemID=itemID)
	
	if format == html:
		template = get_template('itemPage.html')
		variables = Context({
			'titlehead': 'Item',
			'item': item,
			'founds': founds,
			'drops': drops,
			'user': request.user,
			'RATING_CHOICES': ItemReview.RATING_CHOICES,
			})
		#output = template.render(variables, context_instance=RequestContext(request))
		return render_to_response('itemPage.html', RequestContext(request, variables))
		#return HttpResponse(output)

	elif format == json:
		json_response = {}
		json_response['Item ID'] = item.id
		json_response['Item Name'] = item.name 
		json_response['Description'] = item.desc
		json_response['Class'] = { 'Class ID' : item.typeID.id, 'Class Name' : item.typeID.name }
		json_response['Found in'] = [ { 'Area ID' : area.id, 'Area name' : area.name } for area in areas ]
		json_response['Dropped by'] = [ { 'Creature ID' : drop.creatureID.id, 
			'Creature Name' : drop.creatureID.name , 'Drop Rate' : drop.dropRate } for drop in drops ]

		return HttpResponse(jsn.dumps(json_response, indent=json_indent_level, separators=(',', ' : ')), 
			content_type="application/json")
	elif format == xml:
		data = Element('Item')
		SubElement(data, 'Item_ID').text = str(item.id)
		SubElement(data, 'Item_Name').text = item.name
		SubElement(data, 'Description').text = item.desc
		item_class = SubElement(data, 'Class')
		SubElement(item_class, 'Class_ID').text = str(item.typeID.id)
		SubElement(item_class, 'Class_Name').text = item.typeID.name
		found_in = SubElement(data, 'Found_in')
		for area in areas:
			area_object = SubElement(found_in, 'Area')
			SubElement(area_object, 'Area_ID').text = str(area.id)
			SubElement(area_object, 'Area_Name').text = area.name
		
		dropped_by = SubElement(data, 'Dropped_by')
		for drop in drops:
			drop_object = SubElement(dropped_by, 'Drop')
			SubElement(drop_object, 'Creature_ID').text = str(drop.creatureID.id)	
			SubElement(drop_object, 'Creature_Name').text = drop.creatureID.name
			SubElement(drop_object, 'Drop_Rate').text = str(drop.dropRate)

		return HttpResponse(tostring(data), content_type="application/xml")
	else:
		return HttpResponseNotFound(format_error)

def itemClassPage(request, itemClassID, format=html):
	"""
	  Shows a specific item characterized by his name, description,
	  areas that can be found and creatures that drop it.
	"""
	try:
		itemClass = ItemClass.objects.get(id=itemClassID)
	except:
		raise Http404('Item class not found.')

	items = Item.objects.filter(typeID=itemClass.id)

	if format == html:
		template = get_template('itemClassPage.html')
		variables = Context({
			'titlehead': 'Item class',
			'itemClass': itemClass,
			'items': items,
			'user': request.user,
			})
		output = template.render(variables)
		return HttpResponse(output)
	elif format == json:
		json_response = {}
		json_response['Class ID'] = itemClass.id
		json_response['Class Name'] = itemClass.name
		json_response['Class Description'] = itemClass.desc
		json_response['Items in class'] = [ {'Item ID' : item.id, 'Item Name' : item.name} for item in items]

		return HttpResponse(jsn.dumps(json_response, indent=json_indent_level, separators=(',', ' : ')), 
			content_type="application/json")
	elif format == xml:
		data = Element('Item_class')
		SubElement(data, 'Itemclass_ID').text = str(itemClass.id)
		SubElement(data, 'Itemclass_Name').text = itemClass.name
		SubElement(data, 'Description').text = itemClass.desc
		found_in = SubElement(data, 'Items_in_class')
		for item in items:
			area_object = SubElement(found_in, 'Item')
			SubElement(area_object, 'Item_ID').text = str(item.id)
			SubElement(area_object, 'Item_Name').text = item.name

		return HttpResponse(tostring(data), content_type="application/xml")
	else:
		return HttpResponseNotFound(format_error)

def creaturePage(request, creatureID, format=html):
	"""
	  Shows a specific creature characterized by his name, description,
	  if it is unique, the danger level, the number of souls dropped,
	  areas that can be found and items that drops.
	"""
	try:
		creature = Creature.objects.get(id=creatureID)
	except:
		raise Http404('Creature not found.')

	drops = Drops.objects.filter(creatureID=creatureID)
	areas = creature.areas.all()
	encountereds = Encountered.objects.filter(creatureID=creatureID)

	if format == html:
		template = get_template('creaturePage.html')
		variables = Context({
			'titlehead': 'Creature',
			'creature': creature,
			'drops': drops,
			'encountereds': encountereds,
			'user': request.user,
			})
		output = template.render(variables)
		return HttpResponse(output)
	elif format == json:
		json_response = {}
		json_response['Creature ID'] = creature.id
		json_response['Creature Name'] = creature.name
		json_response['Is Unique?'] = creature.unique
		json_response['Danger Level'] = creature.dangerLevel
		json_response['Souls Obtained'] = creature.souls
		json_response['Drops'] = \
			[ {'Item ID' : drop.itemID.id, 'Item Name' : drop.itemID.name, 'Drop Rate' : drop.dropRate} for drop in drops ]
		json_response['Found In'] = [ {'Area ID' : area.id, 'Area Name' : area.name} for area in areas ]

		return HttpResponse(jsn.dumps(json_response, indent=json_indent_level, separators=(',', ' : ')), 
			content_type="application/json")
	elif format == xml:
		data = Element('Creature')
		SubElement(data, 'Creature_ID').text = str(creature.id)
		SubElement(data, 'Creature_Name').text = creature.name
		SubElement(data, 'Description').text = creature.desc
		SubElement(data, 'Is_Unique').text = str(creature.unique)
		SubElement(data, 'Danger_Level').text = str(creature.dangerLevel)
		SubElement(data, 'Souls_Obtained').text = str(creature.souls)
		
		enemy_drops = SubElement(data, 'Dropped_by')
		for drop in drops:
			drop_object = SubElement(enemy_drops, 'Drops')
			SubElement(drop_object, 'Item_ID').text = str(drop.itemID.id)	
			SubElement(drop_object, 'Item_Name').text = drop.itemID.name
			SubElement(drop_object, 'Drop_Rate').text = str(drop.dropRate)

		found_in = SubElement(data, 'Found_in')
		for area in areas:
			area_object = SubElement(found_in, 'Area')
			SubElement(area_object, 'Area_ID').text = str(area.id)
			SubElement(area_object, 'Area_Name').text = area.name

		return HttpResponse(tostring(data), content_type="application/xml")
	else:
		return HttpResponseNotFound(format_error)

def areaPage(request, areaID, format=html):
	"""
	  Shows a specific area characterized by his name, description,
	  areas that can be found and creatures that drop it.
	"""
	try:
		area = Area.objects.get(id=areaID)
	except:
		raise Http404('Area not found.')

	items = Item.objects.filter(found__areaID=area.id)
	founds = Found.objects.filter(areaID=area.id)
	creatures = Creature.objects.filter(areas=area.id)
	encountereds = Encountered.objects.filter(areaID=area.id)

	if format == html:
		template = get_template('areaPage.html')
		variables = Context({
			'titlehead': 'Area',
			'area': area,
			'founds': founds,
			'encountereds': encountereds,
			'user': request.user,
			})
		output = template.render(variables)
		return HttpResponse(output)
	elif format == json:
		json_response = {}
		json_response['Area ID'] = area.id
		json_response['Area Name'] = area.name
		json_response['Items Found'] = [ {'Item ID' : item.id,'Item Name' : item.name} for item in items ]
		json_response['Creatures Found'] = \
			[ {'Creature ID' : creature.id ,'Creature Name' : creature.name } for creature in creatures ]
		return HttpResponse(jsn.dumps(json_response, indent=json_indent_level, separators=(',', ' : ')),
			content_type="application/json")
	elif format == xml:
		data = Element('Area')
		SubElement(data, 'Area_ID').text = str(area.id)
		SubElement(data, 'Area_Name').text = area.name
		SubElement(data, 'Description').text = area.desc
		
		items_found = SubElement(data, 'Items_Found')
		for item in items:
			item_object = SubElement(items_found, 'Item')
			SubElement(item_object, 'Item_ID').text = str(item.id)	
			SubElement(item_object, 'Item_Name').text = item.name

		creatures_found = SubElement(data, 'Creatures_Found')
		for creature in creatures:
			creature_object = SubElement(creatures_found, 'Creature')
			SubElement(creature_object, 'Creature_ID').text = str(creature.id)
			SubElement(creature_object, 'Creature_Name').text = creature.name

		return HttpResponse(tostring(data), content_type="application/xml")
	else:
		return HttpResponseNotFound(format_error)

#RESTFUL API Views

#API Root View
@api_view(('GET',))
def api_index(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'items': reverse('item-list', request=request, format=format),
		'item_classes': reverse('itemclass-list', request=request, format=format),
		'areas': reverse('area-list', request=request, format=format),
		'creatures': reverse('creature-list', request=request, format=format),
		'founds': reverse('found-list', request=request, format=format),
		'users_items': reverse('useritems-list', request=request, format=format),
		'drops': reverse('drops-list', request=request, format=format),
		'encountereds' : reverse('encountered-list', request=request, format=format),
		'reviews' : reverse('itemreview-list', request=request, format=format),
	})

api_permissions_owner = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
api_permissions_authoro = (permissions.IsAuthenticatedOrReadOnly,)

class APIUserList(generics.ListAPIView):
	permission_classes = api_permissions_authoro
	model = User
	serializer_class = UserSerializer

class APIUserDetail(generics.RetrieveAPIView):
	permission_classes = api_permissions_authoro
	model = User
	serializer_class = UserSerializer

class APIItemClassList(generics.ListAPIView):
	permission_classes = api_permissions_authoro
	model = ItemClass
	serializer_class = ItemClassSerializer

class APIItemClassDetail(generics.RetrieveAPIView):
	permission_classes = api_permissions_authoro
	model = ItemClass
	serializer_class = ItemClassSerializer

class APIAreaList(generics.ListCreateAPIView):
	permission_classes = api_permissions_authoro
	model = Area
	serializer_class = AreaSerializer
	def pre_save(self, obj):
		obj.date = date.today()
		obj.user = self.request.user

class APIAreaDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = api_permissions_owner
	model = Area
	serializer_class = AreaSerializer
	def pre_save(self, obj):
		obj.user = self.request.user

class APICreatureList(generics.ListCreateAPIView):
	permission_classes = api_permissions_authoro
	model = Creature
	serializer_class = CreatureSerializer
	def pre_save(self, obj):
		obj.date = date.today()
		obj.user = self.request.user

class APICreatureDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = api_permissions_owner
	model = Creature
	serializer_class = CreatureSerializer
	def pre_save(self, obj):
		obj.user = self.request.user

class APIItemList(generics.ListCreateAPIView):
	permission_classes = api_permissions_authoro
	model = Item
	serializer_class = ItemSerializer
	def pre_save(self, obj):
		obj.date = date.today()
		obj.user = self.request.user

class APIItemDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = api_permissions_owner
	model = Item
	serializer_class = ItemSerializer
	def pre_save(self, obj):
		obj.user = self.request.user

class APIFoundList(generics.ListCreateAPIView):
	permission_classes = api_permissions_authoro
	model = Found
	serializer_class = FoundSerializer

class APIFoundDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = api_permissions_authoro
	model = Found
	serializer_class = FoundSerializer

class APIUserItemsList(generics.ListCreateAPIView):
	permission_classes = api_permissions_authoro
	model = UserItems
	serializer_class = UserItemsSerializer
	def pre_save(self, obj):
		obj.userID = self.request.user

class APIUserItemsDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = api_permissions_authoro
	model = UserItems
	serializer_class = UserItemsSerializer
	def pre_save(self, obj):
		obj.userID = self.request.user

class APIDropsList(generics.ListCreateAPIView):
	permission_classes = api_permissions_authoro
	model = Drops
	serializer_class = DropsSerializer

class APIDropsDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = api_permissions_authoro
	model = Drops
	serializer_class = DropsSerializer

class APIEncounteredList(generics.ListCreateAPIView):
	permission_classes = api_permissions_authoro
	model = Encountered
	serializer_class = EncounteredSerializer

class APIEncounteredDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = api_permissions_authoro
	model = Encountered
	serializer_class = EncounteredSerializer

class APIItemReviewList(generics.ListCreateAPIView):
	permission_classes = api_permissions_authoro
	model = ItemReview
	serializer_class = ItemReviewSerializer
	def pre_save(self, obj):
		obj.date = date.today()
		obj.user = self.request.user

class APIItemReviewDetail(generics.RetrieveAPIView):
	permission_classes = api_permissions_authoro
	model = ItemReview
	serializer_class = ItemReviewSerializer
	def pre_save(self, obj):
		obj.user = self.request.user