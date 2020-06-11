from communityApp.tools import func
def table(name):
    '''
    各个重要字段的格式要求
    :param name: 
    :return: 
    '''
    data={
        "account":{
            "empty":False,
            "length_num":11,
            "con":"number"
        },
        "password":{
            "empty": False,
            "length_num": 16,
            "con": ""
        },
        "community_name":{
            "empty": False,
            "length": 10,
            "con": ""
        },
        "code":{
            "empty": False,
            "length_num": 4,
            "con": "number"
        },
        "phone":{
            "empty": False,
            "length_num": 11,
            "con": "number"
        },
        "title":{
            "empty": False,
            "length_num": 11,
            "con": "number"
        },
        "price":{
            "empty": False,
            "length_num": 11,
            "con": "number"
        },
        "unit":{
            "empty": False,
            "length_num": 5,
            "con": ""
        },
        "start_price":{
            "empty": False,
            "length_num": 10,
            "con": "number"
        },
        "type":{
            "empty": False,
            "length_num": 10,
            "con": ""
        },
        "get_type":{
            "empty": False,
            "length_num": 10,
            "con": ""
        },
        "note":{
            "empty": True,
            "length_num": 100,
            "con": ""
        },
        "inventory":{
            "empty": False,
            "length_num": 100,
            "con": "number"
        }
    }
    return data[name]


def auth(auth_list):
    '''
    验证数据格式
    :param auth_list: 
    :return: 
    '''
    for item in auth_list:
        format = table(item["bt"])
        if not format["empty"]:
            return not func.empty(item["value"])
        if format["length_num"] > 0:
            return func.string_len(item["value"], format["length_num"])
        if format["con"] == "number":
            return isinstance (item["value"],int)
    return True


def page(page_name, role_weight=0):
    '''
    页面的基础功能
    :param page_name: 
    :return: 
    '''
    app_name = "/myapp"
    table={}
    table["index"]=[{
            "title": "暖巢计划",
            "icon": 'icons/respect.png',
            "viewUrl": app_name+'/help_respects?page_id=1'
        },{
            "title": "志愿活动",
            "icon": 'icons/volunteer.png',
            "viewUrl": app_name+'/volunteers?type=all&page_id=1'
        },{
            "title": "赶集广场",
            "icon": 'icons/square.png',
            "viewUrl": app_name+'/product?type=all&page_id=1'
        },{
            "title": "我的社区",
            "icon": 'icons/community.png',
            "viewUrl": app_name + '/mycommunity'
        },{
            "title": "个人中心",
            "icon": 'icons/me.png',
            "viewUrl": app_name+'/user'
        }
    ]
    # "page_url":app_name+"/my_need",
    table["user"]=[{
        "title":"编辑资料",
        "page_url":app_name+"/edit_user_info",
        # "role":["general_user","leader", "adminitrator","people"],
        "role_weight":1,
        "id":"1"
    },
    # {
    #     "title":"老人上报",
    #     "page_url":app_name+"/add_respect",
    #     # "role": ["people","leader", "adminitrator"],
    #     "role_weight": 2,
    #     "id":"2"
    # },
    {
        "title":"商品发布",
        "page_url":app_name+"/my_product",
        # "role": ["people","leader", "adminitrator"],
        "role_weight": 2,
        "id":"4"
    },{
        "title":"志愿记录",
        "page_url":app_name+"/volunteer_d",
        # "role": ["volunteer","leader", "adminitrator"],
        "role_weight": 3,
        "id":"3"
    },{
        "title":"志愿者管理",
        "page_url":app_name+"/m_volunteer?flag=volunteer",
        # "role": ["leader", "adminitrator"],
        "role_weight": 4,
        "id":"8"
    },{
        "title":"发布的活动",
        "page_url":app_name+"/m_activity",
        # "role": ["leader", "adminitrator"],
        "role_weight": 4,
        "id":"8"
    },{
        "title":"成员管理",
        "page_url":app_name+"/del_people",
        # "role": ["adminitrator"],
        "role_weight": 5,
        "id":"5"
    },{
        "title":"商品管理",
        "page_url":app_name+"/my_product",
        # "role": ["adminitrator"],
        "role_weight": 5,
        "id":"6"
    },{
        "title":"指定队长",
        "page_url":app_name+"/m_volunteer?flag=leader",
        # "role": ["adminitrator"],
        "role_weight": 5,
        "id":"7"
    },{
        "title":"活动管理",
        "page_url":app_name+"/m_activity",
        # "role": ["adminitrator"],
        "role_weight": 5,
        "id":"9"
    }]
    if page_name == "user":
        user_page=[]
        for item in table["user"]:
            if role_weight>=item["role_weight"]:
                user_page.append(item)
        return  user_page

    return table[page_name]


def type(value):
    table={
        "col_up": "col_up",
        "col_next": "col_next",
        "row_up": "row_up",
        "row_next": "row_next",
        "init":"init"
    }
    return table[value]