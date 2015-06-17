from django.shortcuts import render_to_response
from django.template import RequestContext
import shopify
from shopify_app.decorators import shop_login_required
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
import json

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


@shop_login_required
def index(request):
    products = shopify.Product.find(limit=3)
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
        print product_ids


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
