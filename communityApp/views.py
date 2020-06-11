from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .import init_data as myinit
from .import models
from communityApp.tools import msg, encrype, number, decorator, data_format, func
from django.contrib import admin
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json

admin.site.site_header = '社区后台管理'
admin.site.site_title = '社区后台管理平台'


def send_sms(phone_numbers, code):
    '''
    发送验证码
    :param phone_numbers: 手机号
    :param code: 验证码
    :return response: 
    '''
    client = AcsClient('', '', '')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('', "")

    # 手机号码，多个号码用英文的逗号分隔开
    # 例如：phone_numbers = '17612835052,15889923535'
    request.add_query_param('PhoneNumbers', phone_numbers)

    request.add_query_param('SignName', "农村社区管理平台")
    request.add_query_param('', "")

    # 验证码, json 格式
    template_param = "{'code': %s }" % code
    request.add_query_param('TemplateParam', template_param)

    response = client.do_action(request)

    return response



def phone_code(request):
    '''
    验证码
    :param request:
    :return msg: 状态信息
    '''
    if request.method == "POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        if len(info_dict["account"])==11:
            code = number.get_id("phone_code")
            request.session["phone_code"] = code
            send_sms(info_dict["account"],code)
            return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))


def init_data(request):
    '''初始数据，用于测试
    :param request:
    :return msg:
    '''
    for item in range(0,10):
        res = models.Users.objects.create(
            myid=number.get_id("user"),
            account="1588992350"+str(item),
            password="e6464745cdb5612d3c2bba55f9a4140e"
        )
    return JsonResponse(msg.table("success"))

def login(request):
    '''
    登录
    :param request
    :return msg/login.html
    '''
    if (request.method=="POST"):
        info_dict = json.loads(request.body.decode('utf-8'))
        user=models.Users.objects.filter(account=info_dict["username"], valid=1)
        password = encrype.password(info_dict["password"])
        # password = "6e0036d0716d3f528f46d86d5ac4e2ff"
        if user and user[0].password == password:
            request.session['community_username'] = info_dict["username"]
            request.session['community_password'] = password
            return JsonResponse(msg.table("success"))
        else:
            return JsonResponse(msg.table("error"))
    else:
        return render(request, 'font/login.html')

@decorator.log_in
def enter_community(request):
    '''
    凭借社区码加入社区
    :param request: 
    :return enter_community.html/msg: 
    '''
    if request.method == "GET":
        return render(request, 'font/enter_community.html')
    elif request.method == "POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        account = request.session["community_username"]
        user = models.Users.objects.get(account=account)
        if not user.community_id:
            community=models.Communities.objects.filter(in_code=info_dict["community_code"],stati=1, valid=1)
            if community:
                user.enter_community(community[0].myid)
                return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))

@decorator.log_in
def create_community(request):
    if request.method == "GET":
        return render(request, 'font/create_community.html')
    if request.method == "POST":
        now_account = request.session["community_username"]
        user = models.Users.objects.get(account=now_account)
        if user.community_id:
            return JsonResponse(msg.table("error"))
        info_dict = json.loads(request.body.decode('utf-8'))
        if now_account != info_dict[3]["value"]:
            JsonResponse(msg.table("wrong_account"))
        if data_format.auth(info_dict):
            user = models.Users.objects.get(account=now_account)
            community = models.Communities.objects.filter(create_person=user, valid=1)
            name_repeat = models.Communities.objects.filter(name=info_dict[0]["value"], valid=1)
            if not community and not name_repeat:
                res = models.Communities.objects.create(
                    myid = number.get_id("community"),
                    create_person=user,
                    name=info_dict[0]["value"],
                    administrator=user,
                    province=info_dict[1]["value"],
                    address=info_dict[2]["value"],
                    in_code=number.get_id("in_code")
                )
                user.set_community_id(id=res.myid)
                user.set_role("administrator",5)
                user.save()
                return JsonResponse(msg.table("success"))
            else:
                return JsonResponse(msg.table("repeat"))

    return JsonResponse(msg.table("error"))

