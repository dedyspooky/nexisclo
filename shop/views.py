from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
import requests
from django.views.decorators.csrf import csrf_exempt




# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)
    # n= len(products)
    # nColumns = n//5 + ceil((n/5)-(n//5))
    # params = {
    #     'no_of_columns': nColumns,
    #     'range': range(1,nColumns),
    #     'product': products
    #     }
    # allProducts = [[products, range(1, len(products)), nColumns],
    #                [products, range(1, len(products)), nColumns]]

    allProducts = []
    catProducts = Product.objects.values('subcategory','id')
    cats = {item['subcategory'] for item in catProducts}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat)
        n = len(prod)
        nColumns = n//5 + ceil((n/5)-(n//5))
        allProducts.append([prod,range(1,nColumns),nColumns])

    params = {'allProducts':allProducts}
    return render(request,'index.html',params)


def searchMatch(query,item):
    '''Return true only if query matches the item'''
    if query.lower() in item.desc.lower() or query.lower() in item.subcategory.lower() or query.lower() in item.category.lower() or query.lower() in item.product_adder.lower() or query.lower() in item.product_name.lower():
        return True    
    return False

def search(request):
    query = request.GET.get('search')
    allProducts = []
    catProducts = Product.objects.values('subcategory','id')
    cats = {item['subcategory'] for item in catProducts}
    for cat in cats:
        prodtemp = Product.objects.filter(subcategory=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nColumns = n//5 + ceil((n/5)-(n//5))
        if len(prod) != 0:
            allProducts.append([prod,range(1,nColumns),nColumns])
    params = {'allProducts':allProducts, 'search_query': query,'message': ""}
    if len(allProducts) == 0:
        params = {'message': query}
    return render(request,'search.html',params)


def base(request):
    return render(request,'base.html')

def men(request):
    allProducts = []
    prod = Product.objects.filter(subcategory="Men")
    n = len(prod)
    nColumns = n//5 + ceil((n/5)-(n//5))
    allProducts.append([prod,range(1,nColumns),nColumns])

    params = {'allProducts':allProducts}
    return render(request,'men.html',params)

def women(request):
    allProducts = []
    prod = Product.objects.filter(subcategory="Women")
    n = len(prod)
    nColumns = n//5 + ceil(n/5)-(n//5)
    allProducts.append([prod,range(1,nColumns),nColumns])
    params = {'allProducts': allProducts}
    return render(request,'women.html',params)

def unisex(request):
    allProducts =[]
    prod = Product.objects.filter(subcategory="Unisex")
    n = len(prod)
    nColumns = n//5 +ceil(n/5)-(n//5)
    allProducts.append([prod,range(1,nColumns),nColumns])
    params = {'allProducts':allProducts}
    return render(request,'unisex.html',params)


def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == "POST":
        # print(request)
        name =  request.POST.get('name','')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone','')
        message = request.POST.get('message','')
        # submitBtn = request.POST.get('submit','')
        contact = (Contact(
            name=name,
            email=email,
            phone=phone,
            message = message
                            ))
        thank = True
        contact.save()
        # print(name)
        # print(email)
        # print(phone)
        # print(message)
        # print(name)
        return render(request,'contact.html',{'thank':thank})
    return render(request,'contact.html')

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId','')
        email = request.POST.get('email','')
        # return HttpResponse(f"{orderId} and {email}")
        try:
            order = Order.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc,'time': item.timestamp})
                    response = json.dumps({'status':'success','updates': updates, 'itemsJson': order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "no item"}')
        except Exception as e:
            return HttpResponse('{"status": "error" }') 
    return render(request,'tracker.html')


def productView(request, productId):
    # Fetch the product using id
    product = Product.objects.filter(id=productId)
    print(product)
    return render(request,'productview.html',
                  {'product': product[0]}
                  )

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        amount = request.POST.get('amount','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        address1 = request.POST.get('address1','')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        order = (Order(
            items_json = items_json,
            amount = amount,
            name=name,
            email=email,
            phone=phone,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
                            ))
        order.save()
        update = OrderUpdate(name=order.name,phone=order.phone,email=order.email ,order_id=order.order_id, update_desc ="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        #Request Khalti to transfer the amount to your account
        
        # return render(request,'checkout.html',{'thank':thank, 'id':id})
    return render(request,'checkout.html')

def cart(request):
    return render(request,'cart.html')

def privacyandterms(request):
    return render(request,'privacyandterms.html')

@csrf_exempt
def verify_payment(request):
    #Khalti post request here
    data = request.POST
    product_id = data['product_identity']
    token = data['token']
    amount = data['amount']


    url = "https://khalti.com/api/v2/payment/verify/"

    payload = {
    'token': token,
    'amount': amount
    }

    headers = {
    'Authorization': 'Key test_secret_key_21706b92a8174f7d90d5d625afb540e3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_data = json.loads(response.text)
    status_code = str(response.status_code)

    if status_code == '400':
        response = JsonResponse({'status':'false',
                                 'message': response_data['detail']
                                 },status = 500)
        return response
    
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response_data)

    return JsonResponse(f"Payment Done !! With IDX. {response_data['user']['idx']}",safe=False)