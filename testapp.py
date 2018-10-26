from pipeline.model import Database
from pipeline.settings import URL, DATABASE_DEBUG
from pipeline.model import Graph, Vertex, Pipeline, Edge, Track
from pipeline.service import create_graph, add_edge, add_vertex
from pipeline.executor import start

# db = Database(URL, echo=DATABASE_DEBUG)
# db.drop_all()
# db.create_all()
# print(db)
# print('*' * 45)
# db1 = Database(URL, echo=DATABASE_DEBUG)
# print(db1)

start(1,'第一条测试数据')


# G_ID = 1
# # s1 = db.session.query(Vertex).filter(Vertex.g_id == G_ID).filter(Vertex.id.notin_(
# #     db.session.query(Edge.head).filter(Edge.g_id == G_ID)
# # )).all()
#
# all_vertex = db.session.query(Vertex).filter(Vertex.g_id == G_ID).all()
# print(all_vertex)
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


