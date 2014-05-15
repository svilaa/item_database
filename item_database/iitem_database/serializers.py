from rest_framework import serializers
from django.contrib.auth.models import User
from iitem_database.models import ItemClass, Area, Creature, \
									Item, Found, UserItems, Drops, Encountered

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'id', 'username', 'useritems_set')

class ItemClassSerializer(serializers.HyperlinkedModelSerializer):
	date = serializers.DateTimeField(read_only=True)
	class Meta:
		model = ItemClass
		fields = ('url', 'id', 'name', 'desc', 'user', 'date', 'item_set')

class AreaSerializer(serializers.HyperlinkedModelSerializer):
	date = serializers.DateTimeField(read_only=True)
	class Meta:
		model = Area
		fields = ('url', 'id', 'name', 'desc', 'user', \
			'date', 'item_set', 'creature_set')

class CreatureSerializer(serializers.HyperlinkedModelSerializer):
	date = serializers.DateTimeField(read_only=True)
	class Meta:
		model = Creature
		fields = ('url', 'id', 'name', 'desc', 'dangerLevel', \
			'souls', 'unique', 'user', 'date', 'areas', 'item_set')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
	date = serializers.DateTimeField(read_only=True)
	class Meta:
		model = Item
		fields = ('url', 'id', 'name', 'desc', 'typeID', \
			'user', 'date', 'areas', 'creatures')

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

class EncounteredSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Encountered
		field = ('url', 'id', 'creature', 'area')