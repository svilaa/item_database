from django.contrib import admin
from iitem_database.models import Item, ItemClass, Area, Creature, Drops, Found, Encountered

admin.site.register(Item)
admin.site.register(ItemClass)
admin.site.register(Area)
admin.site.register(Creature)
admin.site.register(Drops)
admin.site.register(Found)
admin.site.register(Encountered)