@decorator.log_in
def index(request):
    '''首页
    :param request:
    :return index.html，func，activity, index_pro
    '''
    func = data_format.page("index")

    activity={}
    activity_first = models.Volun_activity.objects.filter(stati=3, valid=1)
    user = models.Users.objects.get(account=request.session["community_username"], valid=1)
    if not user.community_id:
        return render(request, 'font/index.html')
    if activity_first:
        activity = activity_first[0].Newsletter()
    query_pro = models.Products.objects.filter(valid=1)[0:6]
    index_pro = []
    for obj in query_pro:
        proItem = obj.short_show()
        # product = list(models.Images.objects.filter(product=obj))
        # proItem["img"] = product
        index_pro.append(proItem)
    con = {}
    con["newsletter"] = activity
    con["indexPro"] = index_pro

    return render(request, 'font/index.html', {"func":func,"activity":activity,"index_pro":index_pro, "user":user})

@decorator.log_in
def help_respects(request):
    page_id = int(request.GET.get('page_id'))
    snum = (page_id - 1) * 10
    enum = page_id * 10
    respects=models.Respects.objects.filter(valid=1)[snum:enum]
    po = False
    user = models.Users.objects.get(account=request.session['community_username'], valid=1, stati__gt=0)
    if func.auth_role(func.role_weight("leader"), user.role_weight):
        po=True
    return render(request, 'font/help_respects.html', {"respects":respects,"po":po})

@decorator.log_in
def respects_detail(request):
    respectsD={}
    if request.method == "GET":
        respect_id=request.GET.get("respect_id")
        respectsD = models.Respects.objects.get(myid=respect_id, valid=1)
        confirm_num = models.Confirm_people.objects.filter(respect=respectsD, valid=1).count()
        is_prove = models.Confirm_people.objects.filter(respect=respectsD, valid=1).exists()
    return render(request, 'font/respects_detail.html', {"respectsD": respectsD,"is_prove":is_prove,"confirm_num":confirm_num})

@decorator.log_in
def confirm_respect(request):
    if request.method == "POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        user = models.Users.objects.get(account=request.session['community_username'], valid=1)
        respect = models.Respects.objects.get(myid=info_dict["respect_id"], valid=1)
        isconfirm= models.Confirm_people.objects.filter(user=user, respect=respect, valid=1)
        if not isconfirm:
            res=""
            res=models.Confirm_people.objects.create(
                user=user,
                respect=respect
            )
            if res:
                return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))


@decorator.log_in
def add_respect(request):
    if request.method == "POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        publish_person=models.Users.objects.get(account=request.session.get("community_username"), valid=1)
        community=models.Communities.objects.get(myid=publish_person.community_id, valid=1)
        res=models.Respects.objects.create(
            myid=number.get_id("respect"),
            name=info_dict["name"],
            age = info_dict["age"],
            gender=info_dict["gender"],
            single=info_dict["single"],
            live_situation=info_dict["live_situation"],
            health_situation=info_dict["health_situation"],
            phone = info_dict["phone"],
            families=info_dict["families"],
            note=info_dict["note"],
            address=info_dict["address"],
            hobby=info_dict["hobby"],
            avatar='images/respect5.jpg',
            # families=families
            publish_person= publish_person,
            community=community
        )
        if res:
            return JsonResponse(msg.table("success"))
        else:
            return JsonResponse(msg.table("error"))
    elif request.method == "GET":
        aRespect={}
        return render(request, 'font/add_respect.html', {"aRespect":aRespect})
    return render(request, 'font/add_respect.html')

@decorator.log_in
def volunteers(request):
    activities=[]
    if request.method == "GET":
        click_type = request.GET.get("type")
        page_id = int(request.GET.get("page_id"))
        if page_id > 0:
            start_num = (page_id-1)*10
            end_num = page_id*10
        else:
            end_num=None
            start_num=-10
        user_info = models.Users.objects.get(account=request.session['community_username'], valid=1)
        btn=True
        if user_info.role_weight>=3:
            btn = False
        totle_page=1
        if click_type=="all":
            activities_temp = models.Volun_activity.objects.filter(valid=1)
            totle_page = int(len(activities_temp)/10)+1
            activities = activities_temp[start_num:end_num]
        elif  click_type=="active":
            activities_temp = models.Volun_activity.objects.filter(stati=1, valid=1)[start_num:end_num]
            totle_page = int(len(activities_temp)/10)+1
            activities = activities_temp[start_num:end_num]
        elif click_type=="deadline":
            activities_temp = models.Volun_activity.objects.filter(stati=2, valid=1)[start_num:end_num]
            totle_page = int(len(activities_temp)/10)+1
            activities = activities_temp[start_num:end_num]
        else:
            activities_temp = models.Volun_activity.objects.filter(stati=3, valid=1)[start_num:end_num]
            totle_page = int(len(activities_temp)/10)+1
            activities = activities_temp[start_num:end_num]
        return render(request, 'font/volunteers.html', \
                      {"activities": activities, "type":click_type, \
                       "btn":btn, "page_id":request.GET.get("page_id"),"totle_page":totle_page})
    return JsonResponse(msg.table("error"))

