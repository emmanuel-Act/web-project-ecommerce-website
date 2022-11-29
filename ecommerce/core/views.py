from django.shortcuts import render,redirect, get_object_or_404
from core.forms import *
from django.contrib import messages
from core.models import *
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .telegram import send_msg_on_telegram
#Create your views here.
def index(request):
    products = Product.objects.all #grabs all objects of Product model and assign it to products variable
    return render(request,'core/index.html', {'products':products}); #the product value declared above will be assigned to products variable in a context dictionary

def add_product(request):
    if request.method =='POST':
        form=ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print(form)
            form.save()
            print("Data Saved Successfully")
            messages.success(request, "Product Added Successfully")
            return redirect('/')
        else:
            print("Not Working")
            print(form.errors)
            return redirect('add_product')
            messages.info(request, "product Not added")
    else:
        form = ProductForm() 
    return render(request, 'core/add_product.html', {'form':form});

def product_desc(request,pk): 
    product = Product.objects.get(pk=pk)#get an object (a particular product) from the Product model based of its id specified in the url
    return render(request, 'core/product_desc.html', {'product':product}) #pass this product object to we created to a product variable 


def add_to_cart(request,pk):
    #get that particular porduct of id = pk
    product = Product.objects.get(pk=pk)
    
    #create order item
    order_item, created = OrderItem.objects.get_or_create( #if the product isnt added yet it will create the order item
    #but if order item is already created (added to cart) it will get the order item and increment the quantity
        product = product,
        user = request.user, #the current user who is making the request
        ordered = False,
    )
    
    #get query set of order object of particualr user
    #A QuerySet is a collection of data from a database. A QuerySet is built up as a list of objects.
#QuerySets makes it easier to get the data you actually need, by allowing you to filter and order the data.
    
    order_qs = Order.objects.filter(user = request.user, ordered = False) #all Order(class) objects with ordered=false will be assigned to order_qs
    if order_qs.exists(): 
        order = order_qs[0] #we will have our first order object
        if order.items.filter(product__pk = pk).exists(): #if an order contains that particular product with the same pk
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "Added Quantity Item")
            return redirect("product_desc", pk=pk) 
    
        else:
            order.items.add(order_item) #if there is no another item with the same product pk in our order then add that 
            messages.info(request, "Item added to Cart")#item to cart (rmbr item attri is manytomany with Order)
            return redirect("product_desc", pk=pk)
    else: #if order itself is not created
        ordered_date = timezone.now() #assign the current time zone to ordered_date variable
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to Cart")
        return redirect("product_desc", pk=pk) 
    
    
def orderlist(request):
    if Order.objects.filter(user = request.user, ordered = False).exists(): #if there is an item in the orderlist(cart)
        order = Order.objects.get(user = request.user, ordered = False)
        return render(request, 'core/orderlist.html', {'order':order})
    return render(request, 'core/orderlist.html', {'message': "Your Cart is Empty"})

def add_item(request, pk):
    #get that particular porduct of id = pk
    product = Product.objects.get(pk=pk)
    
    #create order item
    order_item, created = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False,
    )
    
    #get query set of order object of particualr user
    
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity +=1
                order_item.save()
                messages.info(request, "Added Quantity Item")
                return redirect("orderlist")
            else:
                messages.info(request, "Sorry! Product is out of Stock")
                return redirect("orderlist")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to Cart")
            return redirect("product_desc", pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to Cart")
        return redirect("product_desc", pk=pk) 
    
def remove_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False,
    )
    
    order = order_qs[0]
    if order.items.filter(product__pk = pk).exists():
            order_item = OrderItem.objects.filter(
                product=item,
                user=request.user,
                ordered=False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item Quantity Decremented")
            return redirect("orderlist")
    else:
            messages.info(request, "This item is not in your cart")
            return redirect("orderlist")
    
    
def checkout_page(request):
        msg=" Dear Customer, your order is successful. Thank you for choosing Ecom for your purshase. "
        send_msg_on_telegram(msg)
        messages.info(request, "Your order is successful")
        return render(request, 'core/checkout_address.html')

