from pipeline.model import Database
from pipeline.settings import URL, DATABASE_DEBUG

db = Database(URL, echo=DATABASE_DEBUG)
# db.drop_all()
db.create_all()
# print(db)
# print('*' * 45)
# db1 = Database(URL, echo=DATABASE_DEBUG)
# print(db1)



# def singleton(cls):
#     instance = None
#     flag = {}
#     print('yahou')
#     def wrapper(*args, **kwargs):
#         nonlocal instance   #外层函数定义的，但不是全局
#
#         if not instance:
#             ret = cls(*args, **kwargs)
#             instance = ret
#             print(args)
#             print(kwargs)
#
#
#         return instance
#     return wrapper
#
# @singleton
# class A:
#     def __init__(self, *args, **kwargs):
#         print(args)
#
#
# a = A(123, b=123)
# print('*' * 10)
# b = A(345, c=123)


