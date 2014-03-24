# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from iitem_database.models import ItemClass, Area, Creature, Item, Found, UserItems, Drops
from django.contrib.auth.models import User

def mainpage(request):
	template = get_template('mainpage.html')
	variables = Context({
		'titlehead': 'Item database',
		'pagetitle': 'Welcome',
		'user': request.user,
		})
	output = template.render(variables)
	return HttpResponse(output)

def userpage(request, username):
	try:
		user = User.objects.get(username=username)
	except:
		raise Http404('User not found.')
	template = get_template('userpage.html')
	userItems = UserItems.objects.filter(userID=user.id)
	variables = Context({
		'username': username,
		'userItems': userItems,
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

def itemPage(request, itemID):
	try:
		item = Item.objects.get(id=itemID)
	except:
		raise Http404('Item not found.')
	template = get_template('itemPage.html')
	areas = Area.objects.filter(found__itemID=item.id)
	drops = Drops.objects.filter(itemID=itemID)
	variables = Context({
		'titlehead': 'Item',
		'item': item,
		'areas': areas,
		'drops': drops,
		})
	output = template.render(variables)
	return HttpResponse(output)

def itemClassPage(request, classItemID):
	try:
		itemClass = ItemClass.objects.get(id=classItemID)
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

def creaturePage(request, creatureID):
	try:
		creature = Creature.objects.get(id=creatureID)
	except:
		raise Http404('Creature not found.')
	template = get_template('creaturePage.html')
	drops = Drops.objects.filter(creatureID=creatureID)
	areas = creature.areas.all()
	variables = Context({
		'titlehead': 'Creature',
		'creature': creature,
		'drops': drops,
		'areas': areas,
		})
	output = template.render(variables)
	return HttpResponse(output)

def areaPage(request, areaID):
	try:
		area = Area.objects.get(id=areaID)
	except:
		raise Http404('Area not found.')
		
	template = get_template('areaPage.html')
	items = Item.objects.filter(found__areaID=area.id)
	creatures = Creature.objects.filter(areas=area.id)
	variables = Context({
		'titlehead': 'Area',
		'area': area,
		'items': items,
		'creatures': creatures,
		})
	output = template.render(variables)
	return HttpResponse(output)