@decorator.log_in
def application(request):
    user_info = models.Users.objects.get(account=request.session['community_username'],valid=1)
    if request.method == "GET":
        return render(request, 'font/application.html', {"user_info":user_info})
    elif request.method == "POST":
        app_dict = json.loads(request.body.decode('utf-8'))
        if user_info.role_weight < 3:
            models.Applications.objects.create(
                user = user_info,
                speciality=app_dict['spe'],
                reason=app_dict['reason']
            )
            user_info.set_role("volunteer", 3)
            return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))



@decorator.log_in
def volunteer_card(request):
    user_info={}
    return render(request, 'font/volunteer_c.html', {"user_info":user_info})

@decorator.log_in
def activity_d(request):
    if request.method=="GET":
        activity_id = request.GET.get('activity_id')
        type = request.GET.get('type',"")
        user_info = models.Users.objects.get(account=request.session['community_username'], valid=1)
        activity = models.Volun_activity.objects.filter(myid=activity_id, valid=1)[0]
        if type != "join":
            members = models.Volun_activity_d.objects.filter(activity=activity, valid=1)
            join = models.Volun_activity_d.objects.filter(activity=activity,user_info=user_info,valid=1).exists()

            nojoin = not join
            isFull = False
            if len(members)==activity.need_number:
                isFull=True
            return render(request, 'font/activity_d.html',
                          {"activityD": activity, "members": members, "nojoin": nojoin,"full":isFull})
        elif type == "join":
            models.Volun_activity_d.objects.create(
                activity=activity,
                user_info=user_info,
                reason="原因1",
                job="工作1"
            )
        return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))

@decorator.log_in
def activity_l(request):
    page = int(request.GET.get('page'))
    snum = (page-1)*10
    enum = page*10
    queryL = models.Volun_activity.objects.filter(stati=3, valid=1)[snum:enum]
    L=[]
    for item in queryL:
        data=item.Newsletter()
        L.append(data)
    return render(request, 'font/activity_l.html', {"L":L})

@decorator.log_in
def product_d(request):
    pro_id=request.GET.get('pro_id')
    productD=models.Products.objects.get(myid=pro_id, valid=1)
    imgs = models.Images.objects.filter(product=productD,type="proMain", valid=1).values("url")
    dets = models.Images.objects.filter(product=productD,type="proDet", valid=1).values('url')
    return render(request, 'font/product_d.html', {"productD": productD, "imgs":imgs, "dets":dets})

@decorator.log_in
def user(request):
    user_info={}
    user_info = models.Users.objects.get(account=request.session["community_username"], valid=1)
    funcList=data_format.page("user",user_info.role_weight)
    if user_info.community_id:
        community = models.Communities.objects.get(myid = user_info.community_id)
    return render(request, 'font/user.html', {"user_info": user_info,"funcList":funcList, "in_code":community.in_code})

@decorator.log_in
def product(request):
    if request.method == "GET":
        type = request.GET.get("type")
        con = request.GET.get("con","")
        page_id = 1
        if page_id > 0:
            start_num = (page_id - 1) * 10
            end_num = page_id * 10
        if type =="all":
            qs_products = models.Products.objects.filter(valid=1,title__icontains=con)
        else:
            type_obj = models.Product_type.objects.get(tn=type)
            qs_products = models.Products.objects.filter(type=type_obj,valid=1,title__icontains=con)

        products = qs_products[start_num:end_num]
        new_products=[]
        for item  in  products :
            new_products.append(item.short_show())
        totle_page = len(qs_products)
        type_list = models.Product_type.objects.all()
        print(type_list)
    return render(request, 'font/product.html', {"products": new_products, \
                                                 "totle_page":str(totle_page), \
                                                 "type":type, "type_list":type_list })

