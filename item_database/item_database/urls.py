from django.conf.urls import patterns, include, url
from iitem_database.views import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from rest_framework.urlpatterns import format_suffix_patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'item_database.views.home', name='home'),
    # url(r'^item_database/', include('item_database.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', mainpage, name='home'),
    url(r'^user/(?P<username>\w+)\.(?P<format>\w+)$', userpage),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/register/$', register),
    
    url(r'^user/(?P<username>\w+)/additem/$', addUserItem),
    url(r'^user/(?P<username>\w+)/deleteitem/(?P<item>\w+)$', deleteUserItem),
    url(r'^user/(?P<username>\w+)/item/(?P<item>\w+)/quantity/(?P<quantity>-?\d+)$', quantityUserItem),

    url(r'^items/add/$', ItemCreate.as_view(), name='add-item'),
    url(r'^areas/add/$', AreaCreate.as_view(), name='add-area'),
    url(r'^creatures/add/$', CreatureCreate.as_view(), name='add-creature'),

    url(r'^adddrop/item/(?P<itemID>\w+)/$', addDropForItem),
    url(r'^adddrop/creature/(?P<creatureID>\w+)/$', addDropForCreature),
    url(r'^deletedrop/(?P<dropID>\w+)/$', deleteDrop),

    url(r'^addfound/item/(?P<itemID>\w+)/$', addFoundForItem),
    url(r'^addfound/area/(?P<areaID>\w+)/$', addFoundForArea),
    url(r'^deletefound/(?P<foundID>\w+)/$', deleteFound),

    url(r'^addencountered/creature/(?P<creatureID>\w+)/$', addEncounteredForCreature),
    url(r'^addencountered/area/(?P<areaID>\w+)/$', addEncounteredForArea),
    url(r'^deleteencountered/(?P<encounteredID>\w+)/$', deleteEncountered),

    url(r'^items/delete/(?P<itemID>\w+)$', deleteItem),
    url(r'^areas/delete/(?P<areaID>\w+)$', deleteArea),
    url(r'^creatures/delete/(?P<creatureID>\w+)$', deleteCreature),

    url(r'^items/edit/(?P<pk>\w+)$', EditItem.as_view(), name='edit-item'),
    url(r'^areas/edit/(?P<pk>\w+)$', EditArea.as_view(), name='edit-area'),
    url(r'^creatures/edit/(?P<pk>\w+)$', EditCreature.as_view(), name='edit-creture'),

    url(r'^itemclasses\.(?P<format>\w+)$', itemClassListPage),
    url(r'^itemclasses/(?P<itemClassID>\w+)\.(?P<format>\w+)$', itemClassPage),

    url(r'^areas\.(?P<format>\w+)$', areaListPage),
    url(r'^areas/(?P<areaID>\w+)\.(?P<format>\w+)$', areaPage),

    url(r'^creatures\.(?P<format>\w+)$', creatureListPage),
    url(r'^creatures/(?P<creatureID>\w+)\.(?P<format>\w+)$', creaturePage),

    url(r'^items\.(?P<format>\w+)$', itemListPage),
    url(r'^items/(?P<itemID>\w+)\.(?P<format>\w+)$', itemPage),

    url(r'^api/', include('iitem_database.urls')),
)
