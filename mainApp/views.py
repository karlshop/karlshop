from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from random import randint

from django.conf import settings
from django.core.mail import send_mail

from .models import *

def home(request):
    if(request.method=='POST'):
        email = request.POST.get('email')
        try:
            Newsletter.objects.get(email=email)
            return HttpResponseRedirect('/')
        except:
            n = Newsletter()
            n.email=email
            n.save()
            return HttpResponseRedirect('/')
    #request.session.flush()
    products = Product.objects.all()
    if(len(products)==0):
        products=[]
        product1 = 0
        product2 = 0
        product3 = 0
    else:
        products = products[::-1]
        product1 = products[0]
        product2 = products[1]
        product3 = products[2]
    return render(request,'index.html',{"Products":products,
                                        "Product1":product1,
                                        "Product2":product2,
                                        "Product3":product3,})

def shop(request,m,s,b):
    maincat = MainCategory.objects.all()
    subcat = SubCategory.objects.all()
    brand = Brand.objects.all()
    if(m=="default" and b=="default"):
        products = Product.objects.all()
        products = products[::-1]
    elif(m!="default" and b=="default"):
        mc = MainCategory.objects.get(name=m)
        sc = SubCategory.objects.get(name=s)
        products = Product.objects.filter(maincat=mc,subcat=sc)
        products = products[::-1]
    elif (m=="default" and b != "default"):
        br = Brand.objects.get(name=b)
        products = Product.objects.filter(brand=br)
        products = products[::-1]
    else:
        mc = MainCategory.objects.get(name=m)
        sc = SubCategory.objects.get(name=s)
        br = Brand.objects.get(name=b)
        products = Product.objects.filter(maincat=mc, subcat=sc,brand=br)
        products = products[::-1]
    return render(request,'shop.html',{"Products":products,
                                              "mainCat": maincat,
                                              "subCat": subcat,
                                              "brand": brand,
                                              "m":m,
                                              "b":b,
                                              "s":s})

@login_required(login_url='/login/')
def checkout(request):
    user = User.objects.get(username=request.user)
    if(user is not None and user.is_superuser):
        return HttpResponseRedirect('/admin/')
    else:
        try:
            Seller.objects.get(username=request.user)
            return HttpResponseRedirect('/sellerprofile/')
        except:
            buyer = Buyer.objects.get(username=request.user)
            try:
                c = Checkout.objects.get(buyer=buyer)
            except:
                c = Checkout()
                c.buyer=buyer
                c.q=""
                c.save()
            cart = request.session.get('cart', None)
            product = []
            total = 0
            if (cart):
                for i, q in cart.items():
                    p = Product.objects.get(pid=i)
                    product.append(p)
                    total = total + p.finalPrice * q
            if (total < 1000):
                shipping = 150
            else:
                shipping = 0
            finalAmount = total + shipping
            if(request.method=='POST'):
                c = Checkout.objects.get(buyer=buyer)
                c.buyer= buyer
                mode=c.mode = request.POST.get('mode')
                if(len(product)==0):
                    messages.error(request,"Please Buy Atleast one Item")
                    return render(request,'checkout.html')
                for i in product:
                    c.products.add(i.pid)
                for i in cart.keys():
                    c.q=c.q+str(i)+":"+str(cart[i])+","
                c.total=total
                c.shipping=shipping
                c.final=finalAmount
                c.save()
                del request.session['cart']
                if(mode=='paypal'):
                    return HttpResponseRedirect('/process-payment/'+str(c.cid)+"/")
                else:
                    return HttpResponseRedirect('/buyerprofile/')
            return render(request,'checkout.html',{"Buyer":buyer,
                                                   "Total":total,
                                                   "Shipping":shipping,
                                                   "Final":finalAmount,
                                                   "Products":product})

