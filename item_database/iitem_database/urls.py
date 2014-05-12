from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from iitem_database.views import APIUserList, APIUserDetail
from iitem_database.views import APIItemList, APIItemDetail
from iitem_database.views import APIItemClassList, APIItemClassDetail
from iitem_database.views import APIAreaList, APIAreaDetail
from iitem_database.views import APICreatureList, APICreatureDetail
from iitem_database.views import APIFoundList, APIFoundDetail
from iitem_database.views import APIUserItemsList, APIUserItemsDetail
from iitem_database.views import APIDropsList, APIDropsDetail

urlpatterns = patterns('',
	#REST API URLS
	url(r'^$', 'iitem_database.views.api_index', name='api_root'),

	url(r'user/$', APIItemList.as_view(), name='user-list'),
	url(r'user/(?P<pk>\d+)/$', APIItemDetail.as_view(), name='user-detail'),

	url(r'item/$', APIItemList.as_view(), name='item-list'),
	url(r'item/(?P<pk>\d+)/$', APIItemDetail.as_view(), name='item-detail'),

	url(r'itemclass/$', APIItemClassList.as_view(), name='itemclass-list'),
	url(r'itemclass/(?P<pk>\d+)/$', APIItemClassDetail.as_view(), name='itemclass-detail'),

	url(r'area/$', APIAreaList.as_view(), name='area-list'),
	url(r'area/(?P<pk>\d+)/$', APIAreaDetail.as_view(), name='area-detail'),

	url(r'creature/$', APICreatureList.as_view(), name='creature-list'),
	url(r'creature/(?P<pk>\d+)/$', APICreatureDetail.as_view(), name='creature-detail'),

	url(r'found/$', APIFoundList.as_view(), name='found-list'),
	url(r'found/(?P<pk>\d+)/$', APIFoundDetail.as_view(), name='found-detail'),

	url(r'useritems/$', APIUserItemsList.as_view(), name='useritems-list'),
	url(r'useritems/(?P<pk>\d+)/$', APIUserItemsDetail.as_view(), name='useritems-detail'),

	url(r'drops/$', APIDropsList.as_view(), name='drops-list'),
	url(r'drops/(?P<pk>\d+)/$', APIDropsDetail.as_view(), name='drops-detail'),

	url(r'^login/', include('rest_framework.urls',
    	namespace='rest_framework')),
)

urlpatterns = format_suffix_patterns(urlpatterns)