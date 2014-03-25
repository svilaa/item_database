# Create your views here.
import json as jsn
from xml.etree.ElementTree import Element, SubElement, tostring

from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.template import Context
from django.template.loader import get_template
from iitem_database.models import ItemClass, Area, Creature, Item, Found, UserItems, Drops
from django.contrib.auth.models import User

html = 'html'
json = 'json'
xml = 'xml'

format_error = "Format not found."

json_indent_level = 4

def mainpage(request):
	template = get_template('mainpage.html')
	variables = Context({
		'titlehead': 'Item database',
		'pagetitle': 'Welcome',
		'user': request.user,
		})
	output = template.render(variables)
	return HttpResponse(output)

def userpage(request, username, format=html):
	try:
		user = User.objects.get(username=username)
	except:
		raise Http404('User not found.')

	userItems = UserItems.objects.filter(userID=user.id)

	if format == html:
		template = get_template('userpage.html')
		variables = Context({
			'username': username,
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
			item_object = SubElement(user_items, 'User_Items')
			SubElement(item_object, 'Item_ID').text = str(userItem.itemID.id)
			SubElement(item_object, 'Item_Name').text = userItem.itemID.name
			SubElement(item_object, 'Quantity').text = str(userItem.quantity)		

		return HttpResponse(tostring(data), content_type="application/xml")
	else:
		return HttpResponseNotFound(format_error)

def createList(typeList, titlehead, listUrl, format):

	lis = typeList.objects.all()
	if format == html:
		template = get_template('list.html')
		variables = Context({
			'titlehead': titlehead,
			'element_list': lis,
			'listUrl': listUrl,
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
	return createList(ItemClass, 'Item classes', 'itemclasses', format)

def areaListPage(request, format=html):
	return createList(Area, 'Areas', 'areas', format)

def creatureListPage(request, format=html):
	return createList(Creature, 'Creatures', 'creatures', format)

def itemListPage(request, format=html):
	return createList(Item, 'Items', 'items', format)

def itemPage(request, itemID, format=html):
	try:
		item = Item.objects.get(id=itemID)
	except:
		raise Http404('Item not found.')

	areas = Area.objects.filter(found__itemID=item.id)
	drops = Drops.objects.filter(itemID=itemID)
	
	if format == html:
		template = get_template('itemPage.html')
		variables = Context({
			'titlehead': 'Item',
			'item': item,
			'areas': areas,
			'drops': drops,
			})
		output = template.render(variables)
		return HttpResponse(output)
	elif format == json:
		json_response = {}
		json_response['Item ID'] = item.id
		json_response['Item Name'] = item.name 
		json_response['Description'] = item.desc
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

def itemClassPage(request, classItemID, format=html):
	try:
		itemClass = ItemClass.objects.get(id=classItemID)
	except:
		raise Http404('Item class not found.')

	items = Item.objects.filter(typeID=itemClass.id)

	if format == html:
		template = get_template('itemClassPage.html')
		variables = Context({
			'titlehead': 'Item class',
			'itemClass': itemClass,
			'items': items,
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
	try:
		creature = Creature.objects.get(id=creatureID)
	except:
		raise Http404('Creature not found.')

	drops = Drops.objects.filter(creatureID=creatureID)
	areas = creature.areas.all()

	if format == html:
		template = get_template('creaturePage.html')
		variables = Context({
			'titlehead': 'Creature',
			'creature': creature,
			'drops': drops,
			'areas': areas,
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
	try:
		area = Area.objects.get(id=areaID)
	except:
		raise Http404('Area not found.')

	items = Item.objects.filter(found__areaID=area.id)
	creatures = Creature.objects.filter(areas=area.id)
		
	if format == html:
		template = get_template('areaPage.html')
		variables = Context({
			'titlehead': 'Area',
			'area': area,
			'items': items,
			'creatures': creatures,
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