def cart(request):
    cart = request.session.get('cart',None)
    product=[]
    total=0
    if(cart):
        for i,q in cart.items():
            p = Product.objects.get(pid=i)
            product.append(p)
            total = total + p.finalPrice*q
    if(total<1000):
        shipping=150
    else:
        shipping=0
    finalAmount = total + shipping
    if(request.method=='POST'):
        pid = request.POST.get('pid')
        enteredQ = int(request.POST.get('quantity'))
        cart = request.session.get('cart')
        q = cart[pid]
        q=q+enteredQ-q
        cart[pid]=q
        request.session['cart']=cart
        return HttpResponseRedirect('/cart/')
    return render(request,'cart.html',{"Product":product,
                                       "Total":total,
                                       "Shipping":shipping,
                                       "Final":finalAmount})

def productDetails(request,num):
    product = Product.objects.get(pid=num)
    if(request.method=='POST'):
        q = int(request.POST.get('quantity'))
        cart = request.session.get('cart',None)
        if(cart):
            num=str(num)
            if(num in cart.keys()):
                a = cart.get(num)
                a = a+q
                cart[num]=a
            else:
                cart.setdefault(num,q)
        else:
            cart={}
            cart.setdefault(num,q)
        request.session['cart']=cart
        return HttpResponseRedirect('/cart/')
    return render(request,'product-details.html',{"Product":product})

def loginUser(request):
    if(request.method=="POST"):
        uname=request.POST.get('uname')
        password=request.POST.get('password')
        user=authenticate(username=uname,password=password)
        if(user is not None):
            login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect('/admin/')
            else:
                try:
                    Seller.objects.get(username=request.user)
                    return HttpResponseRedirect('/sellerprofile/')
                except:
                    return HttpResponseRedirect('/buyerprofile/')
        else:
            messages.error(request,'Invalid User Name or Password')
    return render(request,'login.html')


def signupUser(request):
    if(request.POST.get('type')=='seller'):
        seller = Seller()
        seller.name = request.POST.get('name')
        seller.email = request.POST.get('email')
        seller.username = request.POST.get('username')
        pward = request.POST.get('pword')
        try:
            user=User.objects.create_user(username=seller.username,
                                          password=pward,
                                          first_name=seller.name,
                                          email=seller.email)
            user.save()
        except:
            messages.error(request,'User Name Already Exist')
            return render(request,'login.html')

        seller.phone = request.POST.get('phone')
        seller.addressline1 = request.POST.get('addressline1')
        seller.addressline2 = request.POST.get('addressline2')
        seller.addressline3 = request.POST.get('addressline3')
        seller.postcode = request.POST.get('postcode')
        seller.city = request.POST.get('city')
        seller.state = request.POST.get('state')
        seller.pic = request.FILES.get('pic')
        seller.save()
        messages.success(request,'User Account Successfully Created!! Now login !!!')
        return render(request,'login.html')
    else:
        buyer = Buyer()
        buyer.name = request.POST.get('name')
        buyer.email = request.POST.get('email')
        buyer.username = request.POST.get('username')
        pward = request.POST.get('pword')
        try:
            user = User.objects.create_user(username=buyer.username,
                                            password=pward,
                                            first_name=buyer.name,
                                            email=buyer.email)
            user.save()
        except:
            messages.error(request, 'User Name Already Exist')
            return render(request, 'login.html')

        buyer.phone = request.POST.get('phone')
        buyer.addressline1 = request.POST.get('addressline1')
        buyer.addressline2 = request.POST.get('addressline2')
        buyer.addressline3 = request.POST.get('addressline3')
        buyer.postcode = request.POST.get('postcode')
        buyer.city = request.POST.get('city')
        buyer.state = request.POST.get('state')
        buyer.pic = request.FILES.get('pic')
        buyer.save()
        messages.success(request, 'User Account Successfully Created!! Now login !!!')
        return render(request, 'login.html')

