from .model import  db
from .model import Graph, Vertex, Pipeline, Edge, Track
from .settings import URL, DATABASE, DATABASE_DEBUG
from .model import Database

#创建DAG

#创建图的函数
def create_graph(name, desc=None):

    g = Graph()
    g.name = name
    g.desc = desc

    db.session.add(g)

    try:
        db.session.commit()
        return g
    except Exception as e:
        print(e)
        db.session.rollback()


#为图增加顶点
def add_vertex(graph:Graph, name:str, input=None, script=None):
    v = Vertex()
    v.g_id = graph.id
    v.name = name
    v.input = input
    v.script = script

    db.session.add(v)

    try:
        db.session.commit()
        return v
    except Exception as e:
        print(e)
        db.session.rollback()

#为顶点增加边
def add_edge(tail:Vertex, head:Vertex, graph:Graph):
    e = Edge()
    e.g_id = graph.id
    e.tail = tail.id
    e.head = head.id

    db.session.add(e)

    try:
        db.session.commit()
        return e
    except Exception as e:
        db.session.rollback()


#删除顶点
#删除顶点就要删除这个顶点关联的所有边

def del_vetex(id):

    query = db.session.query(Vertex).filter(Vertex.id == id)
    v = query.first()

    if v: #找到顶点后，删除关联的边，然后再删除顶点
        try:
            db.session.query(Edge).filter((Edge.tail == v.id) | (Edge.head == v.id)).delete()
            query.delete()
            db.session.commit()

        except Exception as e:
            print(e)
            db.session.rollback()

    return v




db = Database(URL, echo=DATABASE_DEBUG)
