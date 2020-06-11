
# 返回状态
def table(stati):
    table={
        "success":{"code":"200", "message":"success"},
        "error":{"code":"400", "message":"error"},
        "not_found":{"code": "404", "message": "notFound"},
        "repeat":{"code":"600", "message":"repeat"},
        "wrong_account":{"code":"401","message":"wrong account"},
        "no_authority":{"code":"800","message":"no_authority"},
        "error_code":{"code":"900","message":"error_code"}

    }
    return  table[stati]
