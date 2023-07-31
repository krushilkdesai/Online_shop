from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from .models import Contact
from .models import Orders
from .models import OrderUpdate
from math import ceil
import json


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category = cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == 'POST':
        orderId = request.POST.get("orderId", '')
        email = request.POST.get("email", '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time':item.timestamp})
                    response = json.dumps([updates, order[0].item_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{else}')
        except Exception as e:
            return HttpResponse('{error}')
        
    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def productview(request, myid):
    product = Product.objects.filter(id = myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})


def checkout(request):
    if request.method == 'POST':
        item_json = request.POST.get('itemsJson', '')
        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address1", '') + " " + request.POST.get('address2', '')
        city = request.POST.get("city", '')
        state = request.POST.get("state", '')
        pin_code = request.POST.get("pin_code", '')
        phone = request.POST.get("phone")

        order = Orders(item_json=item_json, name=name, email=email, address=address, city=city, state=state, pin_code=pin_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank=True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'shop/checkout.html')
    