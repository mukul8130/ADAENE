from django.shortcuts import render,redirect,HttpResponse
from product_app.models import Product_table,Variation_table
from category_app.models import Category_table
from cart_app.models import Cart_item_table

# Login
from django.contrib import auth
from django.contrib import messages
# /Login

#registration
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
#/registraion

def home(req):
    return render(req,'index.html')


def shop(req):
    PTD=Product_table.objects.all()
    
    total_pro_qun=[i.id for i in PTD]
    z1=len(total_pro_qun)
    # print(z1)
  
    con={
        'ptd':PTD,
        'total_pro_qun':z1
    }
    return render(req,'shop_page.html',con)

def category(req,x):
    CTD=Product_table.objects.filter(category__category_name=x)
    
    cat_pro_qun=[i.id for i in CTD]
    z2=len(cat_pro_qun)
        # print(z2)
    
    con={
        'ptd':CTD,
        'x':x,
        'cat_pro_qun':z2
    }
    return render(req,'shop_page.html',con)

def filter_price(req):
    if req.method=='POST':
        min_price=0
        max_price=req.POST['Max']
        # print(min_price)
        # print(max_price)
        if(max_price):
            product_price=Product_table.objects.filter(price__range=(min_price,max_price))
            
            f_price_pro_qun=[i.price for i in product_price]
            z3=len(f_price_pro_qun)
            # print(z3)
            if(z3>0):
                con={
                    'ptd':product_price,
                    'f_price_pro_qun':z3
                }
                return render(req,'shop_page.html',con)
            
            else:
                con={
                    'ptd':product_price,
                    'f_price_pro_qun':'0'
                }
                return render(req,'shop_page.html',con)
        
        
def login(req):
    if req.method=='POST':
        n=req.POST['login_username']
        p=req.POST['login_password']
        u=auth.authenticate(username=n,password=p)

        if u:
            auth.login(req,u)
            messages.success(req,'Login Successfull')
            return redirect('/')
        
        else:
            messages.error(req,'User Does Not Exists')
            return render(req,'login.html')

    return render(req,'login.html')

def logout(req):
    auth.logout(req)
    messages.success(req,'Logout Successfull')
    return redirect('/')

def sign_up(req):
    if(req.method=='POST'):
        name=req.POST['name']
        ln=req.POST['lastname']
        un=req.POST['username']
        em=req.POST['email']
        cp=req.POST['cp']
        rp=req.POST['rp']

        def sg(name,ln,un,em,cp,rp):
            if cp != rp:
                messages.error(req,'Password does not match')
            elif User.objects.filter(email=em).exists():
                messages.error(req,'Email is already exists')
            elif User.objects.filter(username=un).exists():
                messages.error(req,'Username is already exists')

            else:
                ud=User.objects.create_user(first_name=name,last_name=ln,username=un,email=em,password=cp,is_active=False)
                ud.save()

                domain_name=get_current_site(req)
                mail_subject='Please click and activate your account'
                user_id=urlsafe_base64_encode(force_bytes(ud.pk))
                token=default_token_generator.make_token(ud)
                msg=f'http://{domain_name}/activate_account/{user_id}/{token}'
                to_email=em
                send_email=EmailMessage(mail_subject,msg,to=[to_email])
                send_email.send()
                messages.success(req,"Check your mail")

        sg(name,ln,un,em,cp,rp)

    return render(req,'sign_up.html')

def activate(req,user_id,token):
    try:
        x=urlsafe_base64_decode(user_id)
        y=User.objects.get(pk=x)

        if(default_token_generator.check_token(y,token)):
            y.is_active=True
            y.save()
            messages.success(req,"Verification Successfull")
            return redirect('/login')
    
    except:
        messages.error(req,"Invalid Credential")
    return redirect('/sign_up')



from django.core.exceptions import ObjectDoesNotExist
def forgot(req):
    if req.method=='POST':
        em=req.POST['E_ADD']
        if(em==""):
            messages.error(req,"Please enter the email")
            print('1')

        elif req.method=='POST':
            print('2')
            em=req.POST['E_ADD']
            # print(e)
            try:
                U=User.objects.get(email=em)
                domain_name=get_current_site(req)
                mail_subject="Reset Password"
                user_id=urlsafe_base64_encode(force_bytes(U.pk))
                token=default_token_generator.make_token(U)
                message=f'http://{domain_name}/reset-password/{user_id}/{token}'
                to_email=em

                send_email=EmailMessage(mail_subject,message,to=[to_email])
                send_email.send()
                messages.success(req,'Reset link sent to your email')
        
            except ObjectDoesNotExist:
                messages.error(req,'No email exists')

    return render(req,'forgot.html')

def reset_pass(req,user_id,token):
    try:
        z=urlsafe_base64_decode(user_id)
        z1=User.objects.get(pk=z)

        if default_token_generator.check_token(z1,token):
            req.session['user_id']=user_id
            messages.success(req,'Please create new password')
            return render(req,'reset_pass.html')
    
    except:
        return redirect('/sign_up')
    
    
