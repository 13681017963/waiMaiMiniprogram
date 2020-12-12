"""mwaimai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from sell import views
from django.conf.urls import url
import xadmin

urlpatterns = [
    url(r'^test', views.test),
    url(r'^disk/wxLogin', views.get_openid),
    url(r'^menu/getAllMenu', views.getAllMenu),
    url(r'^disk/getMenuDisk', views.getMenuDisk),
    url(r'^disk/getDiskById', views.getDiskById),
    url(r'^evaluate/getEvalsByDiskId', views.getEvalsByDiskId),
    url(r'^cart/addCart', views.addCart),
    url(r'^cart/getAllCart', views.getAllCart),
    url(r'^cart/changeSelected', views.changeSelected),
    url(r'^cart/substractCart', views.substractCart),
    url(r'^cart/delCartByDiskId', views.delCartByDiskId),
    url(r'^shop/getInfo', views.getShopInfo),
    url(r'^address/addAddress', views.addAddress),
    url(r'^address/getAddrsByOpenid', views.getAddrsByOpenid),
    url(r'^address/changeDefaultAddr', views.changeDefaultAddr),
    url(r'^address/getAddrByAddrId', views.getAddrByAddrId),
    url(r'^address/updateAddress', views.updateAddress),
    url(r'^address/delAddrByAddrId', views.delAddrByAddrId),
    url(r'^cart/getSelectedCart', views.getSelectedCart),
    url(r'^address/getDefaultAddr', views.getDefaultAddr),
    url(r'^order/saveOrder', views.saveOrder),
    url(r'^order/getAllOrder', views.getAllOrder),
    url(r'^order/changeStatus', views.changeStatus),
    url(r'^order/getOrderDetailByOrderId', views.getOrderDetailByOrderId),
    url(r'^order/getDisksByOrderId', views.getDisksByOrderId),
    url(r'^evaluate/saveEvals', views.saveEvals),
    path('xadmin/', xadmin.site.urls),
]
