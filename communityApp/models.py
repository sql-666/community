from django.db import models
import datetime
deadline = datetime.datetime.now()+datetime.timedelta(days=3)

#用户表
class Users(models.Model):
    myid = models.CharField(max_length=50, primary_key=True, verbose_name="ID", null=False)
    name = models.CharField(max_length=50, verbose_name="姓名")
    vatara = models.CharField(max_length=50, null=True)
    community_id = models.CharField(max_length=50,verbose_name="社区ID",null=True)
    age = models.IntegerField(default=0, verbose_name="年龄")
    gender = models.IntegerField(default=0, verbose_name="性别")
    occupation = models.CharField(max_length=50, verbose_name="职业")
    specialty = models.TextField(null=False, verbose_name="特长")
    content = models.TextField(null=False, verbose_name="人物简介")
    contact = models.CharField(max_length=50, verbose_name="联系方式")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    account = models.CharField(max_length=50, verbose_name="账号", null=False, default="0")
    password = models.CharField(max_length=50, verbose_name="密码", null=False, default="0")
    role = models.CharField(max_length=50, verbose_name='角色', default="general_user")
    role_weight = models.IntegerField(default=1, verbose_name="角色权重")
    zupu_key = models.CharField(max_length=100, verbose_name="族谱key", default="0")
    openid =  models.CharField(max_length=100, verbose_name="openid", default="0")
    mate = models.CharField(max_length=50, verbose_name="配偶", default="0")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    # 重定义系统的str方法，让它返回对应的名字
    def __str__(self):
        return self.account

    def user_info(self):
        community = Communities.objects.get(myid=self.community_id,stati__gt=0)
        img= []
        data={
            "myid":self.myid,
            "name":self.name,
            "vatara":self.vatara,
            "community_id":community.name,
            "age":self.age,
            "gender":self.gender,
            "content":self.content,
            "mate":self.mate,
            "img":img
        }
        return data

    class Meta:
        verbose_name_plural = "用户管理"

    def set_community_id(self, id):
        self.community_id=id
        return

    def set_role(self, role, role_weight):
        self.role = role
        self.role_weight = role_weight
        self.save()
        return

    def delete_role(self,role,role_weight):
        self.role=role
        self.role_weight=role_weight
        self.save()
        return

    def enter_community(self, code):
        self.community_id = code
        self.role = "people",
        self.role_weight = 2
        self.save()
        return

    def del_community(self):
        self.role = "general_user"
        self.role_weight = 1
        self.community_id = ""
        self.save()
        return

#社区表
class Communities(models.Model):
    myid = models.CharField(max_length=50, primary_key=True, verbose_name="ID", null=False)
    name = models.CharField(max_length=100, verbose_name="社区名")
    province=models.CharField(max_length=100,null=True, verbose_name="省市")
    address = models.TextField(null=True, verbose_name="地址")
    administrator =  models.ForeignKey(Users, on_delete=models.CASCADE, null=False, related_name="Users_administrator", verbose_name="社区管理人")
    deadline = models.DateTimeField(auto_now_add=True, verbose_name="截止时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    in_code = models.CharField(max_length=100,null=True, verbose_name="邀请码", default="0")
    create_person = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, related_name="Users_create_person", verbose_name="创建人")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    # 重定义系统的str方法，让它返回对应的名字
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "社区管理"

#志愿者表
class Volunteers(models.Model):
    user_info = models.OneToOneField(Users, primary_key=True, on_delete=models.CASCADE, null=False, verbose_name="用户")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    activtiy = models.TextField(null=True, verbose_name="参与活动")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    # 重定义系统的str方法，让它返回对应的名字
    def __str__(self):
        return self.user_info.name
    class Meta:
        verbose_name_plural = "志愿者管理"


#商品分类表
class  Product_type(models.Model):
    myid = models.CharField(max_length=50, primary_key=True, verbose_name="ID", null=False)
    type_name = models.CharField(max_length=50, verbose_name="类型名")
    type_id = models.IntegerField(default=0, verbose_name="类型ID")
    tn = models.CharField(max_length=30, verbose_name="类型英文名", null=True)
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    # 重定义系统的str方法，让它返回对应的名字
    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name_plural = "商品类型管理"