def resetpassword(req):
    if req.method=="POST":
        p1=req.POST['p1']
        p2=req.POST['p2']

        if(p1==p2):
            uid=req.session['user_id']
            u=User.objects.get(id=urlsafe_base64_decode(uid))
            u.set_password(p1)
            u.save()
            messages.success(req,'Password reset successfully')
            return redirect('/login')
        
        else:
            messages.error(req,'Password does not match')
            return redirect('/reset')
    
    else:
        return render('reset_pass.html')
    

from django.core.mail import send_mail
def sendmsg(req):
    if(req.method=="POST"):
        fn=req.POST['fn']
        ln=req.POST['ln']
        user_em=req.POST['em']
        sb=req.POST['sub']
        ms=req.POST['msg']

        name = fn + " " + ln
        sub="Subject :" + sb
        msg = "From : " + name + "\r\n" + "Massage :" + ms 

        # u=req.user.username

        sender_email=user_em
        mail='mukulgupta8130@gmail.com'

        send_mail(sub,msg,sender_email,[mail],fail_silently=False)

        messages.success(req,"Massage Sent Successfully")

    else:
        messages.error(req,"Massage not sent")

    return render(req,'index.html')


from emails_app.models import email_table
def emailmsg(req):
    if(req.method=='POST'):
        em=req.POST['EMAIL']
        email=email_table(email=em)
        email.save()
        messages.success(req,'You Have Joined The Mailing List')

    return render(req,'index.html')

def send_msg_users(req):
    if(req.method=="POST"):
        msg=req.POST['msg']
        print(msg)
        x=email_table.objects.all()
        l=[]
        # x1=[i.email for i in x] isse bhi list mai data save hota hai or aise bhi
        for i in x:
            l.append(i.email)
        for i1 in l:
            # print(i1)
            se=i1
            mail='mukulgupta8130@gmail.com'
            sub='hello guys i am owner this website THENORTHPOLE'
            # msg='Tomorrow the rates of bags will be 50% off '
            send_mail(sub,msg,mail,[se],fail_silently=False)
        messages.success(req,'Msg Send Successfully')

    return redirect('/')


def product_page(req,pro_id):
    x=Product_table.objects.get(id=pro_id)
    color_variant=Variation_table.objects.filter(pt=x,variation_category='color')
    size_variant=Variation_table.objects.filter(pt=x,variation_category='size')
    
    ###### Single product id ke base par Catergory vise data nikali hai ######
    #.exclude ka mtlb hai ki iss vaali id ka data mat dena iss id ko chode ka sara data dedo category ka  
    product_category = x.category 
    y=Product_table.objects.filter(category=product_category).exclude(id=pro_id)[:4]
    # y=Product_table.objects.filter(category=product_category)[:4]

    ########################

    z1=x.stock
    # print(z1)

    context={
        'z':x,
        'color':color_variant,
        'size':size_variant,
        'stock':z1,
        'y':y
    }
    return render(req,'product_page.html',context)

def Cart(req):
    u=req.user.id
    if u: 
        cart_item=Cart_item_table.objects.filter(ut=u)
    
        total=0
        for i in cart_item:
            total=total+i.pt.price * i.q
    
        c={
            'cart_item':cart_item,
            'total':total,
            'tax':round(total*0.18,2),
            'grand_total':round(total+total*0.18,2)

        }

        return render(req,'cart.html',c)
    
    else:
        return render(req,'cart.html')
    

# def Add_to_cart(req,product_id):
#     user=req.user
#     if user.is_authenticated:
#         p=Product_table.objects.get(id=product_id)

#         if req.method=="POST":
#             color=req.POST['color']
#             size=req.POST['size']

#             size_variant=Variation_table.objects.get(variation_value=color,pt=p)
#             color_variant=Variation_table.objects.get(variation_value=size,pt=p)

#             current_variant=[size_variant,color_variant]

#             is_product_exists=Cart_item_table.objects.filter(pt=p,ut=user).exists()

#             if is_product_exists:

#                 each_product_variant=[]
#                 products=Cart_item_table.objects.filter(pt=p,ut=user)

#                 for product1 in products:
#                     each_product_variant.append(list(product1.vt.all()))

#                 if current_variant in each_product_variant:
#                     product_index=each_product_variant.index(current_variant)
#                     product1=products[product_index]
#                     product1.q+=1
#                     product1.save()
#                     messages.success(req,"Please Check Your Cart")
#                     return redirect('/shop')

#                 else:
#                     product1=Product_table.objects.get(id=product_id)
#                     c=Cart_item_table.objects.create(pt=product1,ut=user,q=1)
#                     c.vt.add(color_variant)
#                     c.vt.add(size_variant)
#                     messages.success(req,'Please Check Your Cart')
#                     return redirect("/shop")

#             else:
#                 z=Cart_item_table.objects.create(pt=p,ut=user,q=1)
#                 z.vt.add(color_variant) 
#                 z.vt.add(size_variant)
#                 messages.success(req,"Please Check Your Cart")
#                 return redirect("/shop")
#     else:
#         messages.error(req,"Please Login")
#     return redirect('/')
    

