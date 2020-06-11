# from django.conf.urls import url
from django.urls import path
from communityApp import views


urlpatterns = [
    path('r_users/', views.r_users, name="r_users"),
    path('zupu_connet/', views.zupu_connet, name="zupu_connet"),
    path('phone_code/',views.phone_code, name="phone_code"),
    path('create_community/', views.create_community, name="create_community"),
    path('enter_community/', views.enter_community, name="enter_community"),
    path('people_l/', views.people_l, name="people_l"),
    path('get_user_info/', views.get_user_info, name="get_user_info"),
    path('xusers/',views.xusers, name="xusers"),
    path('tree/', views.tree, name="tree"),
    path('zupu_part/', views.zupu_part, name='zupu_part'),
    path('zupu_dai/', views.zupu_dai, name="zupu_dai"),
    path('xlogin/', views.xlogin, name="xlogin"),
    path('get_code/',views.get_code, name="get_code"),
    path('init_data/', views.init_data, name="init_data"),
    path('index/', views.index, name="index"),

    path('help_respects/', views.help_respects, name="help_respects"),
    path('del_people/', views.del_people, name="del_people"),
    path('check_people/', views.check_people, name="check_people"),
    path('respects_detail/', views.respects_detail, name="respects_detail"),
    path('add_respect/',views.add_respect, name="add_respect"),
    path('m_volunteer/', views.m_volunteer, name="m_volunteer"),
    path('add_vol_activity/', views.add_vol_activity, name="add_vol_activity"),
    path('end_activity/', views.end_activity, name="end_activity"),
    path('add_activity_d/', views.add_activity_d, name="add_activity_d"),

    path('volunteers/',views.volunteers, name="volunteers"),
    path('application/', views.application, name="application"),
    path('activity_d/', views.activity_d, name="activity_d"),
    path('confirm/', views.confirm_respect, name="confirm"),
    path('activity_l/', views.activity_l, name="activity_l"),
    path('m_activity/', views.m_activity, name="m_activity"),
    path('volunteer_d/', views.volunteer_d, name="volunteer_d"),

    path('product/', views.product, name="product"),
    path('product_d/', views.product_d, name="product_d"),
    path('edit_product/', views.edit_product, name="edit_product"),
    path('user/', views.user, name="user"),
    path('edit_user_info/', views.edit_user_info, name="edit_user_info"),
    path('my_product/',views.my_product, name="my_product"),
    path('edit_my_product/', views.edit_my_product, name="edit_my_product"),
    path('mycommunity/', views.mycommunity, name='mycommunity'),
    path('my_need/', views.my_need, name='my_need'),
    path('create_community/', views.create_community, name="create_community"),
    path('login/',views.login, name="login"),
    path('register/', views.register, name="register"),
    path('test/',views.test, name="test"),


]