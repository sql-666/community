from django.contrib import admin

from communityApp.models import *

@admin.register(Users)
class usersAdmin(admin.ModelAdmin):
    list_display =['name', 'community_id', 'gender', 'account', 'stati', 'valid']
    list_per_page = 10
    search_fields = ['name', 'community_id', 'account']
    actions_on_top = True
    actions_on_bottom = True
    ordering = ['-create_time']

@admin.register(Communities)
class communityAdmin(admin.ModelAdmin):
    list_display=['name','province','administrator','deadline','create_time','create_person','valid']
    list_per_page = 10
    search_fields = ['name','province','administrator']
    ordering = ['-create_time']

@admin.register(Volunteers)
class volunteerAdmin(admin.ModelAdmin):
    list_display=['user_info','activtiy','create_time','valid']
    list_per_page = 10
    search_fields = ['user_info', 'activtiy']
    ordering = ['-create_time']

@admin.register(Products)
class productAdmin(admin.ModelAdmin):
    list_display = ['myid', 'title', 'price', 'unit', 'start_price', 'type', 'community', 'get_type', 'valid']
    list_per_page = 10
    search_fields = ['title', 'myid', 'type', 'get_type']
    ordering = ['-create_time']

@admin.register(Product_type)
class productTypeAdmin(admin.ModelAdmin):
    list_display=['myid','type_name','type_id','tn','valid']
    list_per_page = 10
    search_fields = ['type_name','type_id','tn']
    ordering = ['type_id']

@admin.register(Images)
class imageAdmin(admin.ModelAdmin):
    list_display=['id','title','url','product','type']
    list_per_page = 10
    search_fields = ['title','type', 'id']
    ordering = ['id']

@admin.register(Respects)
class respectAdmin(admin.ModelAdmin):
    list_display=['name', 'age', 'gender', 'live_situation', 'prove_num', 'publish_person','create_time','valid']
    list_per_page = 10
    search_fields = ['name','publish_person', 'myid','gender']
    ordering = ['-create_time']

@admin.register(Volun_leader)
class volunLeaderAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'add_person', 'create_time', 'valid']
    list_per_page = 10
    search_fields = ['user_info', 'add_person']
    ordering = ['-create_time']

@admin.register(Confirm_people)
class confirmPeopleAdmin(admin.ModelAdmin):
    list_display = ['respect', 'user', 'create_time', 'valid']
    list_per_page = 10
    search_fields = ['respect', 'user']
    ordering = ['-create_time']

@admin.register(Volun_activity)
class volunActivityAdmin(admin.ModelAdmin):
    list_display = ['myid', 'title', 'community', 'deadline', 'leader']
    list_per_page = 10
    search_fields = ['title', 'community']
    ordering = ['-deadline']

@admin.register(Applications)
class applicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'speciality', 'reason', 'create_time', 'valid']
    list_per_page = 10
    search_fields = ['user', 'reason', 'speciality']
    ordering = ['-create_time']

@admin.register(Activty_respects)
class activtyRespectAdmin(admin.ModelAdmin):
    list_display = ['activity', 'respect', 'stati', 'valid']
    list_per_page = 10
    search_fields = ['activity', 'respect']

@admin.register(Volun_activity_d)
class volunActivityDAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'activity', 'create_time', 'job', 'valid']
    list_per_page = 10
    search_fields = ['activity', 'user_info']
    ordering = ['-create_time']

@admin.register(Administrator)
class administratorAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'community_id', 'phone', 'create_time', 'valid']
    list_per_page = 10
    search_fields = ['user_info', 'community_id', 'phone' ]
    ordering = ['-create_time']

@admin.register(Family)
class familyAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'community', 'dai_number', 'valid']
    list_per_page = 10
    search_fields = ['user_info', 'community']
    ordering = ['-create_time']

@admin.register(Authority)
class authorityAdmin(admin.ModelAdmin):
    list_display = ['myid', 'title', 'valid']
    list_per_page = 10
    search_fields = ['myid', 'title']

@admin.register(Role)
class roleAdmin(admin.ModelAdmin):
    list_display = ['myid','title', 'authority', 'valid']
    list_per_page = 10
    search_fields = ['myid', 'title','authority']

# 注册Model类
# admin.site.register(Users, usersAdmin)




