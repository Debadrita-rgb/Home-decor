from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from store_app.models import Slider,Category,Product,Cart,Wishlist,Address,Order,Contact
import random
import razorpay
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.templatetags.static import static
from pathlib import Path,os
from django.conf import settings
from email.mime.image import MIMEImage
from django import template



# Create your views here.

def index(request):
    context={}  
    # show slider
    sliders=Slider.objects.filter(is_active=True).order_by('id')  
    context['slider']=sliders
    # show category on header
    category=Category.objects.filter(is_active=True)    
    context['categorys']=category

    # show customer choice
    q1=Q(is_customer_choice=True)
    q2=Q(is_active=True)
    product_choice=Product.objects.filter(q1 & q2).order_by('-id')[:10]  
      
    context['products_choice']=product_choice   

    # show Best Selling
    q1=Q(is_bestseller=True)
    q2=Q(is_active=True)
    product_bestseller=Product.objects.filter(q1 & q2).order_by('-id')[:4]        
    context['products_bestseller']=product_bestseller   

    #show category with product
    allProds = []
    product_cat=Category.objects.filter(q2).order_by('-id')[:4]   
    for cat in product_cat:
        catproduct=Product.objects.filter(cat_id=cat.id)[:4]  
        cat_name=cat.cat_name
        cat_id=cat.id

        allProds.append([cat_name , catproduct , cat_id])

    context['cat_product'] = allProds   
    context['title'] = 'Index'
    return render(request,'index.html',context)

def category_details(request,cid):            
    context={}
    # show category
    category=Category.objects.filter(is_active=True)    
    context['categorys']=category

    # show Product
    q1=Q(cat_id=cid)
    q2=Q(is_active=True)
    product_all=Product.objects.filter(q1 & q2).order_by('-id')  
      
    context['products']=product_all    
    context['cat_id']=cid
    return render(request,'category_details.html',context)

def product_detail(request,pid):
    products=Product.objects.get(id=pid)
    # print(p)
    context={}
    context['p'] = products

    category=Category.objects.filter(is_active=True)    
    context['categorys']=category

    return render(request,'product_detail.html',context)

def add_to_cart(request,pid):
    if request.user.is_authenticated:
        user_id=request.user.id
        
        u=User.objects.filter(id=user_id)
        p=Product.objects.get(id=pid)
        # print(p)
        context={}
        #check product exist or not
        q1=Q(uid=u[0])
        q2=Q(pid=p.id)
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context['p']=p

        category=Category.objects.filter(is_active=True)    
        context['categorys']=category

        if n==1:
            context['errmsg']='Product already exist in the cart!!'
        else:
            pr=Product.objects.filter(id=pid)        
            c=Cart.objects.create(uid=u[0],pid=pr[0])
            c.save()        
            context['success']='Product added successfully to cart'            

        return render(request,'product_detail.html',context)

        # return redirect('/product_details/'+pid)
    else:
        return redirect('/login')

def addtocart_cat(request,pid,cid):
    if request.user.is_authenticated:
        user_id=request.user.id
        u=User.objects.filter(id=user_id)
        p=Product.objects.get(id=pid)
        # print(p)
        context={}
        #check product exist or not
        q1=Q(uid=u[0])
        q2=Q(pid=p.id)
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context['p']=p

        category=Category.objects.filter(is_active=True)    
        context['categorys']=category

        q1=Q(cat_id=cid)
        q2=Q(is_active=True)
        product_all=Product.objects.filter(q1 & q2).order_by('-id')  
            
        context['products']=product_all    
        context['cat_id']=cid
        
        if n==1:
            context['errmsg']='Product already exist in the cart!!'
            return render(request,'category_details.html',context)
        else:
            pr=Product.objects.filter(id=pid)        
            c=Cart.objects.create(uid=u[0],pid=pr[0])
            c.save()   
            context['success_msg']='Product added successfully to cart' 
            return render(request,'category_details.html',context)
    else:
        return redirect('/login')