@login_required(login_url='/login/')
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required(login_url='/login/')
def sellerProfile(request):
    user=Seller.objects.get(username=request.user)
    products=Product.objects.filter(seller=user)
    if(request.method=='POST'):
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.addressline1 = request.POST.get('addressline1')
        user.addressline2 = request.POST.get('addressline2')
        user.addressline3 = request.POST.get('addressline3')
        user.postcode = request.POST.get('postcode')
        user.city = request.POST.get('city')
        user.state = request.POST.get('state')
        if(request.FILES.get('pic') is not None):
            user.pic = request.FILES.get('pic')
        user.save()
        return HttpResponseRedirect('/sellerprofile/')
    return render(request,'sellerprofile.html',{"User":user,
                                                "Products":products})

def addProduct(request):
    if(request.method=='POST'):
        p=Product()
        p.name=request.POST.get('name')
        p.description=request.POST.get('description')
        p.brand = Brand.objects.get(bid=request.POST.get('brand'))
        p.subcat = SubCategory.objects.get(scid=request.POST.get('subCat'))
        p.maincat = MainCategory.objects.get(mcid=request.POST.get('mainCat'))
        p.price=int(request.POST.get('price'))
        p.discount=int(request.POST.get('discount'))
        p.finalPrice=p.price-p.price*p.discount//100
        p.instock=request.POST.get('stock')
        p.size=request.POST.get('size')
        p.color=request.POST.get('color')
        p.img1=request.FILES.get('img1')
        p.img2=request.FILES.get('img2')
        p.img3=request.FILES.get('img3')
        p.img4=request.FILES.get('img4')
        p.seller = Seller.objects.get(username=request.user)
        p.save()
        subject = "Check out New Products on Karl Shop"
        mailmessage = "Welcome to Karlshop Please Check Our New Products with High Discount\n Visit http://localhost:8000/productdetails/"+str(p.pid)+"/"
        email_from = settings.EMAIL_HOST_USER
        emails = Newsletter.objects.all()
        recipient_list = []
        for i in emails:
            recipient_list.append(i)
        send_mail(subject, mailmessage, email_from, recipient_list)
        # send_mass_mail(subject, mailmessage, email_from, recipient_list)
        return HttpResponseRedirect('/sellerprofile/')
    maincat = MainCategory.objects.all()
    subcat = SubCategory.objects.all()
    brand = Brand.objects.all()
    return render(request,'addproduct.html',{
                                "mainCat":maincat,
                                "subCat":subcat,
                                "brand":brand})

@login_required(login_url='/login/')
def deleteProduct(request,num):
    product=Product.objects.get(pid=num)
    user = Seller.objects.get(username=request.user)
    if(product.seller==user):
        product.delete()
    return HttpResponseRedirect('/sellerprofile/')

@login_required(login_url='/login/')
def editProduct(request,num):
    p=Product.objects.get(pid=num)
    user = Seller.objects.get(username=request.user)
    if(p.seller==user and request.method=='POST'):
        p.name = request.POST.get('name')
        p.description = request.POST.get('description')
        p.brand = Brand.objects.get(bid=request.POST.get('brand'))
        p.subcat = SubCategory.objects.get(scid=request.POST.get('subCat'))
        p.maincat = MainCategory.objects.get(mcid=request.POST.get('mainCat'))
        p.price = int(request.POST.get('price'))
        p.discount = int(request.POST.get('discount'))
        p.finalPrice = p.price - p.price * p.discount // 100
        p.instock = request.POST.get('stock')
        p.size = request.POST.get('size')
        p.color = request.POST.get('color')
        if(request.FILES.get('img1')):
            p.img1 = request.FILES.get('img1')
        if (request.FILES.get('img2')):
            p.img2 = request.FILES.get('img2')
        if (request.FILES.get('img3')):
            p.img3 = request.FILES.get('img3')
        if (request.FILES.get('img4')):
            p.img4 = request.FILES.get('img4')
        p.save()
        return HttpResponseRedirect('/sellerprofile/')
    maincat = MainCategory.objects.all()
    subcat = SubCategory.objects.all()
    brand = Brand.objects.all()
    return render(request,'editproduct.html',{"Product":p,
                                              "mainCat": maincat,
                                              "subCat": subcat,
                                              "brand": brand
                                              })