@decorator.log_in
def edit_product(request):
    user = models.Users.objects.get(account=request.session["community_username"])
    if not func.auth_role(func.role_weight("people"), user.role_weight):
        return msg.table("no_authority")

    if request.method == "GET":
        type = request.GET.get("type")
        if type == "del":
            pro_id = request.GET.get("pro_id")
            opr_product = models.Products.objects.get(myid=pro_id)
            opr_product.stati=0
            opr_product.save()
            return JsonResponse(msg.table("success"))
        elif type == "edit":
            pro_id = request.GET.get("pro_id")
            opr_product = models.Products.objects.get(myid=pro_id)
            return render(request, 'font/edit_product.html',{"product":opr_product, "type":"edit"})
        elif type == "new":
            return render(request, 'font/edit_product.html', {"product": {}, "type":"new"})


    elif request.method == "POST":
        type = request.GET.get("type")
        info_dict = json.loads(request.body.decode('utf-8'))
        if data_format.auth(info_dict):
            this_type = models.Product_type.objects.get(type_id=info_dict[5]["value"])
            if type =="new":
                models.Products.objects.create(
                    myid = number.get_id("product"),
                    title = info_dict[0]["value"],
                    price=info_dict[1]["value"],
                    unit=info_dict[2]["value"],
                    inventory=info_dict[3]["value"],
                    start_price=info_dict[4]["value"],
                    type=this_type,
                    phone=info_dict[6]["value"],
                    get_type=info_dict[7]["value"],
                    note=info_dict[8]["value"],
                    publish_person=user,
                    community=models.Communities.objects.get(myid=user.community_id)
                )
                return JsonResponse(msg.table("success"))
            elif type =="edit":
                pro_id = request.GET.get("pro_id")
                opr_product = models.Products.objects.get(myid=pro_id)
                opr_product.title=info_dict[0]["value"],
                opr_product.price=info_dict[1]["value"],
                opr_product.unit=info_dict[2]["value"],
                opr_product.inventory=info_dict[3]["value"],
                opr_product.start_price=info_dict[4]["value"],
                opr_product.type=this_type,
                opr_product.phone=info_dict[6]["value"],
                opr_product.get_type=info_dict[7]["value"],
                opr_product.note=info_dict[8]["value"]
                opr_product.save()
                return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))

@decorator.log_in
def edit_user_info(request):
    if request.method == "GET":
        user_info = models.Users.objects.filter(account=request.session["community_username"], valid=1)
        return render(request, 'font/edit_user_info.html',{"user_info":user_info[0]})
    if request.method == "POST":
        data_dict = json.loads(request.body.decode('utf-8'))
        user = models.Users.objects.filter(account=request.session["community_username"], valid=1)
        if user:
            res=user.update(
                name=data_dict["name"],
                occupation=data_dict["occupation"],
                specialty=data_dict["specialty"],
                content=data_dict["content"],
                gender = data_dict["gender"],
                age = data_dict["age"]
            )
            if res == 1:
                return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))

@decorator.log_in
def my_need(request):
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
    return render(request, 'font/my_need.html')


@decorator.log_in
def volunteer_d(request):
    user = models.Users.objects.get(account = request.session["community_username"])
    activities=models.Volun_activity_d.objects.filter(user_info=user, valid=1)
    re = []
    for item in activities:
        re.append(item.detail())
    return render(request, 'font/volunteer_d.html',{"items":re})

