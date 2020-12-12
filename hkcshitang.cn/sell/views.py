from django.shortcuts import render
from sell import models
from sell.models import Menu, Disk, Evaluate, Shop, Orders, OrdersMain, Address
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict
import datetime
import redis
import requests
from django.conf import settings


# Create your views here.
def test(request):
    return HttpResponse('ok2')

def get_openid(request):
    try:
        print('*'*100)
        code=request.POST.get('code')
        url = "https://api.weixin.qq.com/sns/jscode2session"
        appid = "wx6e9cfe1751be3166"
        appsecret = "9973b66c851761d52c7de1cfae47c1dd"
        urls = url + "?appid=" + appid + "&secret=" + appsecret + "&js_code=" + code + "&grant_type=authorization_code"
        dic = requests.get(urls).json()
        print('dic', dic)
        openid = dic['openid']
        data={}
        data['openid']=openid
        # url = "https://api.weixin.qq.com/sns/jscode2session?appid=wx6e9cfe1751be3166&secret=9973b66c851761d52c7de1cfae47c1dd&js_code=%s&grant_type=authorization_code" %code
        # result = requests.get(url).content.decode("utf-8")
        # result=loads(result)['openid']
        # data={}
        # data['openid']=result
        #print(data)
        # return ht(dumps(data))
        return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": data}, ensure_ascii=False),
                            content_type="application/json")
    except:
        return HttpResponse(json.dumps({"status": 201, "msg": "error!", "data": "获取code错误"}, ensure_ascii=False),
                            content_type="application/json")
    
    # url = "https://api.weixin.qq.com/sns/jscode2session"
    # appid = settings.APPID
    # secret = settings.SECRET
    # code = request.POST.get('code')

    # @classmethod
    # def get_openid(cls, code):
    #     url = cls.url + "?appid=" + cls.appid + "&secret=" + cls.secret + "&js_code=" + code + "&grant_type=authorization_code"
    #     return requests.get(url).json()


class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y/%m/%d')


def getAllMenu(request):
    queryset = models.Menu.objects.all()
    data = []
    for i in queryset:
        p_temp = {
            "id": i.id,
            "title": i.title,
            "parentId": i.parentId,
            "isParentid": i.isParentid,
        }
        data.append(p_temp)

    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": data}, ensure_ascii=False),
                        content_type="application/json")


def getMenuDisk(request):
    mId = request.GET.get("menuId")
    queryset = None
    if int(mId) == 1:
        queryset = models.Disk.objects.filter(menuId=2)
    else:
        queryset = models.Disk.objects.filter(menuId=mId)
    data = []
    for i in queryset:
        p_temp = {
            "id": i.id,
            "menuId": i.menuId,
            "img": i.img,
            "title": i.title,
            "price": i.price,
            "disPrice": i.disPrice,
            "sellPoint": i.sellPoint,
            "created": i.created,
            "updated": i.updated,
            "sellnum": i.sellnum,
            "status": i.status,
        }
        data.append(p_temp)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": data}, ensure_ascii=False),
                        content_type="application/json")


def getDiskById(request):
    diskId = request.GET.get("diskId")
    queryset = models.Disk.objects.get(id=diskId)
    dictStr = model_to_dict(queryset)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": dictStr}, ensure_ascii=False),
                        content_type="application/json")


def getEvalsByDiskId(request):
    ##根据商户的ID
    diskId = request.GET.get("diskId")
    evaluateList = Evaluate.objects.filter(diskid=diskId)  # 有评论的条数

    countAdd = 0  # 当前的商户所有的点赞分数
    for i in evaluateList:
        temp = i.evalValue
        countAdd += temp
    count = len(evaluateList)
    if count == 0:
        ra = 100
        ratio = "%.2f%%" % ra
    else:
        ratioc = countAdd / (count * 3)
        ratio = "%.2f%%" % (ratioc * 100)
    evals = []
    data = {}
    for i in evaluateList:
        p_temp = {
            "id": i.id,
            "nickname": i.nickname,
            "avatarUrl": i.avatarUrl,
            "content": i.content,
            "imgs": i.imgs,
            "evalValue": i.evalValue,
            "isAnonymous": i.isAnonymous,
            "created": str(i.created),
        }
        evals.append(p_temp)
    data["ratio"] = ratio
    data["count"] = count
    data["evals"] = evals

    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": data}, ensure_ascii=False),
                        content_type="application/json")