@login_required(login_url='/login/')
def buyerProfile(request):
    user=Buyer.objects.get(username=request.user)
    mywishlist = Wishlist.objects.filter(buyer=user)
    if(request.method=='POST'):
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.addressline1 = request.POST.get('addressline1')
        user.addressline2 = request.POST.get('addressline2')
        user.addressline3 = request.POST.get('addressline3')
        user.postcode = request.POST.get('postcode')
        user.city = request.POST.get('city')
        user.state = request.POST.get('state')
        if(request.FILES.get('pic') is not None):
            user.pic = request.FILES.get('pic')
        user.save()
        return HttpResponseRedirect('/buyerprofile/')
    return render(request,'buyerprofile.html',{"User":user,
                                                "wishlist":mywishlist,
                                               })
@login_required(login_url='/login/')
def profile(request):
    user=User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    else:
        try:
            Seller.objects.get(username=request.user)
            return HttpResponseRedirect('/sellerprofile/')
        except:
            return HttpResponseRedirect('/buyerprofile/')

def mywishlist(request,num):
    user = User.objects.get(username=request.user)
    if(user is not None and user.is_superuser):
        return HttpResponseRedirect('/admin/')

    try:
        Seller.objects.get(username=request.user)
        return HttpResponseRedirect('/sellerprofile/')
    except:
        product = Product.objects.get(pid=num)
        buyer = Buyer.objects.get(username=request.user)
        w=Wishlist()
        w.buyer=buyer
        w.product=product
        w.save()
        return HttpResponseRedirect('/buyerprofile/')

def deleteWishlist(request,num):
    wish=Wishlist.objects.get(wid=num)
    wish.delete()
    return HttpResponseRedirect('/buyerprofile/')

def deleteCart(request):
    if(request.session['cart']):
        del request.session['cart']
    return HttpResponseRedirect('/cart/')

def forgetPassword(request):
    if(request.method=='POST'):
        username = request.POST.get('uname')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username)
            try:
                u = Seller.objects.get(username=username)
            except:
                u = Buyer.objects.get(username=username)
            if(email==u.email):
                otp=u.otp = randint(1000,9999)
                u.save()
                subject = "Forget Password OTP"
                mailmessage = "Welcome to Karlshop Please Enter "+str(otp)+" on Confirm OTP Page"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = []
                recipient_list.append(email)
                send_mail(subject, mailmessage, email_from, recipient_list)
                return HttpResponseRedirect('/confirmOTP/'+username+"/")
            else:
                messages.error(request,"Invalid Email Id")
        except:
            messages.error(request,"User Name not Valid")
    return render(request,'forget.html')

def confirmOTP(request,username):
    if(request.method=='POST'):
        otp = int(request.POST.get('otp'))
        try:
            user = User.objects.get(username=username)
            try:
                u = Seller.objects.get(username=username)
            except:
                u = Buyer.objects.get(username=username)
            if (u.otp==otp):
                return HttpResponseRedirect('/generatePassword/' + username + "/")
            else:
                messages.error(request, "Invalid OTP")
        except:
            messages.error(request, "User Name not Valid")
    return render(request,'confirmOTP.html')

def generatePassword(request,username):
    if(request.method=='POST'):
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if(password==cpassword):
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Successfully")
            return HttpResponseRedirect('/login/')
        else:
            messages.error(request,"Password and Confirm Password Must Be Same")
    return render(request,'generatePassword.html')

def process_payment(request,num):
    order = Checkout.objects.get(cid=num)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%d' % order.final,
        'item_name': 'Order {}'.format(order.cid),
        'invoice': "karslShop"+str(order.cid),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'order': order, 'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')