@decorator.log_in
def m_volunteer(request):
    user = models.Users.objects.get(account = request.session["community_username"])
    auth_res=func.auth_role(func.role_weight("leader"),user.role_weight)
    if not auth_res:
        return JsonResponse(msg.table("no_authority"))
    if request.method=="GET":
        type = request.GET.get("type","")
        flag = request.GET.get("flag","")
        if type=="edit":
            volunteer_id=request.GET.get("volunteer_id")
            this_volunteer=models.User.objects.get(myid=volunteer_id)
            this_volunteer.role="people"
            this_volunteer.save()
            return JsonResponse(msg.table("success"))
        else:
            volunteers = models.Users.objects.filter(role="volunteer", stati__gt=0, valid=1)
            return  render(request, 'font/m_volunteer.html',{"items":volunteers,"flag":flag})
    if  request.method=="POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        volunteer = models.Users.objects.get(myid=info_dict["myid"])
        if info_dict["flag"]=="volunteer":
            volunteer.delete_role("people",2)
            return JsonResponse(msg.table("success"))
        if info_dict["flag"]=="leader":
            volunteer.set_role("volunteer", 3)
            return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))


@decorator.log_in
def my_product(request):
    user = models.Users.objects.get(account=request.session["community_username"])
    if request.method=="GET":
        items = models.Products.objects.filter(publish_person=user, stati__gt=0, valid=1)
        my_proucts=[]
        for item in items:
            my_proucts.append(item.short_show())
        return render(request, 'font/my_product.html',{"my_proucts":my_proucts})
    elif request.method=="POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        if info_dict["type"] == "del":
            product=models.Products.objects.get(myid=info_dict["myid"])
            product.del_peoduct()
            return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))

@decorator.log_in
def edit_my_product(request):
    myproduct={}
    imgs=['1','2']
    return render(request, 'font/edit_my_product.html', {"myproduct":myproduct, 'imgs':imgs})

@decorator.log_in
def del_people(request):
    user = models.Users.objects.get(account=request.session["community_username"])
    auth_res = func.auth_role(func.role_weight("administrator"), user.role_weight)
    if not auth_res:
        return JsonResponse(msg.table("no_authority"))
    if request.method == "GET":
        adm = models.Communities.objects.filter(myid=user.community_id, stati__gt=0, valid=1)
        if adm:
            people = models.Users.objects.filter(community_id=adm[0].myid, role_weight__lt=5,stati__gt=0, valid=1)
            return render(request, 'font/del_people.html', {"items":people})
    elif request.method == "POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        del_people = models.Users.objects.get(myid=info_dict["myid"],role_weight__lt=5)
        del_people.del_community()
        return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))

@decorator.log_in
def check_people(request):
    items=['1','2']
    return render(request, 'font/check_people.html',{"items":items})

@decorator.log_in
def add_vol_activity(request):
    items=['1','2']
    return render(request, 'font/add_vol_activity.html', {"items":items})

@decorator.log_in
def end_activity(request):
    items=['1','2']
    return render(request, 'font/end_activity.html', {"items":items})

@decorator.log_in
def add_activity_d(request):
    if request.method == "GET":
        return render(request, 'font/add_activity_d.html')
    elif request.method == "POST":
        user = models.Users.objects.get(account=request.session["community_username"], valid=1)
        community = models.Communities.objects.get(myid=user.community_id, valid=1)
        info_dict = json.loads(request.body.decode('utf-8'))
        models.Volun_activity.objects.create(
            myid=number.get_id("volun_activity"),
            title=info_dict["title"],
            description=info_dict["description"],
            need_number=info_dict["need_people"],
            # start_time = info_dict["start_time"],
            # end_time = info_dict["start_time"],
            # deadline=info_dict["deadline"],
            plan=info_dict["plan"],
            create_person = user,
            leader=user,
            community=community,
        )
        return JsonResponse(msg.table("success"))

@decorator.log_in
def m_activity(request):
    account = request.session["community_username"]
    if request.method=="GET":
        user = models.Users.objects.get(account=account, valid=1)
        if user.role_weight<5:
            activities = models.Volun_activity.objects.filter(create_person=user, stati__gt=0, valid=1)
        elif user.role_weight==5:
            activities = models.Volun_activity.objects.filter(stati__gt=0, valid=1)
        return render(request, 'font/m_activity.html',{"activities":activities})
    return JsonResponse(msg.table("success"))