def add_to_wishlist(request,pid):
    if request.user.is_authenticated:
        user_id=request.user.id
        
        u=User.objects.filter(id=user_id)
        p=Product.objects.get(id=pid)
        # print(p)
        context={}
        #check product exist or not
        q1=Q(uid=u[0])
        q2=Q(pid=p.id)
        c=Wishlist.objects.filter(q1 & q2)
        n=len(c)
        context['p']=p

        category=Category.objects.filter(is_active=True)    
        context['categorys']=category

        if n==1:
            context['errmsg']='Product already exist in the wishlist!!'
        else:
            pr=Product.objects.filter(id=pid)        
            c=Wishlist.objects.create(uid=u[0],pid=pr[0])
            c.save()        
            context['success']='Product added successfully to Wishlist'            

        return render(request,'product_detail.html',context)

        # return redirect('/product_details/'+pid)
    else:
        return redirect('/login')

def view_cart(request):
    if request.user.is_authenticated:
        user_id=request.user.id
        context={}

        category=Category.objects.filter(is_active=True)   
        # print(category) 
        context['categorys']=category
    
        c=Cart.objects.filter(uid=user_id).order_by('-id')
        # context={}
        s=0
        for x in c:
            # print(x.pid.price)
            s=s+ x.pid.price*x.qty
        context['data']=c
        context['total']=s
        context['no_of_items']=len(c)


        return render(request,'cart.html',context)

    else:
        return redirect('login')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    # print(c)
    # print(c[0])
    if qv == '1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/view_cart')

