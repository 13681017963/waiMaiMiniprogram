import xadmin
from django.http import HttpResponse
from xadmin import views
from .models import Menu, Orders, OrdersMain, Shop, Address, Disk, Evaluate
from xadmin.plugins.actions import BaseActionView
import json


class BaseSetting(object):
    # 开启主题功能
    enable_themes = True


class GlobalSettings(object):
    # 修改title
    site_title = '外卖后台管理界面'
    # 修改footer
    site_footer = '外卖公司'
    # 收起菜单
    menu_style = 'accordion'


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)


class MenuAdmin(object):
    list_display = ['title', 'parentId', 'isParentid']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['title', 'parentId', 'isParentid']
    # 过滤
    list_filter = ['title', 'parentId', 'isParentid']


class OrdersAdmin(object):
    list_display = ['orderid', 'orderDetail', 'num', 'totalMoney', 'remarks', 'addressid', 'addressName', 'diskid', 'status',
        'isEvaluate']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['orderid', 'totalMoney', 'remarks', 'addressid', 'diskid', 'status', 'isEvaluate', 'num']
    # 过滤
    list_filter = ['orderid', 'totalMoney', 'remarks', 'addressid', 'diskid', 'status', 'isEvaluate', 'num']

    def orderDetail(self, obj):
        res = Disk.objects.filter(id=obj.diskid, status=1)
        list = []
        for x in res:
            list.append(x.title)
        return ','.join(list)
        
    def addressName(self, obj):
        res = Address.objects.filter(id=obj.addressid)
        list = []
        for x in res:
            list.append(x.address)
        return ','.join(list)

    orderDetail.allow_tags = True
    orderDetail.short_description = '菜名'
    
    addressName.allow_tags = True
    addressName.short_description = '地址'


class OrdersDetails(BaseActionView):
    # 这里需要填写三个属性
    # 1. 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    action_name = "Orders_Details"
    # 2. 描述, 出现在 Action 菜单中,
    description = ('查看订单详情')
    # 3. 该 Action 所需权限
    model_perm = 'change'

    # 而后实现 do_action 方法
    def do_action(self, queryset):
        for i in queryset:
            orderid = i.orderid
            res = Orders.objects.filter(orderid=orderid, status=2)
            list = []
            for x in res:
                dict = {}
                disk_res = Disk.objects.filter(id=x.diskid, status=1)
                for y in disk_res:
                    dict['title'] = y.title
                dict['num'] = x.num
                list.append(dict)
        # 返回 HttpResponse
        return HttpResponse(json.dumps(list), content_type='application/json')


class OrdersMainAdmin(object):
    actions = [OrdersDetails, ]
    list_display = ['orderid', 'totalMoney', 'remarks', 'status', 'isEvaluate', 'createtime']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['orderid', 'totalMoney', 'remarks', 'status', 'isEvaluate', 'createtime']
    # 过滤
    list_filter = ['orderid', 'totalMoney', 'remarks', 'status', 'isEvaluate', 'createtime']


class ShopAdmin(object):
    list_display = ['name', 'address', 'time', 'phone']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'address', 'time', 'phone']
    # 过滤
    list_filter = ['name', 'address', 'time', 'phone']


class AddressAdmin(object):
    list_display = ['openid', 'name', 'mobile', 'gender', 'address', 'isDefault']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['openid', 'name', 'mobile', 'gender', 'address', 'isDefault']
    # 过滤
    list_filter = ['openid', 'name', 'mobile', 'gender', 'address', 'isDefault']


class DiskAdmin(object):
    list_display = ['menuId', 'img', 'title', 'price', 'disPrice', 'sellPoint', 'created', 'updated', 'sellnum',
                    'status']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['menuId', 'img', 'title', 'price', 'disPrice', 'sellPoint', 'created', 'updated', 'sellnum',
                     'status']
    # 过滤
    list_filter = ['menuId', 'img', 'title', 'price', 'disPrice', 'sellPoint', 'created', 'updated', 'sellnum',
                   'status']


class EvaluateAdmin(object):
    list_display = ['diskid', 'orderid', 'openid', 'imgs', 'content', 'evalValue', 'created', 'isAnonymous', 'nickname',
                    'avatarUrl']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['diskid', 'orderid', 'openid', 'imgs', 'content', 'evalValue', 'created', 'isAnonymous',
                     'nickname', 'avatarUrl']
    # 过滤
    list_filter = ['diskid', 'orderid', 'openid', 'imgs', 'content', 'evalValue', 'created', 'isAnonymous', 'nickname',
                   'avatarUrl']


xadmin.site.register(Menu, MenuAdmin)
xadmin.site.register(Orders, OrdersAdmin)
xadmin.site.register(OrdersMain, OrdersMainAdmin)
xadmin.site.register(Shop, ShopAdmin)
xadmin.site.register(Address, AddressAdmin)
xadmin.site.register(Disk, DiskAdmin)
xadmin.site.register(Evaluate, EvaluateAdmin)