#商品表
class Products(models.Model):
    myid = models.CharField(max_length=50, primary_key=True, verbose_name="ID", null=False)
    title = models.CharField(max_length=200, verbose_name="标题")
    #main_img = models.TextField(null=True)
    #detail_img = models.TextField(null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="价格")
    unit = models.CharField(max_length=26, verbose_name="单位")
    inventory = models.IntegerField(default=1)
    start_price = models.DecimalField(default=0,max_digits=5, decimal_places=2, verbose_name="起卖价")
    type = models.ForeignKey(Product_type, on_delete=models.CASCADE, null=False, verbose_name='类型')
    phone =  models.CharField(max_length=26, verbose_name="号码")
    contact_type = models.CharField(max_length=50,verbose_name="联系方式")
    note = models.TextField(max_length=600, verbose_name="备注", null=True)
    publish_person = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, verbose_name="发布人")
    community = models.ForeignKey(Communities, on_delete=models.CASCADE, null=False, verbose_name="社区")
    get_type = models.CharField(max_length=26, verbose_name="送货方式", default="1")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "商品管理"

    def del_peoduct(self):
        self.stati=0
        self.save()
        return

    #展示商品
    def short_show(self):
        qs_img = Images.objects.filter(product=self, type="proMain")
        img = ""
        if qs_img:
            img = qs_img[0]
        data={}
        data["myid"] = self.myid
        data["title"] = self.title
        data["price"] = self.price
        data["start_price"] = self.start_price
        data["img"] = img
        data["community"] = self.community.name
        data["get_type"] = self.get_type
        return data


#图片表   类型：proMain(商品主图)、proDetail(商品详细图)、activityMain(活动主图)、activityDetail(活动详细图)、
class Images(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    url = models.TextField(null=False, verbose_name="图片路径")
    title = models.TextField(null=False, max_length=100, verbose_name="标题")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=False, verbose_name="商品")
    type = models.CharField(max_length=20, verbose_name="类别", default="proDetail")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "图片管理"

#老人表
class Respects(models.Model):
    myid = models.CharField(max_length=50, primary_key=True, verbose_name="ID", null=False)
    publish_person = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, verbose_name="发布人")
    name = models.CharField(max_length=50, verbose_name="姓名")
    avatar=models.CharField(max_length=50,null=True, verbose_name="头像")
    community = models.ForeignKey(Communities, on_delete=models.CASCADE, null=False, verbose_name="社区")
    age = models.IntegerField(default=0, verbose_name="年龄")
    gender = models.IntegerField(default=0, verbose_name="性别")
    live_situation = models.CharField(max_length=100, verbose_name="居住状态")
    health_situation = models.CharField(max_length=100, verbose_name="身体状态")
    address = models.CharField(max_length=100, verbose_name="住址")
    single=models.CharField(max_length=20, null=True, verbose_name="是否丧偶")
    hobby = models.TextField(max_length=600, null=True, verbose_name="爱好")
    phone = models.CharField(max_length=50,null=True, verbose_name="电话号码")
    families = models.CharField(max_length=50,null=True, verbose_name="紧急联系人")
    family_call = models.CharField(max_length=50, verbose_name="联系人号码")
    note = models.TextField(null=True, verbose_name="备注")
    prove_num = models.IntegerField(default=0, verbose_name="证实数")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "老人管理"

#证实人信息
class Confirm_people(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, verbose_name="用户")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    respect = models.ForeignKey(Respects, on_delete=models.CASCADE, null=False, verbose_name="老人")
    valid = models.BooleanField(default=1, verbose_name="是否合法")


    def __str__(self):
        return (self.respect.name,self.user.name)

    class Meta:
        verbose_name_plural = "证实管理"


