import abc
from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from matplotlib.style import context
from numpy import product
from .models import Customer, Product, Cart, OrderPlaced

from django.contrib.auth.decorators import login_required

# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self, request):       
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        books = Product.objects.filter(category='B')
        
        total_items = 0
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))

        context = {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'laptops': laptops, 'books': books,'total_items': total_items}
        return render(request, 'app/home.html', context)



# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        
        item_already_in_cart = False
        total_items = 0
        
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

        context = {'product': product, 'total_items': total_items, 'item_already_in_cart': item_already_in_cart}
        return render(request, 'app/productdetail.html', context)




from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def add_to_cart(request):            
    user = request.user
    product_id = request.GET.get('prod_id')
    # print(product_id)
    
    product = Product.objects.get(id=product_id)
    
    Cart(user=user, product=product).save()
    #return render(request, 'app/addtocart.html')
    return redirect('/cart')


# from django.contrib.auth.decorators import login_required
@login_required
def show_cart(request):
    total_items = 0
    ### pass
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
        
        user = request.user
        carts = Cart.objects.filter(user=user)
        # print('----------------------------')
        # print(carts)
        # print('----------------------------')
        
        amount = 0.0
        shipping_amount = 100.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print('----------------------------')
        # print(cart_product)
        # print('----------------------------')
        
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                # print('temp_amount', temp_amount)
                
                amount = amount + temp_amount
                # print('amount', amount)
                
                total_amount = amount + shipping_amount
                # print('total_amount', total_amount)
                
        
            context = {'carts': carts, 'amount': amount, 'total_amount': total_amount, 'shipping_amount': shipping_amount, 'total_items': total_items}
            return render(request, 'app/addtocart.html', context)
        
        else:
            return render(request, 'app/emptycart.html')


from django.db.models import Q
from django.http import JsonResponse
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        
        amount = 0.0
        shipping_amount = 100.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        

        for p in cart_product:
            
            temp_amount = (p.quantity * p.product.discounted_price)
                # print('temp_amount', temp_amount)
                
            amount = amount + temp_amount
                # print('amount', amount)
                
            # total_amount = amount + shipping_amount
                # print('total_amount', total_amount)
                
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)
        
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        
        amount = 0.0
        shipping_amount = 100.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
                # print('temp_amount', temp_amount)
                
            amount = amount + temp_amount
                # print('amount', amount)
                
            # total_amount = amount + shipping_amount
                # print('total_amount', total_amount)
                
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)
    

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        
        amount = 0.0
        shipping_amount = 100.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
                # print('temp_amount', temp_amount)
                
            amount = amount + temp_amount
                # print('amount', amount)
                
            # total_amount = amount + shipping_amount
                # print('total_amount', total_amount)
                
        data = {
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)
            


# #####def change_password(request):
# ##### return render(request, 'app/changepassword.html')



# def bottomwear(request):
#     return render(request, 'app/bottomwear.html')
def bottomwear(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'Lee' or data == 'Pantaloons':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=550)
    elif data == 'above':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=550)

    context = {'bottomwears': bottomwears}
    return render(request, 'app/bottomwear.html', context)


# def topwear(request):
#     return render(request, 'app/topwear.html')
def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Park' or data == 'Polo':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=450)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=450)
    

    context = {'topwears': topwears}
    return render(request, 'app/topwear.html', context)



# def mobile(request):
#     return render(request, 'app/mobile.html')
def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=15000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=15000)

    context = {'mobiles': mobiles}
    return render(request, 'app/mobile.html', context)


# def laptop(request):
#     return render(request, 'app/laptop.html')
def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Dell' or data == 'HP' or data == 'Apple' or data == 'Lenovo':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=48000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=48000)

    context = {'laptops': laptops}
    return render(request, 'app/laptop.html', context)


# def book(request):
#     return render(request, 'app/book.html')
def book(request, data=None):
    if data == None:
        books = Product.objects.filter(category='B')  
        # print(books)        
    elif data == 'Indian' or data == 'Foreign':
        books = Product.objects.filter(category='B').filter(brand=data)
    elif data == 'below':
        books = Product.objects.filter(category='B').filter(discounted_price__lt=1300)
    elif data == 'above':
        books = Product.objects.filter(category='B').filter(discounted_price__gt=1300)
    
    context = {'books': books}
    return render(request, 'app/book.html', context)
    



# def login(request):
#  return render(request, 'app/login.html')


from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()

        context = {'form': form}
        return render(request, 'app/customerregistration.html', context)
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()
            
        context = {'form': form}
        return render(request, 'app/customerregistration.html', context)


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# def profile(request):
#  return render(request, 'app/profile.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        #### pass
        form = CustomerProfileForm()
        
        context = {'form': form, 'active': 'btn-primary'}
        return render(request, 'app/profile.html', context)
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            
            messages.success(request, 'Congratulations !! Profile Updated Successfully')
            
        context = {'form': form, 'active': 'btn-primary'}
        return render(request, 'app/profile.html', context)



# def address(request):
#  return render(request, 'app/address.html')
@login_required
def address(request):
    address = Customer.objects.filter(user=request.user)
    
    context = {'address': address, 'active': 'btn-primary'}
    return render(request, 'app/address.html', context)




# def checkout(request):
#  return render(request, 'app/checkout.html')

@login_required
def checkout(request):
    user = request.user
    address = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 100.0
    total_amount = 0.0
    
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
            total_amount = amount + shipping_amount
            
        
    context = {'user': user, 'address': address, 'cart_items': cart_items, 'amount': amount, 'total_amount': total_amount}
    return render(request, 'app/checkout.html', context)

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
        
    return redirect('orders')





def buy_now(request):
 return render(request, 'app/buynow.html')



# def orders(request):
#  return render(request, 'app/orders.html')

@login_required
def orders(request):
    user = request.user
    order_placed = OrderPlaced.objects.filter(user=user)
    
    context = {'order_placed': order_placed}    
    return render(request, 'app/orders.html', context)




