from django.conf.urls import url
from . import views

urlpatterns = [
    # GET ROUTES
    url(r'^$', views.main, name='get_main'),
    url(r'^dashboard$', views.dashboard, name='get_dashboard'),    
    url(r'^wish_items(?P<item_id>\d+)$', views.wish_items, name='get_item'),
    url(r'^wish_items/create$', views.create, name='get_create'),

    # POST ROUTES
    url(r'^login$', views.login, name='post_login'),
    url(r'^register$', views.register, name='post_register'),
    url(r'^wish_items/add_item$', views.add_item, name='post_add_item'),
]