#志愿服务队长
class Volun_leader(models.Model):
    user_info = models.OneToOneField(Users, primary_key=True, on_delete=models.CASCADE, null=False,related_name='user_info_User', verbose_name="用户")
    add_person = models.ForeignKey(Users, on_delete=models.CASCADE, null=False,related_name='add_person_User', verbose_name="添加人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    stati =  models.IntegerField(default=0, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    def __str__(self):
        return self.user_info.name

    class Meta:
        verbose_name_plural = "队长管理"

#志愿活动发起表
class Volun_activity(models.Model):
    myid = models.CharField(max_length=50, primary_key=True, verbose_name="ID", null=False)
    title = models.TextField(max_length=600, null=True, verbose_name="标题")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="开始时间")
    end_time = models.DateTimeField(auto_now_add=True, verbose_name="结束时间")
    deadline = models.DateTimeField(default=deadline, verbose_name="报名截止")
    create_person = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, related_name='create_person_VolunLeader', verbose_name="创建人")
    leader = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, related_name='leader_VolunLeader', verbose_name="队长")
    #respects = models.TextField(null=False)
    description = models.TextField(null=True, verbose_name="描述")
    plan = models.TextField(null=False, verbose_name="计划")
    img =  models.TextField(null=True, verbose_name="主图")
    #img_detail = models.TextField(null=True)
    need_number=models.IntegerField(default=1,verbose_name="需要人数")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")
    community=models.ForeignKey(Communities, on_delete=models.CASCADE, null=False, verbose_name="社区")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "志愿活动管理"

    #获取首页简讯
    def Newsletter(self, flag=""):
        data={}
        data["myid"]=self.myid
        data["title"]=self.title
        data["description"]=self.description
        data["img"] = self.img
        return data

    #编辑、添加志愿
    def editInfo(self, info, flag):
        if flag=="add":
            self.myid = info["myid"]
            self.leader = info["leader"]
        self.title = info["title"]
        self.start_time = info["start_time"]
        self.end_time=info["end_time"]
        self.totle_time = info["totle_time"]
        self.create_person = info["create_person"]
        self.respects = info["respects"]
        self.note = info["note"]
        self.plan = info["plan"]
        self.save()
    #用户删除记录
    def delActivity(self):
        pass

    #添加、修改主图
    def addImg(self, img):
        self.img = img
        self.save()

    #更改队长
    def editLeader(self, leader):
        self.leader = leader
        self.save()

    #获得参与活动的老人
    def record(self):
        respects=Activty_respects.objects.filter(activity=self)
        data={
            "title":self.title,
            "community": self.community.name,
            "leader":self.leader.user_info.name,
            "start_time":self.start_time,
            "end_time":self.end_time,
            "respects":respects
        }
        return data


class Applications(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, verbose_name="用户")
    speciality = models.TextField(null=False, verbose_name="特长")
    reason = models.TextField(null=False, verbose_name="原因")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name_plural = "志愿申请"


#参与活动的老人
class Activty_respects(models.Model):
    activity = models.ForeignKey(Volun_activity, on_delete=models.CASCADE, null=False, verbose_name="参与活动")
    respect = models.ForeignKey(Respects, on_delete=models.CASCADE, null=False, verbose_name="老人")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    def __str__(self):
        return self.respect.name

    class Meta:
        verbose_name_plural = "参与活动老人"

#志愿活动详细表
class Volun_activity_d(models.Model):
    activity = models.ForeignKey(Volun_activity, on_delete=models.CASCADE, null=False, verbose_name="活动")
    user_info = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, verbose_name="用户")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    reason = models.TextField(verbose_name="原因",null=True)
    job = models.CharField(max_length=50, verbose_name="工作", null=True)
    my_start_time = models.DateTimeField(auto_now_add=True, verbose_name="我的开始时间")
    my_end_time = models.DateTimeField(auto_now_add=True, verbose_name="我的结束时间")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    def __str__(self):
        return self.activity.title

    def detail(self):
        respects = Activty_respects.objects.filter(activity=self.activity, valid=1)
        data={
            "d":self,
            "respects":respects
        }
        return data

    class Meta:
        verbose_name_plural = "活动详情"


#管理员表
class Administrator(models.Model):
    user_info = models.OneToOneField(Users, primary_key=True,on_delete=models.CASCADE, null=False, verbose_name="用户")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    phone = models.CharField(max_length=50, null=False, verbose_name="手机号")
    community_id = models.IntegerField(default=0, verbose_name="社区号", null=False)
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    def __str__(self):
        return self.user_info.name

    class Meta:
        verbose_name_plural = "社区管理员"

#社区家族表
class Family(models.Model):
    user_info = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, verbose_name="用户")
    community = models.ForeignKey(Communities, on_delete=models.CASCADE, null=False, verbose_name="社区")
    dai_number = models.IntegerField(default=0, verbose_name="代数" ,null=False)
    married = models.IntegerField(default=0, verbose_name="是否婚配")
    mate = models.CharField(max_length=20, null=False, verbose_name="配偶")
    parent = models.CharField(max_length=50, null=False, verbose_name="父母")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    def __str__(self):
        return self.user_info.name

    class Meta:
        verbose_name_plural = "家族家族"

#         族谱架构表
# class zupu()


#权限表
class Authority(models.Model):
    myid = models.CharField(max_length=50, primary_key=True, verbose_name="ID", null=False)
    title = models.CharField(max_length=50, verbose_name="标题")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "权限管理"

