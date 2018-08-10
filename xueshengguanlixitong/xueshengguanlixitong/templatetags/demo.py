from django import template

register = template.Library()

@register.filter
def abc(value):
    return value.split(',')

# @register.filter
# def abc2(value):
#     return value.split('|')
# class a:
#     def aa(self):
#         print("c")
# print(a()==a())   #指向了不同的内存