def remove_product(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    
    return redirect('/view_cart')

def place_order(request):
    user_id=request.user.id
    context={}

    if request.method=='POST':
        add=request.POST['address']
        ord=Order.objects.filter(uid=user_id, order_status='pending')
        for x in ord:
            ord.update(aid=add)

        q1=Q(is_active=True)
        q2=Q(user_id=user_id)
        q3=Q(id=add)
        address=Address.objects.filter(q1 & q2 & q3)
        context['selected_add']=address[0]       
    else:        
        c=Cart.objects.filter(uid=user_id)
        ord=Order.objects.filter(uid=user_id, order_status='pending')
        if len(ord) > 0:
            oid = ord[0].orderid
        else:
            oid=random.randrange(1000,9999)
        for x in c:
            o=Order.objects.create(orderid=oid,pid=x.pid,uid=x.uid,qty=x.qty)
            o.save()
            x.delete() 
        q1=Q(is_active=True)
        q2=Q(user_id=user_id)
        address=Address.objects.filter(q1 & q2)
        context['address']=address
        
    q1=Q(uid=user_id)
    q2=Q(order_status='pending')
    ord=Order.objects.filter(q1 & q2).order_by('-id')
    context['data']=ord
    s=0 
    add=''
    for x in ord:
        # print(x.pid.price)
        s=s+ x.pid.price*x.qty
        add=x.aid
    # context['add_check']=add
    # print(add)

    category=Category.objects.filter(is_active=True)   
    # print(address) 
    context['categorys']=category
    context['total']=s
    context['no_of_items']=len(ord)
    # print(context)
    return render(request,'place_order.html',context)

def remove_oqty(request,oid):
    c=Order.objects.filter(id=oid)
    c.delete()
    
    return redirect('/place_order')

def makepayment(request):
    q1=Q(uid=request.user.id)
    q2=Q(order_status = 'pending')
    ord=Order.objects.filter(q1 & q2)
    s=0
    for x in ord:
        s=s+ x.pid.price*x.qty
        oid=x.orderid
    
    client = razorpay.Client(auth=("rzp_test_pjmfONoAV5hhRJ", "2qLFlWxOv0vaA1jxWEEHwbcA"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    # print(payment)
    context={}
    context['data']=payment
    uemail=request.user.email
    context['uemail']= uemail
    context['order']=ord
    category=Category.objects.filter(is_active=True)    
    context['categorys']=category

    return render(request,'pay.html',context)

def sendusermail1(request,uemail):

    u=User.objects.filter(email=uemail)

    q1=Q(uid=u[0].id)
    q2=Q(order_status='pending')
    ord=Order.objects.filter(q1 & q2)
    
    
    prod_details = []
    addressID = '';
    orderID = '';
    total_qty = 0;
    total_price = 0;
    for o in ord:
        prod_id = getattr(o.pid, 'id')
        product = Product.objects.filter(id=prod_id)
        prod_details.append([product[0], o.qty])

        addressID = getattr(o.aid, 'id')
        orderID = o.orderid
        total_qty = total_qty + o.qty
        total_price = total_price + (product[0].price * o.qty)
        ord.update(order_status='completed')

    q1=Q(is_active=True)
    q2=Q(user_id=u[0].id)
    q3=Q(id=addressID)
    address=Address.objects.filter(q1 & q2 & q3)
    
    # msg="Order details are:  ''"
    # send_mail(
    #     "Home decor order placed successfully",
    #     msg,
    #     "debadritapaul76@gmail.com",
    #     [uemail],
    #     fail_silently=False,
    # )

    context = {'prod_details': prod_details, 'address': address[0], 'total_qty': total_qty, 'total_price': total_price, 'orderID': orderID}
    text_content = render_to_string('receipt_email.txt', context, request=request)
    html_content = render_to_string('email_template.html', context, request=request)
    emailSubject = 'Home decor order placed successfully'
    emailOfSender = "debadritapaul76@gmail.com"
    emailOfRecipient = uemail


    # try:
        #I used EmailMultiAlternatives because I wanted to send both text and html
    emailMessage = EmailMultiAlternatives(subject=emailSubject, body=text_content, from_email=emailOfSender, to=[emailOfRecipient,], reply_to=[emailOfSender,])
    emailMessage.attach_alternative(html_content, "text/html")
    emailMessage.send(fail_silently=False)

    # except SMTPException as e:
    #     print('There was an error sending an email: ', e) 
    #     error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
    #     raise serializers.ValidationError(error)
    return render(request,'sendmail.html')

def sendusermail(request,uemail):

    u=User.objects.filter(email=uemail)

    q1=Q(uid=u[0].id)
    q2=Q(order_status='pending')
    ord=Order.objects.filter(q1 & q2)
    
    
    prod_details = []
    prod_imgs = []
    addressID = '';
    orderID = '';
    total_qty = 0;
    total_price = 0;
    for o in ord:
        prod_id = getattr(o.pid, 'id')
        product = Product.objects.filter(id=prod_id)

        img_path = os.path.join(settings.BASE_DIR, product[0].image1.url[1:])
        img_base_path = os.path.basename(img_path)

        prod_details.append([product[0], o.qty, img_base_path])
        prod_imgs.append(product[0].image1.url)

        addressID = getattr(o.aid, 'id')
        orderID = o.orderid
        total_qty = total_qty + o.qty
        total_price = total_price + (product[0].price * o.qty)
        ord.update(order_status='completed')

    q1=Q(is_active=True)
    q2=Q(user_id=u[0].id)
    q3=Q(id=addressID)
    address=Address.objects.filter(q1 & q2 & q3)

    # msg="Order details are:  ''"
    # send_mail(
    #     "Home decor order placed successfully",
    #     msg,
    #     "debadritapaul76@gmail.com",
    #     [uemail],
    #     fail_silently=False,
    # )

    
    context = {'prod_details': prod_details, 'address': address[0], 'total_qty': total_qty, 'total_price': total_price, 'orderID': orderID}
    text_content = render_to_string('receipt_email.txt', context, request=request)
    html_content = render_to_string('email_template.html', context, request=request)
    emailSubject = 'Home decor order placed successfully'
    emailOfSender = "debadritapaul76@gmail.com"
    emailOfRecipient = uemail


    # try:
        #I used EmailMultiAlternatives because I wanted to send both text and html
    emailMessage = EmailMultiAlternatives(subject=emailSubject, body=text_content, from_email=emailOfSender, to=[emailOfRecipient,], reply_to=[emailOfSender,])
    emailMessage.attach_alternative(html_content, "text/html")
    emailMessage.mixed_subtype = 'related'

    
    fp = open(os.path.join(settings.STATICFILES_DIRS[0], 'assets/images/lo1.jpg'), 'rb')
    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header('Content-ID', '<{}>'.format('lo1.jpg'))
    emailMessage.attach(msg_img)

    for img in prod_imgs:
        img_path = os.path.join(settings.BASE_DIR, img[1:])
        fp = open(img_path, 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<{}>'.format(os.path.basename(img_path)))
        emailMessage.attach(msg_img)


    emailMessage.send(fail_silently=False)

    # except SMTPException as e:
    #     print('There was an error sending an email: ', e) 
    #     error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
    #     raise serializers.ValidationError(error)
    return render(request,'sendmail.html')


def email_temp(request):
    return render(request, 'email.html')

def view_wishlist(request):
    if request.user.is_authenticated:
        user_id=request.user.id
        context={}
        category=Category.objects.filter(is_active=True)    
        context['categorys']=category

        wishlist=Wishlist.objects.filter(uid=user_id).order_by('-id')
        context={}
        context['data']=wishlist
    
        category=Category.objects.filter(is_active=True)    
        context['categorys']=category
        
        return render(request,'view_wishlist.html',context)
    else:
        pass

def my_address(request):
    if request.user.is_authenticated:
        user_id=request.user.id
        context={}
        category=Category.objects.filter(is_active=True)    
        context['categorys']=category
 
        u=User.objects.filter(id=user_id)

        if request.method == 'POST':
            uname=request.POST['uname']
            address=request.POST['address']
            uemail=request.POST['email']
            city=request.POST['city']
            state=request.POST['state']
            postal_code=request.POST['postal']
            country=request.POST['country']
            phone_number=request.POST['phone']
            
            user=Address.objects.create(name=uname,address=address,email_address=uemail,city=city,state=state,postal_code=postal_code,country=country,phone_number=phone_number,user_id=u[0])
            user.save()
            context['successmsg']='Address Created Successfully'
        else:
            get_address=Address.objects.filter(user_id=u[0])
            # print(get_address)
            context['address']=get_address
        return render(request,'my_address.html',context)

    else:
        return redirect('login')

def deleteaddress(request,aid):
    a=Address.objects.filter(id=aid)
    a.delete()
    return redirect('/my_address')    

def setasdefault(request,aid):
    a=Address.objects.filter(id=aid)
    user_id=request.user.id
    a.update(is_default=1)
    
    
    return HttpResponse('Ko')
    
def register(request):
    context={}
    
    if request.method=='POST':
        uname=request.POST['uname']
        uemail=request.POST['uemail']
        upassword=request.POST['upassword']
        cpassword=request.POST['cpassword']

        if uname =='' or uemail=='' or upassword=='' or cpassword=='':
            context['errmsg'] ="Fields cannot be empty"
        elif upassword != cpassword:
            context['errmsg']="Password and confirm password didnot match"
        else:
            try:
                user=User.objects.create(first_name=uname,username=uemail,email=uemail,password=upassword)
                user.set_password(upassword)
                user.save()
                context['successmsg']='User Created Successfully'
            except Exception:
                context['errmsg'] ="User with same username already exist!!"
        category=Category.objects.filter(is_active=True)    
        context['categorys']=category
        # return render(request,'register.html',context)
        return redirect('/login')
    else:
        category=Category.objects.filter(is_active=True)    
        context['categorys']=category

        return render(request,'register.html',context)

def user_login(request):
    context={}
    
    if request.method == 'POST':
        uname=request.POST['uemail']
        upass=request.POST['upass']
        # print(uname)
        # print(upass)
                
        if uname=='' or upass=='':
            category=Category.objects.filter(is_active=True)    
            context['categorys']=category

            context['errmsg'] = "Fields cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            # print(u)  #object = fourthuser@gmail.com
            if u is not None:
                login(request,u) #start session
                return redirect('/')
            else:
                category=Category.objects.filter(is_active=True)    
                context['categorys']=category

                context['errmsg']='Invalid Username and password'
                return render(request,'login.html',context)
            # context['success_msg']='login successfull'
        
    else:
        category=Category.objects.filter(is_active=True)    
        context['categorys']=category

        return render(request,'login.html',context)
        
def user_logout(request):
    logout(request)
    return redirect('/')    

def sort(request,cid,sv): #sv='0'
    if sv=='0':
        #ascending order
        col='price'
    else:
        #descending order
        col='-price'

    cate=Category.objects.get(id=cid)
    cat_id=cate.id
    
    q1=Q(is_active=True)
    q4=Q(cat_id=cat_id)

    p=Product.objects.filter(q1 & q4).order_by(col)
    
    # p=Product.objects.filter(is_active=True)
    context={}
    context['products']=p
    category=Category.objects.filter(is_active=True)    
    context['categorys']=category
 
    return render(request,'category_details.html',context)

def range(request,cid):
    # min and max value ->request.GET
    min=request.GET.get('min')
    max=request.GET.get('max')
    q1=Q(is_active=True)
    q2=Q(price__gte=min)
    q3=Q(price__lte=max)
    cate=Category.objects.get(id=cid)
    cat_id=cate.id
    q4=Q(cat_id=cat_id)
    p=Product.objects.filter(q1 & q2 & q3 & q4)
    context={}
    context['products']=p
    category=Category.objects.filter(is_active=True)    
    context['categorys']=category
    context['cat_id']=cid
 
    return render(request,'category_details.html',context)  

def order_history(request):
    user_id=request.user.id
    q1=Q(order_status='completed')
    q2=Q(uid=user_id)
    oh=Order.objects.filter(q1 & q2)
    context={}
    context['order_history']=oh

    category=Category.objects.filter(is_active=True)    
    context['categorys']=category

    return render(request,'order_history.html',context)

def about(request):
    context={}
    category=Category.objects.filter(is_active=True)    
    context['categorys']=category
        
    return render(request,'about.html',context)

def privacy(request):
    context={}
    category=Category.objects.filter(is_active=True)    
    context['categorys']=category
    
    return render(request,'privacy.html',context)

def contact(request):
    context={}
    if request.method=='POST':
        uname=request.POST['uname']
        umail=request.POST['umail']
        umob=request.POST['umob']
        umsg=request.POST['umsg']
        # print(uname,'-',umail,'-',umob,'-',umsg)
        u=Contact.objects.create(name=uname,email=umail,mobile=umob,message=umsg,status='contact')        
        u.save()

        msg="We will contact you soon"
        send_mail(
            "Submitted your query successfully",
            msg,
            "debadritapaul76@gmail.com",
            [umail],
            fail_silently=False,
        ) 
        
        context['success_msg']='Your Query is successfully send to us.We will contact you soon'
        return render(request,'contact.html',context)

        # return redirect('/contact')
    else:
        
        category=Category.objects.filter(is_active=True)    
        context['categorys']=category

        return render(request,'contact.html',context)
    
def newsletter(request):
    context={}
    if request.method=='POST':
        umail=request.POST['emails']
        u=Contact.objects.create(email=umail,status='newsletter')        
        u.save()

        msg="We will contact you soon"
        send_mail(
            "Newsletter",
            msg,
            "debadritapaul76@gmail.com",
            [umail],
            fail_silently=False,
        ) 
        
        context['success_msg']='Your email is successfully send to us.We will contact you soon'
        return redirect('/')

     