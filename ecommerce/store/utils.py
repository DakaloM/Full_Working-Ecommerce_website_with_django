import json
from . models import *

def cookieCart(request):
    
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        
    print("Cart: ", cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']
    
    for i in cart:
        #prevent getting errors if itens in cart are removed from the database
        try:
            
            cart_items += cart[i]["quantity"]
            
            product = Product.objects.get(id = i)
            product_total = (product.price * cart[i]['quantity'])
            print("Total: ", product_total)
            
            order['get_cart_total'] += product_total
            order['get_cart_items'] += cart[i]["quantity"]
            
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url
                    
                    },
                'quantity': cart[i]['quantity'],
                'get_total': product_total
            }
            
            print('Image: ', item['product']['image_url'])
            print("Digital: ", product.digital)
            
            items.append(item)
            
            if product.digital == False:
                order['shipping']= True
                
                
        except:
            pass
            
    print("Order Total: ", order['get_cart_total'])    
    print("Items Total: ", order['get_cart_items']) 
        
    return {'cart_items': cart_items, 'order': order, 'items': items}

def cartData(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        
    else:
        cookieData = cookieCart(request)
        cart_items = cookieData['cart_items']
        order = cookieData['order']
        items = cookieData['items']
        
    return {'items': items, 'order': order, 'cart_items': cart_items}

def guestOrder(request, data):
    
    name = data['form']['name']
    email = data['form']['email']
    
    cookieData = cookieCart(request)
    items = cookieData['items']
    
    customer, create = Customer.objects.get_or_create(email=email, ) 
    customer.name = name
    customer.save()
    
    order = Order.objects.create(customer=customer, complete= False)
    
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        
        order_item = OrderItem.objects.create(product=product,order=order,
                                                quantity=item['quantity'])
    
    
    return {'order': order, 'customer': customer} 