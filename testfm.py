# def sing(cls):
#     print('giao')
#     def wrapper(*args, **kwargs):
#         ret = cls(*args, **kwargs)
#         print(args)
#         print(kwargs)
#         return ret
#
#     return wrapper
#
# @sing
# class A:
#     def __init__(self, *args, **kwargs):
#         pass
#
#
# a = A(123)
# print('*' * 8)
# b = A(234)

from collections import  defaultdict

s1 = defaultdict()
print(s1)

s2 = defaultdict(list)
print(s2)

s3 = defaultdict(set)
print(s3)

s4 = defaultdict(tuple)
print(s4)

s5 = defaultdict(dict)
print(s5)