def register(request):
    if request.method == "POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        if info_dict["captcha"] != request.session["phone_code"]:
            return JsonResponse(msg.table("error_code"))
        user = models.Users.objects.filter(account=info_dict["username"], valid=1)

        if not user:
            password=encrype.password(info_dict["password"])
            res=models.Users.objects.create(
                myid = number.get_id("user"),
                account=info_dict["username"],
                password=password
            )
            # 记住我
            # if info_dict["remember"]:
            #     request.session.set_expiry(50000)
            return JsonResponse(msg.table("success"))
        else:
            return JsonResponse(msg.table("repeat"))
    elif request.method == "GET":
        return render(request, 'font/register.html')
    return JsonResponse(msg.table("error"))

def mycommunity(request):
    '''
    我的社区
    :param request: 
    :return: 
    '''
    now_account = request.session["community_username"]
    if request.method == "GET":
        user = models.Users.objects.get(account=now_account, valid=1)
        mycommunity = models.Communities.objects.get(myid=user.community_id)
        people = models.Users.objects.filter(community_id=user.community_id)
        return render(request, 'font/mycommunity.html', {"mycommunity":mycommunity, "people":people})
    if request.method == "POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        if now_account != info_dict[1]["value"]:
            JsonResponse(msg.table("wrong_account"))
        if data_format.auth(info_dict):
            user = models.Users.objects.get(account=now_account)
            community = models.Communities.objects.fillter(create_person=user, valid=1)
            name_repeat = models.Communities.objects.fillter(name=info_dict[0]["value"], valid=1)
            if not community and not name_repeat:
                res = ""
                res=models.Communities.objects.create(
                    create_person=user,
                    name = info_dict[0]["value"],
                    administrator=user,
                    province=info_dict[1]["value"],
                    address=info_dict[2]["value"],
                    in_code=number.get_id("in_code"),
                )
                if not res:
                    JsonResponse(msg.table("success"))
            return JsonResponse(msg.table("repeat"))
    return JsonResponse(msg.table("error"))


def people_l(request):
    user = models.Users.objects.get(account=request.session["community_username"])
    auth_res = func.auth_role(func.role_weight("administrator"), user.role_weight)
    if not auth_res:
        return JsonResponse(msg.table("no_authority"))
    if request.method == "GET":
        flag = request.GET.get("flag", "")
        adm = models.Communities.objects.filter(myid=user.community_id, stati__gt=0, valid=1)
        if adm:
            if flag=="volunteer":
                people = models.Users.objects.filter(community_id=adm[0].myid, role_weight=3, stati__gt=0, valid=1)
            elif flag=="leader":
                people = models.Users.objects.filter(community_id=adm[0].myid, role_weight=4, stati__gt=0, valid=1)
            return render(request, 'font/people_l.html', {"items": people})
    elif request.method == "POST":
        return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))


def get_code(request):
    appid = ''
    secret = ''
    info_dict = json.loads(request.body.decode('utf-8'))
    js_code = info_dict["code"]
    grant_type = 'authorization_code'
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + js_code + '&grant_type=authorization_code'
    r = request.get(url)
    result = r.json()
    openid = result['openid']
    res = msg.table("success")["openid"]=openid
    return JsonResponse(res)

def xlogin(request):
    '''
    小程序登录
    :param request: 
    :return: msg
    '''
    info_dict = json.loads(request.body.decode('utf-8'))
    hash_password = encrype.password(info_dict["password"])
    user = models.Users.objects.filter(account=info_dict["account"], password=hash_password)
    if user:
        msg.table("success")["openid"]="6e0036d0716d3f528f46d86d5ac4e2ff"
        return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))

def zupu_connet(request):
    '''
    族谱关联个人
    :param request: 
    :return: 
    '''
    if request.method == "POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        user = models.Users.objects.get(openid=info_dict["openid"])
        if func.auth_role(func.role_weight("zupu"), user.role_weight):
            zupu_user = models.zupu_relationship.objects.get(myid=info_dict["zupu_id"])
            r_user = models.Users.objects.get(myid=info_dict["user_id"])
            qs_user = models.zupu_relationship.objects.filter(info=r_user, stati=1)
            if not qs_user:
                zupu_user.connect(r_user)
                return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))
