from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Customer (models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE) #this is the user model
    #of our admin panel, we havent added any new field here.
    
    
    #extra fields
    
    phone_field = models.CharField(max_length=12, blank=False)
    
    
    def __str__(self):
     return self.user.username
 
class Category(models.Model):
    category_name=models.CharField(max_length=200)
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey('Category', on_delete=models.CASCADE) #category is a foreign key cuz it is related and 
    #dependable on the category class (primary key) and on_delete -> when a category is deleted all product will also be
    desc=models.TextField() #product description
    price=models.FloatField(default=0.0) #product price
    product_available_count=models.IntegerField(default=0)#if a customer orders a product but we don't have that amount
    #of product we should check on the check out if the product count is less that this product available count.
    img=models.ImageField(blank = True)#image of product
    date = models.DateField(auto_now=True)
    
    
    
    #def get_add_to_cart_url(self):
       # return reverse("core:add-to-cart",kwargs={
        #"pk":self.pk
   # })
    
    def __str__(self):
        return self.name
    
class OrderItem(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False) #when an order is processed the ordered value should be false and its only at the time of payment that it is going to be true as a response from the payment integration mode.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self): #str function in a django model returns a string that is exactly rendered as the display name of instances for that model.
        return f"{self.quantity} of {self.product.name}"
    
    def get_total_item_price(self):  
        return self.quantity * self.product.price
                                #those 2 are for an item added to a product
    def get_final_price(self):
        return self.get_total_item_price()
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem) #many to many means that an order item can belong to many orders and vice verca
   # start_date = models.DateTimeField(auto_now_add = True) #the time when the first item is added to cart
    ordered_date = models.DateTimeField() #the date after successful submission of the payment
    ordered = models.BooleanField(default = False) 
    order_id = models.CharField(max_length=100, unique=True, default=None, blank=True, null=True) 
 
    
    
    
    def save(self, *args, **kwargs): #overwriting the save method meaning saving the instance created from a particular model(order_id in our case)
        if self.order_id is None and self.datetime_ofpayment and self.id: #sekf.id is the id of the user
            self.order_id = self.datetime_ofpayment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        #so when an order is created if the order doesnt have an id and the conditions in the if are fulfilled an id will be produced in the above format
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username
    
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total    #initialize total price = 0 loop through and add all the orderitems 
    def get_total_count(self):
        order = Order.objects.get(pk=self.pk) #get each object by its is and and return the tot no of products.
        return order.items.count()
    

                
    
    
    
 
