from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from core.forms import UserRegisterForm, ProductForm,UpdateStock
from core.models import User,Product, Map,ProductList,ProductListItem,CATEGORY_TYPE
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
import cv2
from pyzbar.pyzbar import decode
import cv2
import numpy as np
from django.shortcuts import get_object_or_404
import json
from django.db.models import Subquery
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from django.utils import timezone


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("sign-in")
   
    form = UserRegisterForm()
    if 'q' in request.GET:
        q = request.GET['q']
        product = Product.objects.filter(Q(product_id__icontains=q) | Q(product_name__icontains=q)).order_by('-stock')
        if not product:  # Check if products queryset is empty
            message1 = "Item not found"
        else:
            message1=""

    else:
        product = Product.objects.all().order_by('-stock')

        message1=""

    if 'a' in request.GET:
        a = request.GET['a']
        user = User.objects.filter(Q(email__icontains=a) | Q(username__icontains=a))
        if not user:  # Check if products queryset is empty
            message = "User not found"
        else:
            message=""

    else:
        user = User.objects.all()
        message=""

    # productList = ProductList.objects.filter(user=request.user).order_by('-time')[:3]
    zero_stock_product_ids = Product.objects.filter(stock=0).values('product_id')
    # print(zero_stock_product_ids)
    # Filter out ProductList items where the associated product has stock equals 0
    product_list_with_zero_stock = ProductList.objects.filter(
        user=request.user,
        productlistitem__product_id__in=zero_stock_product_ids
    ).distinct()
    print(product_list_with_zero_stock)
    # # Get the product lists for the user, excluding those with zero stock products
    productList = ProductList.objects.filter(user=request.user).exclude(id__in=Subquery(product_list_with_zero_stock.values('id'))).order_by('-time')[:3]

    # print(productList.productlistitem__stock)
    
    context = {
        'form' : form,
        'user':user,
        'product':product,
        'productList':productList,
        'message':message,
        'message1':message1,
    }
    return render(request, 'index.html',context)

def add_user(request):
    if not request.user.is_authenticated:
        return redirect("sign-in")
    else:
        if request.user.account_type != "admin":
            return redirect("index")
        else:
            if request.method == "POST":
                form = UserRegisterForm(request.POST or None)
                if form.is_valid():
                    # Create new product
                    new_user = form.save()
                    new_user.account_type = form.cleaned_data.get('account_type')
                    new_user.save()
                    return redirect("index")
            else:
                form = UserRegisterForm()
            context = {
                'form' : form,
            }
            return render(request, "add-user.html", context)




def signIn(request):
    if request.user.is_authenticated:
        return redirect("index")
    message = False
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email)
        print(password)
        try:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                message = True
        except:
            message = True
            print(message)

            return render(request, "signIn.html",{"message":message})

    return render(request, "signIn.html",{"message":message})

def add_item(request):
    message = False
    if not request.user.is_authenticated:
        return redirect("sign-in")
    else:
        if request.user.account_type != "stockpurchaser":
            return redirect("index")
        else:
            if request.method == "POST":
                form = ProductForm(request.POST or None)
                if form.is_valid():
                    # Create new product
                    new_product = form.save()
                    return redirect("index")
                else:
                    message = True
            else:
                form = ProductForm()
            context = {
                'form' : form,
                'message':message
            }
            return render(request, "add-item.html", context)

def log_out(request):
    logout(request)
    return redirect("sign-in")

def update_stock(request):
    updateproduct = request.GET.getlist("product[]")
    stock = request.GET.getlist("stock[]")
    # products = Product.objects.all()
    if len(updateproduct) > 0:
        for i in range(len(updateproduct)):
            product_id = updateproduct[i]
            stock_value = stock[i]

            # Retrieve the product by ID
            product = Product.objects.get(product_id=product_id)
            productlistitems = ProductListItem.objects.filter(product_id=product_id)


            # Update the stock value
            if stock_value != '':
                stock_value = int(stock_value)
                product.stock = product.stock+stock_value
                product.save()
                for item in productlistitems:
                    item.stock = item.stock+ stock_value
                    item.save()
                print(product)

    data = render_to_string("async/update-stock.html",{"products":product})
    return JsonResponse({"data": data})

def update_product_detail(request, pk):
    queryset = Product.objects.get(product_id=pk)        
    context= {
        'category_choices': CATEGORY_TYPE , # Pass CATEGORY_TYPE to the template context
        'product':queryset
    }
    return render(request, 'updatedetail.html',context)

