# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from iitem_database.models import ItemClass, Area, Creature, Item, Found, Encountered
from django.contrib.auth.models import User

def mainpage(request):
	template = get_template('mainpage.html')
	variables = Context({
		'titlehead': 'Item database',
		'pagetitle': 'Welcome',
		'user': request.user
		})
	output = template.render(variables)
	return HttpResponse(output)

def userpage(request, username):
	try:
		user = User.objects.get(username=username)
	except:
		raise Http404('User not found.')

	template = get_template('userpage.html')
	variables = Context({
		'username': username
		})
	output = template.render(variables)
	return HttpResponse(output)

def createList(typeList, titlehead):
	template = get_template('list.html')
	lis = typeList.objects.all()
	variables = Context({
		'titlehead': titlehead,
		'element_list': lis,
		})
	output = template.render(variables)
	return HttpResponse(output)

def itemClassListPage(request):
	return createList(ItemClass, 'Item classes')

def areaListPage(request):
	return createList(Area, 'Areas')

def creatureListPage(request):
	return createList(Creature, 'Creatures')

def itemListPage(request):
	return createList(Item, 'Items')

def itemPage(request, itemName):
	try:
		item = Item.objects.get(name=itemName)
	except:
		raise Http404('Item not found.')
	template = get_template('itemPage.html')
	areas = Area.objects.filter(found__itemID=item.id)
	creatures = Creature.objects.filter(drops__itemID=item.id)
	variables = Context({
		'titlehead': 'Item',
		'item': item,
		'areas': areas,
		'creatures': creatures,
		})
	output = template.render(variables)
	return HttpResponse(output)

def itemClassPage(request, classItemName):
	try:
		itemClass = ItemClass.objects.get(name=classItemName)
	except:
		raise Http404('Item class not found.')
	template = get_template('itemClassPage.html')
	items = Item.objects.filter(typeID=itemClass.id)
	variables = Context({
		'titlehead': 'Item class',
		'itemClass': itemClass,
		'items': items,
		})
	output = template.render(variables)
	return HttpResponse(output)

def creaturePage(request, creatureItemName):
	try:
		creature = Creature.objects.get(name=creatureItemName)
	except:
		raise Http404('Creature not found.')
	template = get_template('creaturePage.html')
	items = Item.objects.filter(drops__creatureID=creature.id)
	areas = Area.objects.filter(encountered__creatureID=creature.id)
	variables = Context({
		'titlehead': 'Item class',
		'creature': creature,
		'items': items,
		'areas': areas,
		})
	output = template.render(variables)
	return HttpResponse(output)

def areaPage(request, areaItemName):
	try:
		area = Area.objects.get(name=areaItemName)
	except:
		raise Http404('Area not found.')
	template = get_template('areaPage.html')
	items = Item.objects.filter(found__areaID=area.id)
	creatures = Creature.objects.filter(encountered__areaID=area.id)
	variables = Context({
		'titlehead': 'Item class',
		'area': area,
		'items': items,
		'creatures': creatures,
		})
	output = template.render(variables)
	return HttpResponse(output)