def zupu_dai(request):
    '''
    编辑代数
    :param request: 
    :return: 
    '''
    if request.method == "GET":
        openid = request.GET.get("openid", "")
        user = models.Users.objects.get(openid=openid)
        community = models.Communities.objects.filter(myid=user.community_id)
        if not community:
            return JsonResponse(msg.table("error"))
        else:
            community = community[0]
        if func.auth_role(func.role_weight("people"), user.role_weight):
            dai = list(models.zupu_level.objects.filter(community=community).order_by("dai"))
            dai_list=[]
            for item in dai:
                sub = item.get_subords()
                dai_list.append({"dai":item.dai,"fid":item.myid,"name":item.name,"degs":0,"subords":sub["subords"]})
            res=msg.table("success")
            res["zupu"]=dai_list
            if func.auth_role(func.role_weight("administrator"), user.role_weight):
                res["flag"] = True
            return  JsonResponse(res)
        return JsonResponse(msg.table("error"))
    if request.method == "POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        user = models.Users.objects.get(openid=info_dict["openid"])
        community = models.Communities.objects.filter(myid=user.community_id)
        if not community:
            return JsonResponse(msg.table("error"))
        del info_dict["openid"]
        if func.auth_role(func.role_weight("administrator"),user.role_weight):

            for dai, name in info_dict.items():

                qs_dai = models.zupu_level.objects.filter(dai = dai,community = community[0])
                if qs_dai:
                    qs_dai[0].name=name
                    qs_dai[0].save()

                else:
                    dai_o=models.zupu_level.objects.create(
                        myid = number.get_id("dai"),
                        community = community[0],
                        level_key = "ddd",
                        dai = dai,
                        name = name,
                        create_person = user
                    )
                    # 初始化孩子
                    if dai == "0":
                        models.zupu_relationship.objects.create(
                            myid=number.get_id("zupu"),
                            name="始祖",
                            dai=dai_o,
                            community=community[0],
                            parent="",
                            xh=0
                        )

            return JsonResponse(msg.table("success"))
    return JsonResponse(msg.table("error"))

def zupu_part(request):
    if request.method=="GET":
        openid = request.GET.get("openid", "")
        page=int(request.GET.get("page", "1"))
        dai = request.GET.get("dai", "")
        dai_obj = models.zupu_level.objects.get(dai=dai)
        user = models.Users.objects.get(openid=openid)
        community = models.Communities.objects.filter(myid=user.community_id)[0]
        start_num = (page-1)*10
        end_num = (page)*10
        if func.auth_role(func.role_weight("people"), user.role_weight):
            qs_part = models.zupu_relationship.objects.filter(community=community,dai=dai_obj, stati__gt=0).order_by("create_time")
            zupu_part = []
            for item in qs_part:
                zupu_part.append(item.short_show())
            res = msg.table("success")
            res["zupu_part"]=zupu_part
            return JsonResponse(res)
    if  request.method=="POST":
        info_dict = json.loads(request.body.decode('utf-8'))
        user = models.Users.objects.get(openid=info_dict["openid"])
        del info_dict["openid"]
        if not func.auth_role(func.role_weight("people"), user.role_weight):
            return JsonResponse( msg.table("error"))
        community = models.Communities.objects.filter(myid=user.community_id)[0]
        if info_dict["type"]=="new":
            f = models.zupu_relationship.objects.get(myid=info_dict["fid"])
            dai = int(info_dict["dai"])
            dai_obj = models.zupu_level.objects.get(dai=int(dai + 1))

            xh=(models.zupu_relationship.objects.filter(community=community,dai=dai_obj, stati__gt=0).count())+1
            child = models.zupu_relationship.objects.create(
                myid=number.get_id("zupu"),
                name = info_dict["name"],
                dai=dai_obj,
                community=community,
                parent=f.myid,
                xh=xh
            )
        elif info_dict["type"]=="edit":
            del info_dict["type"]
            del info_dict["dai"]
            for key, value in info_dict.items():
                qs = models.zupu_relationship.objects.get(myid=key)
                qs.set_name(value)
        elif  info_dict["type"]=="del":
            qs = models.zupu_relationship.objects.get(myid=info_dict["myid"])
            qs.change_stati(-1)

        return JsonResponse( msg.table("success"))
    return JsonResponse( msg.table("error"))


