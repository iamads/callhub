from django.shortcuts import render_to_response
from django.template import RequestContext
import shopify
from shopify_app.decorators import shop_login_required
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from piccolo.models import Buyers, Transactions, PreviousOrders
from django.db import connections

list_of_products = [{"title": 'Coat', "price": '245'}, {"title": 'Blazer', "price": '500'},
                    {"title": 'Shirt', "price": '150'},
                    {"title": 'Black Jeans', "price": '350'}, {"title": 'Blue Jeans', "price": '300'},
                    {"title": 'T-shirt', "price": '150'},
                    {"title": 'Brick', "price": '5'}, {"title": 'Coke', "price": '35'},
                    {"title": 'Cheese', "price": '10'}
                    ]


def welcome(request):
    return render_to_response('piccolo/welcome.html', {
        'callback_url': "http://%s/login/finalize" % (request.get_host()),
    }, context_instance=RequestContext(request))


def theyboughtthis(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        buyer_list = []
        for a in Transactions.objects.filter(product_id=product_id):
            buyer = a.buyer_id
            count = a.count
            name = Buyers.objects.get(buyer_id=buyer).first_name + " " + Buyers.objects.get(
                buyer_id=buyer).last_name
            phone = Buyers.objects.get(buyer_id=buyer).phone
            buyer_list.append({"name": name, "phone": phone, "count": count})
        print buyer_list
        if len(buyer_list) == 0:
            d = {}
        else:
            d = {"buyers": buyer_list}
        return render(request, "piccolo/theyboughtthis.html", d)


@shop_login_required
def index(request):
    products = shopify.Product.find()
    orders = shopify.Order.find(limit=3, order="created_at DESC")
    return render_to_response('piccolo/index.html', {
        'products': products,
        'orders': orders,
    }, context_instance=RequestContext(request))


@csrf_exempt
def payload(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data['customer']['first_name']
        last_name = data['customer']['last_name']
        customer_id = data['customer']['id']
        phone = data['customer']['default_address']['phone']
        order_id = data['id']
        print first_name, last_name, customer_id, phone, order_id
        product_ids = []
        for i in data['line_items']:
            product_ids.append(i['product_id'])
        # print product_ids
        if PreviousOrders.objects.filter(order_id=order_id).exists():
            pass
        else:
            new_order = PreviousOrders(order_id=order_id)
            new_order.save()
            if Buyers.objects.filter(buyer_id=customer_id).exists():
                pass
            else:
                new_customer = Buyers(first_name=first_name, last_name=last_name, phone=phone, buyer_id=customer_id)
                new_customer.save()
            for product_id in product_ids:
                if Transactions.objects.filter(buyer_id=customer_id, product_id=product_id).exists():
                    old_transaction = Transactions(buyer_id=customer_id, product_id=product_id)
                    old_transaction.count += 1
                    old_transaction.save()
                else:
                    new_transaction = Transactions(buyer_id=customer_id, product_id=product_id, count=1)
                    new_transaction.save()


def prerequisites(request):
    # On button click create webhook, load product data set, load transaction data set
    if request.POST.get('webhook'):
        hook = shopify.Webhook()
        hook.topic = 'orders/paid'
        hook.address = 'http://5a726739.ngrok.com/payload/'
        hook.format = 'json'
        # if hook.errors:
        # print "Something Broke"
        check = hook.save()
        print check
        return redirect(prerequisites)
        # Call webhook creator
    elif request.POST.get('load_products'):
        new_product = shopify.Product()
        for i in list_of_products:
            new_product.title = i["title"]
            new_product.price = i["price"]
            success = new_product.save()
            print success
        return redirect(prerequisites)
        # Call to load products
    return render(request, "piccolo/prerequisites.html", )


def about(request):
    return render(request, "piccolo/about.html", )
