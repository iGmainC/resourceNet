from django import template

register = template.Library()  #固定写法,不可改变
@register.filter  #过滤器
def add_str(value, arg):  # 最多有两个
    return '{}{}'.format(value, arg)