def getAllCartList(openid):
    CarList = []
    pool = redis.ConnectionPool(host='127.0.0.1', port='6379')
    coon = redis.Redis(connection_pool=pool)
    carlist = coon.get(openid)
    globals = {
        'true': 0,
        'false': 1,
    }
    if carlist:
        calist = carlist.decode()
        strlist = eval(calist, globals)
        CarList.extend(strlist)
        for i in CarList:
            if i["selected"] == 0:
                i["selected"] = True
            else:
                i["selected"] = False
    return CarList


def saveCart(openid, cartList):
    pool = redis.ConnectionPool(host='127.0.0.1', port='6379')
    conn = redis.Redis(connection_pool=pool)
    jsonArr = json.dumps(cartList, ensure_ascii=False)
    CartList = conn.set(openid, jsonArr)


def addCart(request):
    openid = request.GET.get("openid")
    diskid = request.GET.get("diskId")
    cartList = getAllCartList(openid)
    flag = False
    for i in cartList:
        if i["id"] == int(diskid):
            i["num"] = i["num"] + 1
            flag = True
            break
    if not flag:
        disk = Disk.objects.get(id=diskid)
        p_temp = {
            "id": disk.id,
            "menuId": disk.menuId,
            "img": disk.img,
            "title": disk.title,
            "price": disk.price,
            "disPrice": disk.disPrice,
            "sellPoint": disk.sellPoint,
            "created": disk.created,
            "updated": disk.updated,
            "sellnum": disk.sellnum,
            "status": disk.status,
            "num": 1,
            "selected": True,
        }
        cartList.append(p_temp)
        # 存储到redis
    saveCart(openid, cartList)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": "", "count": ""}, ensure_ascii=False),
                        content_type="application/json")


def getAllCart(request):
    openid = request.GET.get('openid')
    carList = getAllCartList(openid)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": carList}, ensure_ascii=False),
                        content_type="application/json")


def changeSelected(request):
    openid = request.GET.get("openid")
    diskid = request.GET.get("diskId")
    carList = getAllCartList(openid)
    for i in carList:
        if i["id"] == int(diskid):
            i["selected"] = not i["selected"]
            break

    saveCart(openid, carList)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": ""}, ensure_ascii=False),
                        content_type="application/json")


def substractCart(request):
    openid = request.GET.get("openid")
    diskid = request.GET.get("diskId")
    carList = getAllCartList(openid)
    for i in carList:
        if i["id"] == int(diskid):
            i["num"] = i["num"] - 1
            if i["num"] <= 0:
                carList.remove(i)
    saveCart(openid, carList)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": ""}, ensure_ascii=False),
                        content_type="application/json")


def delCartByDiskId(request):
    openid = request.GET.get("openid")
    diskid = request.GET.get("diskId")
    cartList = getAllCartList(openid)
    for i in cartList:
        if i["id"] == int(diskid):
            cartList.remove(i)
    saveCart(openid, cartList)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": ""}, ensure_ascii=False),
                        content_type="application/json")


def getShopInfo(request):
    Shopinfo = Shop.objects.get(id=1)
    shopdict = model_to_dict(Shopinfo)
    shopdict['time'] = str((datetime.datetime.now()))
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": shopdict}, ensure_ascii=False),
                        content_type="application/json")


