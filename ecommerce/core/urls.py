from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name="index"), #for the '' our default url, run the index function in views.py
                                        #and the name is something that represents the route or url
    path('add_product', views.add_product, name = "add_product"),
    path('product_desc/<pk>', views.product_desc, name= "product_desc"), 
    path('add_to_cart/<pk>', views.add_to_cart, name= "add_to_cart"),
    path('orderlist', views.orderlist, name = "orderlist"),
    path('add_item/<pk>', views.add_item, name = "add_item"),
    path('remove_item/<pk>', views.remove_item, name="remove_item"),
    path('checkout_page', views.checkout_page, name = "checkout_page"),
]                                       