def update_detail_done(request):
    id = request.GET['product_id']
    id_main = request.GET['product-id-main']
    name = request.GET['product_name']
    stock = request.GET['update_stock']
    product_category1 = request.GET['product_category']

    product = Product.objects.get(product_id=id_main)
    productlistitems = ProductListItem.objects.filter(product_id=id_main)
    productlist = ProductList.objects.filter(product__contains=product.product_name)

    product.product_id = id
    product.product_name = name
    product.stock = stock
    product.product_category =product_category1
    product.save()

    for item1 in productlist:
        # Split the product field by comma and whitespace
        products = item1.product.split(', ')
        print(products)
        # Replace the matching part with the new name
        updated_products = []
        for product in products:
            for item in productlistitems:
                print(item.product_name)
                if product == item.product_name:  # Corrected comparison operator
                    updated_products.append(name)  # Append new name if product matches
                    break  # Break out of the inner loop if match found
            else:
                updated_products.append(product)  # Append original product if no match found
                
        # Join the updated products back into a single string
        updated_product = ', '.join(updated_products)
        print(updated_product)
        # Update the product field and save the item
        item1.product = updated_product
        print(item1.product)
        item1.save()


    for item2 in productlistitems:
        item2.product_id = id
        item2.product_name = name
        item2.stock = stock
        item2.product_category = product_category1
        item2.save()

    return JsonResponse({})


def delete_product(request,pk):
    product = Product.objects.get(product_id=pk)
    productlistitems = ProductListItem.objects.filter(product_id=pk)
    productlist = ProductList.objects.filter(product__contains=product.product_name)

    if request.method=="POST":
        product.delete()
        productlistitems.delete()
        productlist.delete()
        return redirect("index")

    context={
        "product":product,
    }
    
    return render(request, "delete-product.html", context)

def delete_user(request,pk):
    user = User.objects.get(email=pk)
    if request.method=="POST":
        user.delete()
        return redirect("index")

    context={
        "user":user,
    }
    
    return render(request, "delete-user.html", context)

def scan_pick(request):
    return render(request, 'scan-pick.html')

def render_scan_page(frame):
    try:
        # Perform barcode decoding or any other processing with the frame_pil
        decoded_barcodes = decode(frame)
        for barcode in decoded_barcodes:
            barcode_data = barcode.data.decode('utf-8')

            if barcode_data.startswith('http'):
                return barcode_data
                
    except Exception as e:
        print("Error decoding QR code:", e)

    return

def update_stock_picker(request, pk):
    product = get_object_or_404(Product, product_id=pk)
    context= {
        'product':product,
    }
    return render(request, "update_stock_picker.html", context)

class ClassConsumer(AsyncWebsocketConsumer): 
    async def connect(self):
        self.i = 0
        self.loop = asyncio.get_running_loop()
        await self.accept()

    async def disconnect(self, close_code):
        self.i = 0
        self.stop = True
        raise StopConsumer()

    async def receive(self, bytes_data):        
        if not bytes_data:
            self.i = 0
            print('Closed connection')
            await self.close()
        else:
            # Decode the image bytes
            self.frame = await self.loop.run_in_executor(None, cv2.imdecode, np.frombuffer(bytes_data, dtype=np.uint8), cv2.IMREAD_COLOR)            
            url = render_scan_page(self.frame)

            if url and url.startswith('http'):
                # Redirect the user to the scanned URL
                await self.send(url)

def add_to_pick(request):
    cart_product = {}
    cart_product[str(request.GET['id'])]={
        'name': request.GET['name'],
        'id': str(request.GET['id']),
        'stock': request.GET['stock'],
        'category': request.GET['category'],
        'location': request.GET['location'],
        'image': request.GET['image'],
    }
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            request.session['cart_data_obj'] = cart_data
            # print(cart_data)

        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
            # print(cart_data)
            
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})

def depart(request):
    cart_product={
        'depart': str(request.GET['depart']),
    }

    if 'cart_data_ob' in request.session:
        if str(request.GET['depart']) in request.session['cart_data_ob']:
            cart_data = request.session['cart_data_ob']
            request.session['cart_data_ob'] = cart_data
        else:
            cart_data = request.session['cart_data_ob']
            cart_data.update(cart_product)
            request.session['cart_data_ob'] = cart_data

    else:
        request.session['cart_data_ob'] = cart_product
    return JsonResponse({"data": request.session['cart_data_ob']})


def cart_view(request):
    if 'cart_data_obj' in request.session:
        if not request.session['cart_data_obj']:
            # messages.warning(request, "Please select at least one item")
            return redirect("index")
            
        return render(request, "selected-item.html", {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})
    else:
        # messages.warning(request, "Please select at least one item")
        return redirect("index")
    

