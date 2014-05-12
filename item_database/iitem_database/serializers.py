from rest_framework import serializers
from django.contrib.auth.models import User
from iitem_database.models import ItemClass, Area, Creature, Item, Found, UserItems, Drops

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'id', 'username')

class ItemClassSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ItemClass
		fields = ('url', 'id', 'name', 'desc', 'user', 'date')

class AreaSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Area
		fields = ('url', 'id', 'name', 'desc', 'user', 'date')

class CreatureSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Creature
		fields = ('url', 'id', 'name', 'desc', 'dangerLevel', \
			'souls', 'unique', 'areas', 'user', 'date')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Item
		fields = ('url', 'id', 'name', 'desc', 'typeID', 'user', 'date')

class FoundSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Found
		fields = ('url', 'id', 'itemID', 'areaID')

class UserItemsSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = UserItems
		fields = ('url', 'id', 'userID', 'itemID', 'quantity')

class DropsSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Drops
		fields = ('url', 'id', 'itemID', 'creatureID', 'dropRate')