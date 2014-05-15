from django.db import models
from django.contrib.auth.models import User
from datetime import date

def get_default_user():
    return User.objects.get(pk=1)
    
class ItemClass(models.Model):
	"""
	  The items are classified by his type, can be swords, shields,
	  armors, helmets, healing objects, multiplayer objects, etc
	"""
	#id automatic generated by Django
	name = models.CharField(max_length=50, unique=True)
	desc = models.TextField(max_length=400)
	user = models.ForeignKey(User, default=get_default_user)
	date = models.DateField(default=date.today)

	def __unicode__(self):
		return self.name

class Item(models.Model):
	"""
	  An item is a object that the player can use, wear or wield
	"""
	#id automatic generated by Django
	name = models.CharField(max_length=50, unique=True)
	desc = models.TextField(max_length=400)
	creatures = models.ManyToManyField('Creature', blank=True, through='Drops')
	areas = models.ManyToManyField('Area', blank=True, through='Found')
	typeID = models.ForeignKey(ItemClass, related_name='item type')
	user = models.ForeignKey(User, default=get_default_user)
	date = models.DateField(default=date.today)

	def __unicode__(self):
		return self.name

class Area(models.Model):
	"""
	  An area is the place where items and enemies where found
	"""
	#id automatic generated by Django
	name = models.CharField(max_length=50, unique=True)
	desc = models.TextField(max_length=400)
	user = models.ForeignKey(User, default=get_default_user)
	date = models.DateField(default=date.today)

	def __unicode__(self):
		return self.name

class Creature(models.Model):
	"""
	  A creature has a danger level deppends of his aggressiveness, located in one or more
	  areas, and drops souls (the currency of the game). This can be unique for many reasons
	  (a boss, a special enemy, is part of the story, etc)
	"""
	#id automatic generated by Django
	name = models.CharField(max_length=50, unique=True)
	desc = models.TextField(max_length=400)
	dangerLevel = models.IntegerField()
	souls = models.PositiveIntegerField()
	unique = models.BooleanField()
	areas = models.ManyToManyField(Area, blank=True, through='Encountered')
	user = models.ForeignKey(User, default=get_default_user)
	date = models.DateField(default=date.today)
	
	def __unicode__(self):
		return self.name

class Encountered(models.Model):
	creature = models.ForeignKey(Creature, related_name='c1')
	area = models.ForeignKey(Area, related_name='area1')


class Drops(models.Model):
	"""
	  Associates an item and a creature with a specific drop rate to obtain the item
	"""
	itemID = models.ForeignKey(Item)
	creatureID = models.ForeignKey(Creature)
	dropRate = models.FloatField()

	def __unicode__(self):
		return self.itemID.name + " - " + self.creatureID.name

class Found(models.Model):
	"""
	  Associates an item and an area
	"""
	itemID = models.ForeignKey(Item)
	areaID = models.ForeignKey(Area)

	def __unicode__(self):
		return self.itemID.name + " - " + self.areaID.name
		
class UserItems(models.Model):
	"""
	  Stores the quantity of the item that has an user
	"""
	userID = models.ForeignKey(User)
	itemID = models.ForeignKey(Item)
	quantity = models.PositiveIntegerField()
	def __unicode__(self):
		return self.userID.username + " - " + self.itemID.name + " - " + str(self.quantity)