def addAddress(request):
    openid = request.GET.get("openid")
    name = request.GET.get("name")
    mobile = request.GET.get("mobile")
    gender = request.GET.get("gender")
    address = request.GET.get("address")
    isDefault = request.GET.get("isDefault")
    a = Address()
    a.openid = openid
    a.name = name
    a.mobile = mobile
    a.gender = gender

    a.address = address
    a.isDefault = isDefault
    a.save()
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": ""}, ensure_ascii=False),
                        content_type="application/json")


def getAddrsByOpenid(request):
    openid = request.GET.get("openid")
    addAddressList = Address.objects.filter(openid=openid)
    data = []
    for i in addAddressList:
        p_temp = {
            "id": i.id,
            "name": i.name,
            "mobile": i.mobile,
            "gender": i.gender,
            "address": i.address,
            "isDefault": i.isDefault,
        }
        data.append(p_temp)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": data}, ensure_ascii=False),
                        content_type="application/json")


def changeDefaultAddr(request):
    openid = request.GET.get("openid")
    addrId = request.GET.get("addrId")
    addressList = Address.objects.filter(openid=openid)

    for i in addressList:
        if i.id == int(addrId):
            i.isDefault = 1
        else:
            i.isDefault = 0
        i.save()
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": ""}, ensure_ascii=False),
                        content_type="application/json")


def getAddrByAddrId(request):
    addrId = request.GET.get("addrId")
    address = Address.objects.get(id=int(addrId))
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": model_to_dict(address)}, ensure_ascii=False),
                        content_type="application/json")


def updateAddress(request):
    id = request.GET.get("id")
    openid = request.GET.get("openid")
    name = request.GET.get("name")
    mobile = request.GET.get("mobile")
    gender = request.GET.get("gender")
    address = request.GET.get("address")
    isDefault = request.GET.get("isDefault")
    a = Address.objects.get(id=id)
    a.openid = openid
    a.name = name
    a.mobile = mobile
    a.gender = gender

    a.address = address
    a.isDefault = isDefault
    a.save()
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": ""}, ensure_ascii=False),
                        content_type="application/json")


def delAddrByAddrId(request):
    addid = request.GET.get("addrId")
    address = Address.objects.get(id=int(addid))
    address.delete()
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": ""}, ensure_ascii=False),
                        content_type="application/json")


def getSelectedCartUtil(openid):
    cartlist = getAllCartList(openid)
    data = []
    for i in cartlist:
        if i["selected"] == True:
            data.append(i)
    return data


def getSelectedCart(request):
    openid = request.GET.get("openid")
    data = getSelectedCartUtil(openid)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": data}, ensure_ascii=False),
                        content_type="application/json")


def getDefaultAddr(request):
    openid = request.GET.get("openid")
    addAddressList = Address.objects.filter(openid = openid)
    #data = []
    data = {}
    for item in addAddressList:
        #if item.isDefault:
        if item.isDefault == 1:
            data = item
    # address = Address.objects.get(isDefault=int(1))
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": model_to_dict(data) }, ensure_ascii=False),
                        content_type="application/json")


def saveOrder(request):
    openid = request.GET.get("openid")
    totalMoney = request.GET.get("totalMoney")
    remarks = request.GET.get("remarks")
    selectedAddrId = request.GET.get("selectedAddrId")
    orderid = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + openid
    datalist = getSelectedCartUtil(openid)
    for i in datalist:
        order = Orders()
        order.totalMoney = int(totalMoney)
        order.remarks = remarks
        order.addressid = int(selectedAddrId)
        order.orderid = orderid
        order.status = 2
        order.isEvaluate = 1
        order.num = int(i["num"])
        order.diskid = int(i["id"])
        order.save()
    ordersMain = OrdersMain()
    ordersMain.orderid = orderid
    ordersMain.totalMoney = int(totalMoney)
    ordersMain.remarks = remarks
    ordersMain.status = 2
    ordersMain.isEvaluate = 1
    ordersMain.createtime = datetime.datetime.now()
    ordersMain.save()
    # pool = redis.ConnectionPool(host='127.0.0.1', port='6379')
    # coon = redis.Redis(connection_pool=pool)
    # coon.delete_pattern(openid)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": orderid}, ensure_ascii=False),
                        content_type="application/json")


