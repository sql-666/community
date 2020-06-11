from . import models
import datetime
from communityApp.tools import number
now_time = datetime.datetime.now()

def model_data():
   #User:
    user = models.Users.objects.create(
        myid=number.get_id("user"),
        name="Victroy",
        community_id = "",
        age = 20,
        gender = 1,
        occupation = "学生",
        specialty = "打代码",
        content = "我是一个好女孩",
        contact = "18293876721",
        create_time = now_time,
        vatara="images/smile.jpg"
    )

   # Communities
    community = models.Communities.objects.create(
        myid=number.get_id("community"),
        name="社区1",
        address="xx省xx市",
        administrator=user,
        deadline=now_time,
        create_time=now_time,
        create_person=user,
        province="广东肇庆"

    )

    #Volunteers
    volunteer=models.Volunteers.objects.create(
        user_info=user,
        create_time = now_time,
        activtiy = ""
    )

    #ProductType
    product_type=models.Product_type.objects.create(
        myid=number.get_id("product_type"),
        type_name = "肉类",
        type_id = 2001
    )

    # Products(models.Model):
    product = models.Products.objects.create(
        myid = number.get_id("product"),
        title = "本地土鸡",
        price = 20.01,
        unit = "只",
        inventory = 20,
        start_price = 10.01,
        type = product_type,
        contact = "78932786122",
        contact_type = "手机联系",
        note = "",
        publish_person = user,
        community =community
    )

    # Respects
    respect = models.Respects.objects.create(
        myid = number.get_id("respect"),
        publish_person = user,
        name = "老人1",
        community = community,
        age = 88,
        gender = 1,
        live_situation = "夫妻居住",
        health_situation = "身体良好",
        address = "xx镇",
        hobby = "",
        phone = "28937465321",
        families = "",
        family_call = "89374856321",
        note = "",
        create_time = now_time
    )

    #volun_leader
    volun_leader=models.Volun_leader.objects.create(
        user_info = user,
        add_person = user,
        create_time = now_time
    )

    #Volun_activity
    volun_activity=models.Volun_activity.objects.create(
        myid=number.get_id("volun_activity"),
        title = "共度重阳",
        create_time = now_time,
        start_time = now_time,
        end_time = now_time,
        create_person = volun_leader,
        leader = volun_leader,
        description = "",
        img = "images/spellGroup.jpg",
        plan = "计划1",
        community=community
    )

    #VolunActivityD
    volun_activity_d=models.Volun_activity_d.objects.create(
        activity = volun_activity,
        user_info = user,
        create_time = now_time,
        reason = "原因1",
        job = "后勤",
        my_start_time = now_time,
        my_end_time = now_time
    )
    #activity_respect
    activity_respect=models.Activty_respects.objects.create(
        activity = volun_activity,
        respect = respect
    )
    #administrator
    # administrator=models.administrator.objects.create(
    #     myid = user,
    #     create_time = now_time,
    #     phone = "83943434332",
    #     community_id = "2001"
    # )

    #Family
    family=models.Family.objects.create(
        user_info = user,
        community = community,
        dai_number = 2,
        married = 1,
        mate = "xxx",
        parent = ""
    )

    #Authority
    authority=models.Authority.objects.create(
        myid = number.get_id("authority"),
        title = "编辑"
    )

    #Role
    role = models.Role.objects.create(
        myid = number.get_id("role"),
        authority = "001,002",
        title = "管理员"
    )

    #Images
    image =  models.Images.objects.create(
        url = "images/mouse.jpg",
        title = "本地鸡",
        type = "proMain",
        product = product
    )

