def empty(value):
    '''
    判空
    :param value: 
    :return: 
    '''
    if value == "":
        return True
    return False


def string_len(value, len_num):
    '''
    字符串长度
    :param value: 
    :param len_num: 
    :return: 
    '''
    if int(len_num)==int(len(value)):
        return True
    return False

def role_weight(name):
    table={
        "general_user":1,
        "people":2,
        "volunteer":3,
        "leader":4,
        "zupu":4,
        "administrator":5
    }
    return table[name]

def auth_role(value,role_weight):
    '''
    查看权限
    :param value: 应有的角色权重
    :param role_weight: 用户角色权重
    :return: 
    '''
    if int(value) <= int(role_weight):
        return True
    else:
        return False