def getAllOrder(request):
    openid = request.GET.get("openid")
    ordermain = OrdersMain.objects.filter(orderid__contains=openid)
    data = []
    for i in ordermain:
        orderList = Orders.objects.filter(orderid=i.orderid)
        items = []
        for i in orderList:
            diskid = i.diskid
            disk = Disk.objects.get(id=int(diskid))
            diskdict = model_to_dict(disk)
            diskdict['num'] = i.num
            items.append(diskdict)

        p_temp = {
            "orderId": i.orderid,
            "status": i.status,
            "totalMoney": i.totalMoney,
            "items": items,
            "isEvaluate": i.isEvaluate,
        }
        data.append(p_temp)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": data}, ensure_ascii=False),
                        content_type="application/json")


def changeStatus(request):
    orderId = request.GET.get("orderId")
    flag = request.GET.get("flag")
    orderList = Orders.objects.filter(orderid=orderId)
    for i in orderList:
        if int(flag) == 2:
            i.status = 5
            i.save()
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": ""}, ensure_ascii=False),
                        content_type="application/json")


def getOrderDetailByOrderId(request):
    orderId = request.GET.get("orderId")
    ordermain = OrdersMain.objects.get(orderid=orderId)
    data = {}
    items = []
    orderList = Orders.objects.filter(orderid=ordermain.orderid)
    p_temp = {
        "orderId": ordermain.orderid,
        "status": ordermain.status,
        "totalMoney": ordermain.totalMoney,
        "createTime": str(ordermain.createtime),
        "isEvaluate": ordermain.isEvaluate,
    }
    addid = int(orderList[0].addressid)
    address = Address.objects.get(id=addid)
    addressDict = model_to_dict(address)
    for i in orderList:
        diskid = i.diskid
        disk = Disk.objects.get(id=int(diskid))
        diskdict = model_to_dict(disk)
        diskdict['num'] = i.num
        items.append(diskdict)
    data.update(p_temp)
    data["orderAddr"] = addressDict
    data["items"] = items
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": data}, ensure_ascii=False),
                        content_type="application/json")


def getDisksByOrderId(request):
    orderId = request.GET.get("orderId")
    ordermain = OrdersMain.objects.get(orderid=orderId)
    orderList = Orders.objects.filter(orderid=ordermain.orderid)
    data = []
    for i in orderList:
        diskid = i.diskid
        disk = Disk.objects.get(id=int(diskid))
        diskdict = model_to_dict(disk)
        diskdict['diskId'] = i.diskid
        diskdict['num'] = i.num
        diskdict['orderId'] = orderId
        data.append(diskdict)
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": data}, ensure_ascii=False),
                        content_type="application/json")


def saveEvals(request):
    evals = request.GET.get("evals")
    globals = {
        'true': 0
    }
    strList = eval(evals, globals)
    nickname = request.GET.get("nickname")
    avatarUrl = request.GET.get("avatarUrl")
    isAnonymous = request.GET.get("isAnonymous")
    for i in strList:
        evaluate = Evaluate()
        evaluate.diskid = int(i["diskId"])
        evaluate.orderid = i["orderId"]
        evaluate.openid = i["openid"]
        evaluate.imgs = i["imgs"]
        evaluate.content = i["content"]
        evaluate.nickname = nickname
        evaluate.avatarUrl = avatarUrl
        evaluate.isAnonymous = int(isAnonymous)
        evaluate.evalValue = i["evalValue"]
        evaluate.created = datetime.datetime.now()
        evaluate.save()
        orderList = Orders.objects.filter(orderid=i["orderId"])
        for i in orderList:
            i.status = 2
            i.save()
    return HttpResponse(json.dumps({"status": 200, "msg": "OK!", "data": ""}, ensure_ascii=False),
                        content_type="application/json")
