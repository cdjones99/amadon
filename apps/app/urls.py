from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$',views.index),
	url(r'^register$',views.register),
	url(r'^login$',views.login),
	url(r'^home$',views.home),
	url(r'^item$',views.item),
	url(r'^addItem$',views.addItem),
	url(r'^editItem$',views.editItem),
	url(r'^shopping_cart/(?P<id>\d+)$',views.addOrder),
	url(r'^delete/(?P<id>\d+)$',views.delete),
	url(r'^renderCart$',views.renderCart),
	url(r'^purchase$',views.purchase),
	url(r'^clear_cart$',views.clear_cart),
	url(r'^logout$',views.logout),
]