#角色表
class Role(models.Model):
    myid = models.CharField(max_length=50, primary_key=True, verbose_name="ID", null=False)
    title = models.CharField(max_length=50, verbose_name="标题")
    name = models.CharField(max_length=50, verbose_name="英文名",default="")
    authority = models.TextField(max_length=100, verbose_name="权限")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "角色管理"

#家族代数
class zupu_level(models.Model):
    myid = models.CharField(max_length=50, primary_key=True, verbose_name="ID", null=False)
    community = models.ForeignKey(Communities, on_delete=models.CASCADE, null=False, verbose_name="社区")
    level_key =  models.CharField(max_length=50, verbose_name="族谱key")
    name = models.CharField(max_length=50, verbose_name="标题")
    dai = models.IntegerField(default=1, verbose_name="代数")
    create_person =  models.ForeignKey(Users, on_delete=models.CASCADE, null=False, verbose_name="创建人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")
    def __str__(self):
        return self.dai

    def get_subords(self):
        qs=zupu_relationship.objects.filter(dai=self,stati__gt=0)
        parent=[]
        for item in qs:
            if not item.parent in parent:
                parent.append(item.parent)
        page=[]
        for item_zi in parent:
            er=list(zupu_relationship.objects.filter(dai=self,parent=item_zi,stati__gt=0).values('name',"myid").order_by('xh'))
            if er:
                page=page+er
        return  {"subords":page}

#未注册/过世人员
class zupu_people(models.Model):
    myid = models.CharField(max_length=50, primary_key=True, verbose_name="ID", null=False)
    community = models.ForeignKey(Communities, on_delete=models.CASCADE, null=False, verbose_name="社区")
    avatara = models.CharField(max_length=100, verbose_name="头像")
    zupu_key = models.CharField(max_length=100, verbose_name="族谱key")
    name = models.CharField(max_length=100, verbose_name="姓名")
    gender = models.IntegerField(default=0, verbose_name="性别")
    imgs = models.TextField(max_length=100, verbose_name="相关图片")
    content = models.TextField(max_length=100, verbose_name="人物简介")
    age = models.IntegerField(default=0, verbose_name="年龄")
    mate = models.IntegerField(default=0, verbose_name="状态")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")

    def __str__(self):
        return self.name

#族谱关系
class zupu_relationship(models.Model):
    myid = models.CharField(max_length=50, primary_key=True, verbose_name="ID", null=False)
    dai = models.ForeignKey(zupu_level, on_delete=models.CASCADE, null=False, verbose_name="代数")
    # dai = models.IntegerField(default=0, verbose_name="代数")
    xh =  models.IntegerField(default=1, verbose_name="排序")
    parent = models.CharField(max_length=100, verbose_name="父辈ID")
    name = models.CharField(max_length=100, verbose_name="名称", null=True)
    info = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name="详细信息")
    # children = models.TextField(max_length=200, verbose_name="孩子ID")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", null=True)
    community = models.ForeignKey(Communities, on_delete=models.CASCADE, null=False, verbose_name="社区")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")
    def __str__(self):
        return self.name

    def connect(self,obj):
        self.info = obj
        self.save()
        return

    def set_name(self, name):
        self.name=name
        self.save()

    def change_stati(self, value):
        self.stati=value
        self.save()

    def short_show(self):
        children = zupu_relationship.objects.filter(parent=self.myid, stati__gt=0).order_by("create_time")
        new_children=[]
        for item in children:
            temp = item.short_show()
            new_children.append(temp)
        if  self.info:
            name = self.info.name
        else:
            name = ""
        data={
            "dai":self.dai.dai,
            "name":self.name,
            "myid":self.myid,
            "xh":self.xh,
            "info":name,
            "children":new_children
        }
        return data

class Children(models.Model):
    parent=models.ForeignKey(zupu_relationship, on_delete=models.CASCADE, null=False, verbose_name="父亲ID",related_name="father")
    child = models.ForeignKey(zupu_relationship, on_delete=models.CASCADE, null=False, verbose_name="孩子ID",related_name="child")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    stati = models.IntegerField(default=1, verbose_name="状态")
    valid = models.BooleanField(default=1, verbose_name="是否合法")
    def short_show(self):

        data={
            "dai":self.child.dai.dai,
            "name":self.child.name,
            "myid":self.child.myid,
            "xh": self.child.xh
        }
        return data