def Add_to_cart(req,product_id):
    user=req.user
    if user.is_authenticated:
        p=Product_table.objects.get(id=product_id)

        if req.method=="POST":

            if 'color' in req.POST and 'size' in  req.POST:

                color=req.POST['color']
                print(color)
                size=req.POST['size']
                print(size)

                size_variant=Variation_table.objects.get(variation_value=color,pt=p)
                print(size_variant)
                color_variant=Variation_table.objects.get(variation_value=size,pt=p)
                print(color_variant)
                current_variant=[size_variant,color_variant]
                print(current_variant)

                is_product_exists=Cart_item_table.objects.filter(pt=p,ut=user).exists()

                if is_product_exists:

                    each_product_variant=[]
                    products=Cart_item_table.objects.filter(pt=p,ut=user)
                    print(products)

                    for product1 in products:
                        each_product_variant.append(list(product1.vt.all()))
                    print(each_product_variant)

                    if current_variant in each_product_variant:
                        product_index=each_product_variant.index(current_variant)
                        product1=products[product_index]
                        quantity=int(req.POST['quan'])
                        x=Product_table.objects.get(id=product_id)
                        stock=x.stock
                        if(product1.q<stock):
                            product1.q+=quantity<=stock
                            product1.save()
                            messages.success(req,"Please Check Your Cart")
                            return redirect('/shop')
                        
                        else:
                            messages.error(req,'Out Of Stock')
                            return redirect('/cart_page')

                    else:
                        quantity=int(req.POST['quan'])
                        product1=Product_table.objects.get(id=product_id)
                        c=Cart_item_table.objects.create(pt=product1,ut=user,q=quantity)
                        c.vt.add(color_variant)
                        c.vt.add(size_variant)
                        messages.success(req,'Please Check Your Cart')
                        return redirect("/shop")

                else:
                    quantity=int(req.POST['quan'])
                    z=Cart_item_table.objects.create(pt=p,ut=user,q=quantity)
                    z.vt.add(color_variant) 
                    z.vt.add(size_variant)
                    messages.success(req,"Please Check Your Cart")
                    return redirect("/shop")

            elif 'color' in req.POST:
                color=req.POST['color']
                print(color)
                color_variant=Variation_table.objects.get(variation_value=color,pt=p)
                current_variant=[color_variant]

                is_product_exists=Cart_item_table.objects.filter(pt=p,ut=user).exists()

                if is_product_exists:

                    each_product_variant=[]
                    products=Cart_item_table.objects.filter(pt=p,ut=user)

                    for product1 in products:
                        each_product_variant.append(list(product1.vt.all()))

                    if current_variant in each_product_variant:
                        product_index=each_product_variant.index(current_variant)
                        product1=products[product_index]
                        quantity=int(req.POST['quan'])
                        x=Product_table.objects.get(id=product_id)
                        stock=x.stock
                        if(product1.q<stock):
                            product1.q+=quantity<=stock
                            product1.save()
                            messages.success(req,"Please Check Your Cart")
                            return redirect('/shop')
                        
                        else:
                            messages.error(req,'Out Of Stock')
                            return redirect('/cart_page')

                    else:
                        product1=Product_table.objects.get(id=product_id)
                        quantity=int(req.POST['quan'])
                        c=Cart_item_table.objects.create(pt=product1,ut=user,q=quantity)
                        c.vt.add(color_variant)
                        # c.vt.add(size_variant)
                        messages.success(req,'Please Check Your Cart')
                        return redirect("/shop")

                else:
                    quantity=int(req.POST['quan'])
                    z=Cart_item_table.objects.create(pt=p,ut=user,q=quantity)
                    z.vt.add(color_variant) 
                    # z.vt.add(size_variant)
                    messages.success(req,"Please Check Your Cart")
                    return redirect("/shop")

    else:
        messages.error(req,"Please Login")
    return redirect('/')
    

    
    


def remove_btn(req,product_id):
    user=req.user
    ci=Cart_item_table.objects.get(id=product_id,ut=user)
    ci.delete()
    return redirect('/cart_page')

def minus_btn(req,product_id):
    user=req.user
    ci=Cart_item_table.objects.get(id=product_id,ut=user)
    
    if ci.q>1:
        ci.q -= 1
        ci.save()
    
    else:
        ci.delete()
    
    return redirect('/cart_page')


from django.shortcuts import get_object_or_404
def plus_btn(req,product_id):
    user=req.user
    ci=Cart_item_table.objects.get(id=product_id,ut=user)

    x=get_object_or_404(Cart_item_table,id=product_id)
    stock_quantity=x.pt.stock

    if(ci.q<stock_quantity):
        if(ci.q>=1):
            ci.q=ci.q+1
            # ci.q+=1
            ci.save()
        
        return redirect('/cart_page')

    else:
        messages.error(req,'Out of stock')
        return redirect('/cart_page')


