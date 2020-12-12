from django.db import models


# Create your models here.
class Menu(models.Model):
    title = models.CharField('菜单名', max_length=20)
    parentId = models.IntegerField('父菜单ID', default=0)
    isParentid = models.IntegerField('是否为父菜单', default=0)

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Disk(models.Model):
    menuId = models.IntegerField('菜单ID', default=0)
    img = models.CharField('图片', max_length=100)
    title = models.CharField('菜名', max_length=100)
    price = models.FloatField('价格', default=0)
    disPrice = models.FloatField('disprice', default=0)
    sellPoint = models.CharField('备注', max_length=100)
    created = models.CharField('创建时间', max_length=100)
    updated = models.CharField('更新时间', max_length=100)
    sellnum = models.IntegerField('分数', default=0)
    status = models.IntegerField('状态', default=0)

    class Meta:
        verbose_name = '商户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.menuId


class Shop(models.Model):
    name = models.CharField('食堂名', max_length=100)
    address = models.CharField('地址', max_length=100)
    time = models.DateField('创建时间', max_length=100)
    phone = models.CharField('手机号', max_length=100)

    class Meta:
        verbose_name = '购物'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Address(models.Model):
    openid = models.CharField(max_length=100)
    name = models.CharField('地址名', max_length=100)
    mobile = models.CharField('电话', max_length=100)
    gender = models.IntegerField(default=0)
    address = models.CharField('地址', max_length=100)
    isDefault = models.IntegerField('是否默认地址', default=0)

    class Meta:
        verbose_name = '地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Orders(models.Model):
    orderid = models.CharField('订单ID', max_length=100)
    totalMoney = models.IntegerField('总价格', max_length=100)
    remarks = models.CharField('备注', max_length=100)
    addressid = models.IntegerField('地址ID', default=0)
    diskid = models.IntegerField('商户ID', default=0)
    status = models.CharField('状态', max_length=100)
    num = models.IntegerField('数量', default=0)
    isEvaluate = models.IntegerField('是否是当前用户', default=0)

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.orderid


class OrdersMain(models.Model):
    orderid = models.CharField('订单ID', max_length=100)
    totalMoney = models.IntegerField('总价格', max_length=100)
    remarks = models.CharField('备注', max_length=100)
    status = models.CharField('状态', max_length=100)
    isEvaluate = models.IntegerField('是否是当前用户', default=0)
    createtime = models.DateField('创建时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.orderid


class Evaluate(models.Model):
    diskid = models.IntegerField('商户ID', default=0)
    orderid = models.CharField('订单ID', max_length=100)
    openid = models.CharField(max_length=100)
    imgs = models.CharField('用户图片', max_length=100)
    content = models.CharField('评论内容', max_length=100)
    evalValue = models.IntegerField(default=0)
    created = models.DateField('创建时间')
    isAnonymous = models.IntegerField('', default=0)
    nickname = models.CharField('用户名', max_length=100)
    avatarUrl = models.CharField('用户Url', max_length=100)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.diskid
