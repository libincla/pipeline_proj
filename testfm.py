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
