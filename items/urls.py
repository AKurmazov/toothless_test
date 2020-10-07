from django.urls import path

from items.views import index, item_details, buy_item, thanks


urlpatterns = [
    path('', index, name='index'),
    path('item/<pk>', item_details, name='item_details'),
    path('buy/<pk>', buy_item, name='buy_item'),
    path('thanks', thanks, name='thanks'),
]
