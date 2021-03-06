from django.db import models
import random



class asset(models.Model):

    MANAGER_CHOICES=(
        ('何全','何全'),
        ('其他','其他'),
    )
    PROJECT_CHOICES=(
        ('项目1','项目1'),
        ('项目2', '项目2'),
        ('项目3', '项目3'),
        ('其他', '其他')
    )

    hostname = models.CharField(max_length=64, verbose_name='主机名',unique=True)
    network_ip = models.GenericIPAddressField(verbose_name='外网IP', null=True,blank=True)
    inner_ip = models.GenericIPAddressField(verbose_name='内网IP', null=True, blank=True)


    system = models.CharField(max_length=128,verbose_name='系统版本',null=True,blank=True)
    cpu = models.CharField(max_length=64,verbose_name='CPU',null=True,blank=True)
    memory = models.CharField(max_length=64, verbose_name='内存', null=True,blank=True)
    disk = models.CharField(max_length=256,verbose_name="硬盘",null=True,blank=True)
    bandwidth = models.IntegerField(verbose_name='带宽', null=True,blank=True,default="1")


    platform = models.ForeignKey(max_length=128, to="platform",on_delete=models.SET_NULL,null=True, verbose_name='平台')
    region = models.ForeignKey(max_length=256,to="region",on_delete=models.SET_NULL,null=True,verbose_name="区域",)

    manager = models.CharField(max_length=128, choices=MANAGER_CHOICES, verbose_name='负责人')
    project = models.CharField(max_length=128, choices=PROJECT_CHOICES, verbose_name='项目')

    user = models.ForeignKey(verbose_name="登录用户",to='asset_user',on_delete=models.SET_NULL,null=True, blank=True)

    Instance_id = models.CharField(max_length=64, verbose_name='实例ID', null=True, blank=True)
    buy_time = models.DateTimeField(verbose_name='购买时间',null=True, blank=True)
    expire_time = models.DateTimeField(verbose_name='到期时间',null=True, blank=True)
    ps = models.CharField(max_length=1024,verbose_name="备注",null=True,blank=True)
    port = models.IntegerField(verbose_name="登录端口",default='22',null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=('激活'))

    ctime= models.DateTimeField(auto_now_add=True,null=True,verbose_name='创建时间',blank=True)
    utime = models.DateTimeField(auto_now=True, null=True,verbose_name='更新时间',blank=True)

    class  Meta:
        db_table ="asset"
        verbose_name="资产管理"
        verbose_name_plural = '资产管理'
        permissions = {
            ('read_asset',u"只读资产管理"),
        }


    def __str__(self):
        return self.hostname


#平台
class platform(models.Model):
    name = models.CharField(max_length=30)


    class  Meta:
        db_table ="platform"
        verbose_name="云平台管理"
        verbose_name_plural = '云平台管理'

    def __str__(self):
        return self.name

#区域
class region(models.Model):
    name = models.CharField(max_length=40)
    platforms = models.ForeignKey(platform,on_delete=models.SET_NULL,null=True,)

    class  Meta:
        db_table ="region"
        verbose_name="云区域管理"
        verbose_name_plural = '云区域管理'


    def __str__(self):
        return self.name










##登录用户
class  asset_user(models.Model):
    hostname = models.CharField(max_length=64, verbose_name='名称', unique=True)
    username = models.CharField(max_length=64, verbose_name="用户名", default='root', null=True, blank=True)
    password = models.CharField(max_length=256, blank=True, null=True, verbose_name=('密码'))
    private_key = models.FileField(upload_to = 'upload/private_key/%Y%m%d_{}'.format(random.randint(0,99999)),verbose_name="私钥",null=True,blank=True)

    ps = models.CharField(max_length=10240, verbose_name="备注", null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', blank=True)
    utime = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间', blank=True)

    class  Meta:
        db_table ="asset_user"
        verbose_name="资产用户"
        verbose_name_plural = '资产用户'
        permissions = {
            ('read_asset_user',u"只读资产用户"),
        }

    def __str__(self):
        return self.username
