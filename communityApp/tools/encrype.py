import hashlib

def password(value):
    value=value+"_@community_$425_*"
    m = hashlib.md5()
    m.update(value.encode("utf-8"))
    value_md5 = m.hexdigest()
    return value_md5