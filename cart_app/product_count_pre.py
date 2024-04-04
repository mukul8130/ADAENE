from .models import Cart_item_table
from django.shortcuts import redirect,render
# def count_product(req):
#     u=req.user
#     if u.is_authenticated:
#         cp=Cart_item_table.objects.filter(ut=u).count()
    
#     else:
#         cp=0
    
#     return {'count_product':cp}

def count_product(req):
    if req.user.id:
        u=req.user
        cp=Cart_item_table.objects.filter(ut=u).count()
    
    else:
        cp=0
    
    return {'count_product':cp}

def cart(req):
    cart_item=[]
    total=0
    tax=0
    grand_total=0
    u=req.user
    if u.is_authenticated:
        cart_item=Cart_item_table.objects.filter(ut=u)

        for i in cart_item:
            total=total+i.pt.price * i.q
        
        tax=round(total*0.18,2)
        grand_total=round(total+total*0.18,2)
    
    return{ 'cd':cart_item,'total':total,'tax':tax,'grand_total':grand_total}

