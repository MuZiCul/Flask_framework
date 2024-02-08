import re


def is_valid_email(email):
    # 根据RFC 5322官方标准定义的一个简化版邮箱正则表达式
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # 使用match方法检查邮箱地址的格式
    if re.match(pattern, email):
        return True
    else:
        return False
