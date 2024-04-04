"""bag_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('shop/',shop),
    path('shop/category/<x>',category),
    path('filter_price/',filter_price),
    path('login/',login),
    path('logout/',logout),
    path('sign_up/',sign_up),
    path('activate_account/<user_id>/<token>/',activate),
    path('forgot/',forgot),
    path('reset-password/<user_id>/<token>/',reset_pass),
    path('reset/',resetpassword),
    path('sendmsg/',sendmsg),
    path('emailmsg/',emailmsg),
    path('send_msg_users/',send_msg_users),
    path('product_page/<pro_id>',product_page),
    path('cart_page/',Cart),
    path('Add_to_cart/<product_id>',Add_to_cart),
    path('remove_btn/<product_id>',remove_btn),
    path('minus_btn/<product_id>',minus_btn),
    path('plus_btn/<product_id>',plus_btn)
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
