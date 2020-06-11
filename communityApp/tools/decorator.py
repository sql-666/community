from django.shortcuts import redirect

# 查看登录状态
def log_in(func):
    '''身份认证装饰器，
    :param func:
    :return:
    '''
    def wrapper(request,*args,**kwargs):
        if not request.session.get("community_username"):
            return redirect("/myapp/login/")
        return  func(request,*args, **kwargs)
    return wrapper