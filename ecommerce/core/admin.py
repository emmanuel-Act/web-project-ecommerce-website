from django.contrib import admin
from core.models import * # import all models from models.py of the core app (module)
# Register your models here.

admin.site.register(Customer) #register the model (Customer model)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)

