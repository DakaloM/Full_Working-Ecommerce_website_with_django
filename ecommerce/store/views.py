import datetime
import json
from multiprocessing import context
from django.shortcuts import render
from pkg_resources import ContextualVersionConflict
from .models import *
from django.http import JsonResponse
from . utils import  cartData, cookieCart, guestOrder


# Create your views here.

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)    
        
    else:
        print("User is not logged in..")
        print("COOKIES: ", request.COOKIES)
        
        guestFuction =guestOrder(request, data)
        order = guestFuction['order']
        customer = guestFuction['customer']
            
            
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
        
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shippingInfo']['address'],
            city = data['shippingInfo']['city'],
            state = data['shippingInfo']['state'],
            zip_code = data['shippingInfo']['zipcode'],
        )
      
            
            
    return JsonResponse("Payment submitted...", safe=False)

def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product: ', product_id)
    
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    order_item , created = OrderItem.objects.get_or_create(order=order, product = product)
    
    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -=1
        
    order_item.save()
    
    if order_item.quantity <= 0:
        order_item.delete()
    
    return JsonResponse('Item was added', safe=False)

def store(request):
    
    cart_data = cartData(request)
    cart_items = cart_data['cart_items']
        
        
    product_list = Product.objects.all()
    context = {'product_list': product_list, 'cart_items': cart_items}
    return render(request, 'store/store.html', context)


def cart(request):
    
    cart_data = cartData(request)
    items = cart_data['items']
    order = cart_data['order']
    cart_items = cart_data['cart_items']
        
        
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/cart.html', context)


def checkout(request):
    cart_data = cartData(request)
    items = cart_data['items']
    order = cart_data['order']
    cart_items = cart_data['cart_items']
        
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/checkout.html', context)

