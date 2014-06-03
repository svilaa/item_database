from django.contrib import admin
from iitem_database.models import Item, ItemClass, Area, Creature, Drops, Found, UserItems, ItemReview

admin.site.register(Item)
admin.site.register(ItemClass)
admin.site.register(Area)
admin.site.register(Creature)
admin.site.register(Drops)
admin.site.register(Found)
admin.site.register(UserItems)
admin.site.register(ItemReview)