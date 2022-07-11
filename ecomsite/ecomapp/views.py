
from email import message
from email.mime import image
from itertools import product
from multiprocessing import context
from unicodedata import category
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import random


from .models import Cart, Category, OrderItem, Product, CustomUserForm, Wishlist, Order, Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    category = Category.objects.filter()
    t_pro = Product.objects.filter(trending=1)
    context ={'t_pro': t_pro, 'category':category}
    return render(request, 'ecomapp/index.html', context)

def collections(request):
    category = Category.objects.filter(status = 0)
    data = {'category': category}
    return render(request, 'ecomapp/layouts/collections.html', data)


def collectionsview(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'products':products, 'category':category}
        return render(request, 'ecomapp/products/index.html', context)
    else:
        messages.warning(request, 'Invalid Category')
        return redirect('collections')


def productview(request, cate_slug, prod_slug):
    if(Category.objects.filter(slug=cate_slug, status=0)):
        if(Product.objects.filter(slug=prod_slug, status=0)):
            products = Product.objects.filter(slug=prod_slug, status=0).first
            data = {'products':products}
        else:
            messages.error(request, 'Invalid Product')
            return redirect('collections')
    
    else:
        messages.error(request, 'Invalid Category')
        return redirect('collections')
    
    return render(request, 'ecomapp/products/view.html', data)
        
        

def register(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration done successfully, Login to continue....")
            return redirect('/login')
    context = {'form':form}
    return render(request, "ecomapp/register.html", context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already logged in...")
        return redirect('/')
    else:
        if request.method == "POST":
            name = request.POST.get("username")
            password = request.POST.get("password")
            
            user = authenticate(request, username=name, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Login successfully!!")
                return redirect('/')
            else:
                messages.error(request, "Invalid username & Password")
                return redirect('/login')
        
    return render(request,"ecomapp/loginpage.html")

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successuflly...")
    return redirect('/')

def addtocart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)

            if(product_check):
                if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status': 'Product already in cart'})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status': 'Product Added successfully'})
                    else:
                        return JsonResponse({'status': "only " + str(product_check.quantity) + " quantity available"})
            else:
                return JsonResponse({'status': 'No such product found'})

        else:
            return JsonResponse({'status': 'Login to continue'})
    return redirect('/')

@login_required(login_url='loginpage')
def viewcart(request):
        cart = Cart.objects.filter(user=request.user)
        context ={'cart':cart}
        return render(request, 'ecomapp/products/cart.html', context)
    
def updatecart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(user=request.user, product_id=prod_id)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status': 'Updated successfully'})
    return redirect('/')

def deletecartitem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
        return JsonResponse({'status':'Deleted Successfully'})
    return redirect('/')


@login_required(login_url='loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user = request.user)
    context = {'wishlist': wishlist}
    return render(request, 'ecomapp/products/wishlist.html', context)


def addtowishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id = prod_id)):
                    return JsonResponse({'status': 'product already added in wishlist'})
                else:
                    Wishlist.objects.create(user=request.user, product_id = prod_id)
                    return JsonResponse({'status': 'Product added to wishlist successfully!!!'})
            else:
                return JsonResponse({'status': 'No such product is found'})
        else:
            return JsonResponse({'status': 'Login to continue'})

    return redirect('/')


def deletewishlistitem(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                wishlistitem = Wishlist.objects.get(product_id=prod_id, user=request.user)
                wishlistitem.delete()
                return JsonResponse({'status': 'Deleted Successfully'})
            else:
                return JsonResponse({'status': 'Product not found in wishlist'})
        else:
            return JsonResponse({'status':'Login to continue..'})
    return redirect('/')

@login_required(login_url='loginpage')
def checkoutview(request):
    originalcart = Cart.objects.filter(user = request.user)
    for item in originalcart:
        if item.product_qty >  item.product.quantity:
            Cart.objects.delete(id=item.id)
            
    cartitems = Cart.objects.filter(user = request.user)
    total_price = 0
    for item in cartitems:
        total_price += item.product.selling_price * item.product_qty
    userprofile = Profile.objects.filter(user = request.user).first() 
    context ={'cartitems':cartitems, 'total_price':total_price, 'userprofile':userprofile}
    return render(request, 'ecomapp/checkout.html', context)


@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == "POST":
        
        currentuser = User.objects.filter(id=request.user.id).first()
        
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()
            
        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()
            
            
        
        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')
        
        cart = Cart.objects.filter(user = request.user)
        cart_total_price =0
        for item in cart:
            cart_total_price+=item.product.selling_price * item.product_qty
            
        neworder.total_price = cart_total_price
        
        trackno = 'sham' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'sham' + str(random.randint(1111111,9999999))
            
        neworder.tracking_no =trackno
        neworder.save()
        
        neworderitems = Cart.objects.filter(user = request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                product = item.product,
                price = item.product.selling_price,
                quantity = item.product_qty
            )
            #to minus the product quantity from available stocks
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity-=item.product_qty
            orderproduct.save()
            
            Cart.objects.filter(user = request.user).delete()
            
            messages.success(request, "Order has been placed successfully")
            
            paymode = request.POST.get('payment_mode')
            if(paymode == 'Razorpay payment' or paymode == 'Paypal payment'):
                return JsonResponse({'status':'Order has been placed successfully'})
            else:
                messages.success(request, 'Order has been placed successully')
        
    return redirect('/')

@login_required(login_url='loginpage')
def razorpaycheck(request):
    cart = Cart.objects.filter(user = request.user)
    total_price =0
    for item in cart:
        total_price+=item.product.selling_price * item.product_qty
        
    return JsonResponse({
        'total_price': total_price
    })
    
def myorders(request):
    orders = Order.objects.filter(user = request.user)
    context ={'orders':orders}
    return render(request, 'ecomapp/orders.html', context)


def orderview(request, t_no):
    order = Order.objects.filter(tracking_no = t_no).filter(user = request.user).first()
    orderitems = OrderItem.objects.filter(order= order)
    context = {'order':order, 'orderitems':orderitems}
    return render(request,'ecomapp/orderview.html',context)


def productlist(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)
    productslist = list(products)
    
    return JsonResponse(productslist, safe=False)

def searchproduct(request):
    if request.method == "POST":
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=searchedterm).first()
            
            if product:
                return redirect('collections/'+ product.category.slug +'/'+ product.slug)
            else:
                messages.info(request,"No product matched")
                return redirect(request.META.get('HTTP_REFERER'))
        
    return redirect(request.META.get('HTTP_REFERER'))