def delete_item_from_cart(request):
    product_id = str(request.GET.get('id', None))
    if product_id and 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
            return JsonResponse({ "totalcartitems": len(request.session['cart_data_obj'])})
    
    return redirect("index")

def navigation_view(request):
    depart_value=None
    if 'cart_data_ob' in request.session and request.session['cart_data_obj']:
        depart_value = request.session['cart_data_ob'].get('depart')
        # print(depart_value)
    # Retrieve the destination from the cart data if available
    desti = None
    if 'cart_data_obj' in request.session and request.session['cart_data_obj']:
        first_item = next(iter(request.session['cart_data_obj'].values()))
        # print(first_item)
        desti = first_item['category']
        # print(desti)
        # Query the Map model for the specific map
    try:
        map_instance = Map.objects.get(depart=depart_value, destination=desti)
    except Map.DoesNotExist:
        map_instance = None 

    try:
        picking_item = next(iter(request.session['cart_data_obj'].values()))
        picking_item_name = picking_item['name']
        product = Product.objects.get(product_name=picking_item_name)
    except Product.DoesNotExist:
        product = None 

    if 'cart_data_obj' in request.session:
        if not request.session['cart_data_obj']:
            return redirect("index")
            
        return render(request, "navigation.html", {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']),'map_instance': map_instance, 'product':product})
    else:
        return redirect("index")
    
def start_location(request):

    return render(request, 'start-location.html')

def clear_session(request):
    del request.session['cart_data_obj']  # Delete the entire cart_data_obj
    del request.session['cart_data_ob']  # Delete the entire cart_data_obj

    return JsonResponse({"message": "Cart data deleted successfully"})

def navigation_pick(request, pk):
    product = get_object_or_404(Product, product_id=pk)
    context= {
        'product':product,
    }
    return render(request, "navigation-pick.html", context)

def product_list(request):
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        product_names = ", ".join([item['name'] for item in cart_data.values()])
        # Check if a ProductList with the same product names exists
        existing_product_list = ProductList.objects.filter(user=request.user, product=product_names).first()
        print(existing_product_list)
        if not existing_product_list:
            # If a ProductList with the same product names doesn't exist, create a new one
            productList = ProductList.objects.create(
                user=request.user,
                product=product_names,
            )

            # Create ProductListItem objects for each item in the cart data
            for p_id, item in cart_data.items():
                cart_order_product = ProductListItem.objects.create(
                    order=productList,
                    product_id=item['id'],
                    product_name=item['name'],
                    stock=item['stock'],
                    product_category=item['category'],
                    location = item['location'],
                    image = item['image']
                )
        else:
            # If a ProductList with the same product names already exists, use the existing one
            existing_product_list.time = timezone.now()
            existing_product_list.save()
            productList = existing_product_list

        return JsonResponse({ "totalcartitems": len(request.session['cart_data_obj'])})



def add_to_pick_list(request):
    items_array_string = request.GET.get('itemsArray')
    items_array = json.loads(items_array_string)
    cart_product = {}

    for item in items_array:
        cart_product[item['id']] = {
            'name': item['name'],
            'id': item['id'],
            'stock': item['stock'],
            'category':item['category'],
            'location':item['location'],
            'image':item['image']
        }
    if 'cart_data_obj' in request.session:
        del request.session['cart_data_obj']  # Delete the entire cart_data_obj
        request.session['cart_data_obj'] = cart_product

    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})

def item_pick(request):
    pickingqty = int(request.GET['pickingqty'])
    pickproduct = request.GET['pickproduct']

    product = Product.objects.get(product_name=pickproduct)
    productlistitems = ProductListItem.objects.filter(product_name=pickproduct)
    if pickingqty <= product.stock:
        product.stock -= pickingqty
        product.save()  
        for item in productlistitems:
            item.stock -= pickingqty
            item.save()

        message=False
        return JsonResponse({"message": message})
    else:
        message=True
        # Re-render the form with the same context
        return JsonResponse({"message": message})

def item_pick_scan(request):
    pickingqty = int(request.GET['pickingqty'])
    pickproduct = request.GET['pickproduct']

    product = Product.objects.get(product_name=pickproduct)
    productlistitems = ProductListItem.objects.filter(product_name=pickproduct)
    if pickingqty <= product.stock:
        product.stock -= pickingqty
        product.save()  
        for item in productlistitems:
            item.stock -= pickingqty
            item.save()

        message=False
        return JsonResponse({"message": message})
    else:
        message=True
        # Re-render the form with the same context
        return JsonResponse({"message": message})
  