# 树形
def tree(request):
    if request.method == "GET":
        openid = request.GET.get("openid", "0")
        put_id=request.GET.get("id", "0")
        type = request.GET.get("type", "")
        me = models.zupu_relationship.objects.get(myid=put_id, stati__gt=0)
        id=put_id
        if type =="col_up":
            # 竖向上一页，找哥哥
            xh = int(me.xh)-1
            qs = models.zupu_relationship.objects.filter(parent=me.parent, xh=xh, stati__gt=0)
            if qs:
                id = qs[0].myid
            else:
                return JsonResponse(msg.table("error"))
        elif type =="col_next":
            # 竖向下一页，找弟弟
            xh = int(me.xh) + 1
            qs = models.zupu_relationship.objects.filter(parent=me.parent, xh=xh, stati__gt=0)

            if qs:
                id = qs[0].myid
            else:
                return JsonResponse(msg.table("error"))

        elif type == "row_up":
            # 横向上一页，找长子
            qs = list(models.zupu_relationship.objects.filter(parent=me.myid, stati__gt=0).order_by("xh"))

            if qs:
                id = qs[0].myid
            else:
                return JsonResponse(msg.table("error"))

        elif type == "row_next":
            # 横向下一页，找小儿子
            qs = list(models.zupu_relationship.objects.filter(parent=me.myid, stati__gt=0).order_by("xh"))
            if qs:
                id = qs[-1].myid
            else:
                return JsonResponse(msg.table("error"))

        # 一级
        one = models.zupu_relationship.objects.get(myid=id, stati__gt=0)
        # 二级
        two = models.zupu_relationship.objects.filter(parent=id, stati__gt=0).order_by("xh")

        children1=[]
        for item in two:
            children2=[]
            three=models.zupu_relationship.objects.filter(parent=item.myid, stati__gt=0).order_by("xh")
            for item2 in three:
                children2.append({"name":item2.name,"children":[]})
            children1.append({"name": item.name, "children": children2})

        tree = {
            "myid":one.myid,
            "name": one.name,
            "children":children1
        }
        res = msg.table("success")
        res["tree"] = tree
        return JsonResponse(res)
    return JsonResponse(msg.table("error"))

def get_user_info(request):
    openid = request.GET.get("openid", "0")
    user_id = request.GET.get("user_id", "0")
    user = models.Users.objects.get(openid=openid)
    if func.auth_role(func.role_weight("people"), user.role_weight):
        zupu_user = models.zupu_relationship.objects.get(myid=user_id)
        res = msg.table("success")
        if not zupu_user.info:
            res["user_info"] ={"name":zupu_user.name}
            res["dai"]=zupu_user.dai.dai
        else:
            res["user_info"]=zupu_user.info.user_info()
            res["dai"]=zupu_user.dai.dai
        return JsonResponse(res)
    return JsonResponse(msg.table("error"))


def xusers(request):
    if request.method == "GET":
        openid = request.GET.get("openid", "0")
        name = request.GET.get("name", "")
        user = models.Users.objects.get(openid=openid)
        if  func.auth_role(func.role_weight("people"), user.role_weight):
            community = models.Communities.objects.filter(myid=user.community_id)
            zupu_users = models.zupu_relationship.objects.filter(name__icontains=name).values('name',"myid")
            res = msg.table("success")
            res["users"]=list(zupu_users)
            return JsonResponse(res)
    return JsonResponse(msg.table("error"))

def r_users(request):
    '''
    小程序获得真正的用户
    :param request: 
    :return: 
    '''
    if request.method == "GET":
        openid = request.GET.get("openid", "0")
        name = request.GET.get("name", "")
        user = models.Users.objects.get(openid=openid)
        if  func.auth_role(func.role_weight("people"), user.role_weight):
            community = models.Communities.objects.filter(myid=user.community_id)
            r_users = models.Users.objects.filter(name__icontains=name).values('name',"myid")
            res = msg.table("success")
            res["users"]=list(r_users)
            return JsonResponse(res)
    return JsonResponse(msg.table("error"))

def test(request):
    """
       图片上传
       :param request: 
       :return: 
       """
    if request.method == 'POST':
        img=request.FILES.get('img'),
        name=request.FILES.get('img').name
        return JsonResponse(msg.table("success"))
    return render(request, 'font/test.html')