from django.contrib import messages
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

# Create your views here.
def index (request):
    if request.user.is_authenticated:
        customer=request.user
        '''
        Creating a cart for a logged in user. check if cart exists, create 
        '''
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        '''
        Getting the cartitems(child) from the cart(parent)
        '''
        cartitems=cart.cartitems_set.all()
    else:
        cart=[]
        cartitems=[]
        cart={'cartquantity':0}
    products=Product.objects.all()
    ctx={
        'products':products, 
        'cartitems':cartitems,
        'cart': cart,
    }
    return render (request, 'index.html', ctx)

def cart(request):
    '''
    check if user is authenticated, so they can create a new cart
    '''
    if request.user.is_authenticated:
        customer=request.user
        '''
        Creating a cart for a logged in user. check if cart exists, create 
        '''
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        '''
        Getting the cartitems(child) from the cart(parent)
        '''
        cartitems=cart.cartitems_set.all()
    else:
        cart=[]
        cartitems=[]
        cart={'cartquantity':0}
    ctx={
        'cart':cart,
        'cartitems':cartitems
    }
    return render(request, 'cart.html', ctx)

def updateCart(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    if request.user.is_authenticated:
        customer =request.user
        product = Product.objects.get(product_id=product_id)
        cart, created =Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems, created =Cartitems.objects.get_or_create(product=product, cart=cart)

        if action == 'add':
            cartitems.quantity += 1
            cartitems.save()

        msg={
            'quantity':cart.cartquantity,
            'created':created
        }

    return JsonResponse(msg, safe=False)

def updateQuantity(request):
    data=json.loads(request.body)
    inputval= int(data['in_val'])
    product_id=data['p_id']
    if request.user.is_authenticated:
        customer =request.user
        product = Product.objects.get(product_id=product_id)
        cart, created =Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems, created =Cartitems.objects.get_or_create(product=product, cart=cart)

        cartitems.quantity=inputval
        cartitems.save()

        msg={
            'subtotal':cartitems.subtotal,
            'grandtotal':cart.grandtotal,
            'quantity':cart.cartquantity,
            'created':created
        }

    return JsonResponse(msg, safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(owner=customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'cartquantity': 0}
    context = {'cart': cart, 'cartitems': cartitems}
    return render(request, 'checkout.html', context)




def contact(request):
    return render(request, 'contact.html')

       
def register(request):
    if request.method== "POST":
        username=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        if password1 != password2:
            messages.error(request,"Your Passwords do not Match!! Please Try Again")
            return redirect('/register/')
        new_user=User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )
        new_user.save()
        return render (request,'userlogin.html')
    return render(request,'register.html')


def signin(request):
    if request.method== "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have successfuly logged in")
            return redirect ("/")
    return render(request,'userlogin.html')

def searchbar(request):
    if 'query' in request.GET and request.GET["query"]:
        search_term = request.GET.get("query")
        searched_product=Product.searchbar(search_term)
        message=f"{search_term}"

        ctx={
            'searched_products': searched_product,
            'message': message
        }   
        return render(request, 'searchresults.html', ctx)
    else:
        message = "You haven't searched for any products yet"
        return render(request, 'searchresults.html',{"message": message})

def signout(request):
    logout(request)
    messages.success(request,"You have logged out, we will be glad to have you back again")
    return redirect ("index")