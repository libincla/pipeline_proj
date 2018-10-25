from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from .settings import URL, DATABASE, DATABASE_DEBUG



Base = declarative_base()


STATE_WAITING = 0
STATE_PENDING = 1
STATE_RUNNING = 2
STATE_SUCCED = 3
STATE_FAILED = 4
STATE_FINISH = 5


class Graph(Base):
    __tablename__ = 'graph'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False, unique=True)
    desc = Column(String(250), nullable=True)
    checked = Column(Integer, nullable=False, default=0)
    sealed = Column(Integer, nullable=False, default=0)

    # vertexes = relationship('Vertex', foreign_keys="Vertex.g_id")
    # edges = relationship('Edge', foreign_keys="Edge.g_id")

    def __repr__(self):
        return "<Graph {} {} >".format(self.id, self.name)

    __str__ = __repr__

class Vertex(Base):
    __tablename__ = 'vertex'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False)
    input = Column(Text, nullable=True)
    script = Column(Text, nullable=True)
    g_id = Column(Integer, ForeignKey('graph.id'))

    graph = relationship('Graph')
    tails = relationship('Edge', foreign_keys='[Edge.tail]')
    heads = relationship('Edge', foreign_keys='Edge.head')

    def __repr__(self):
        return "<Vertex {} {} >".format(self.id, self.name)

    __str__ = __repr__

class Edge(Base):
    __tablename__ = 'edge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)
    tail = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    head = Column(Integer, ForeignKey('vertex.id'), nullable=False)

    def __repr__(self):
        return "<Edge {} {} >".format(self.id)

    __str__ = __repr__

class Pipeline(Base):
    __tablename__ = 'pipeline'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False)
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)
    #current = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    state = Column(Integer, nullable=False, default=STATE_WAITING)


    tracks = relationship('Track', foreign_keys="Track.p_id")
    #在一端查多端，需要加上foreign_keys 设计这个字段是为了 有人从pipeline查询所有Track的字段。
    #在一端的话，查询就应该像
    #pipeline = db.session.query(Pipeline).filter(Pipeline.id = 1).one()  这是找到一个pipeline的对象
    #再通过 pipeline.tracks 查出属于这个id为1的pipeline有多少tracks，这个pipeline.tracks的类型是个列表



    def __repr__(self):
        return "<Pipeline {} {} >".format(self.id, self.name)

    __str__ = __repr__

class Track(Base):

    __tablename__ = 'track'
    id = Column(Integer, primary_key=True, autoincrement=True)
    p_id = Column(Integer, ForeignKey('pipeline.id'), nullable=False)
    v_id = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    input = Column(Text, nullable=True)
    output = Column(Text, nullable=True)
    script = Column(Text, nullable=True)
    state = Column(Integer, nullable=False,default=STATE_WAITING)

    vertex = relationship('Vertex')
    # 这属于在多端查一端
    # 加这个relationship是为了后面需要从Track表 查顶点的名称时，由于是多对一关系，查询起来非常复杂，需要在多端加一个relationship()
    # 以后如果需要查，则可以通过 Track(实例名).vertex.name 从Track表中查看对应顶点的名称
    pipeline = relationship('Pipeline')  #方便查 Track.pipeline.name



    def __repr__(self):
        return "<Track {} {} >".format(self.id, self.state)

    __str__ = __repr__


# engine = create_engine(URL, echo=DATABASE_DEBUG)
# session = sessionmaker(bind=engine)()


# #装饰器 实现单例的装饰器
# from functools import  wraps
#
# def singleton(cls):
#     instance = None
#     @wraps(cls)
#     def wrapper(*args, **kwargs):
#         nonlocal instance   #外层函数定义的，但不是全局
#         if not instance:
#             ret = cls(*args, **kwargs)
#             instance = ret
#
#         # return ret
#         return instance
#     return wrapper





#单例模式
# @singleton
class Database:
    # count = 0
    # # 在实例化的时候，先走到__new__方法中
    def __new__(cls, *args, **kwargs):
        # print(cls)
        # print(args)
        # print(kwargs)
        if not hasattr(cls, '_instance'):
            print('第一')

        if hasattr(cls, '_instance'):
            print(cls)
            print('第二')
            print('!!!!!!!!!!!',cls._instance)
            print('以上')
            return cls._instance

        cls._instance = super().__new__(cls)
        # print(cls._instance.__dict__)
        # return super().__new__(cls)
        cls._instance._engine = create_engine(args[0], **kwargs)
        cls._instance._session = sessionmaker(bind=cls._instance._engine)()


        return cls._instance

    def __init__(self, url, **kwargs):
        # if self.count == 0:
        #     self.__class__.count += 1
        # if not hasattr(type(self), '_instance'):
        # if not hasattr(type(self), '_instance'):
        # self._engine = create_engine(url, **kwargs)
        # self._session = sessionmaker(bind=self.engine)()
        print(self.__dict__)


    @property
    def session(self):
        return self._session

    @property
    def engine(self):
        return  self._engine


    def create_all(self):
        Base.metadata.create_all(self._engine)

    def drop_all(self):
        Base.metadata.drop_all(self._engine)

    def __repr__(self):
        return "~~~~~~<{} {} {} >".format(self.__class__.__name__, id(self), id(self._engine), id(self._session))
#

db = Database(URL, echo=DATABASE_DEBUG)


# print('*') * 45
# db1 = Database(URL, echo=DATABASE_DEBUG)
