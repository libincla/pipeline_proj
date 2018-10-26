from pipeline.model import db
from pipeline.model import Database
from pipeline.settings import URL, DATABASE_DEBUG
from pipeline.model import Graph, Vertex, Pipeline, Edge, Track
from pipeline.service import create_graph, add_edge, add_vertex
import json
from pipeline.executor import start, showpipeline
import json
from collections import defaultdict

def test_create_dag():

    try:
        #创建DAG
        g = create_graph('my_test11') #成功的话则返回一个图对象

        #增加顶点Vertex
        input = {
            "ip" : {
                "type": "str",
                "required": True,
                "default": "172.16.10.1"
            }
        }

        script = {
            "script" : "echo 'my_test1.A'\nping {ip}",
            "next" : "B"
        }
        #这里为了让用户方便，next可以接收两种类型，数字表示顶点的id，字符串表示同一个DAG中该名称的节点，不能够重复

        a = add_vertex(g, 'A', json.dumps(input), json.dumps(script))
        b = add_vertex(g, 'B', None, 'echo B')
        c = add_vertex(g, 'C', None, 'echo C')
        d = add_vertex(g, 'D', None, 'echo D')

        # 增加顶点的边
        ab = add_edge(a, b, g)
        ac = add_edge(a, c, g)
        cb = add_edge(c, b, g)
        bd = add_edge(b, d, g)


        #创建第二个图，该图是一个环路

        g1 = create_graph('my_test2', 'loop')
        # 增加顶点
        a1 = add_vertex(g1, 'A', None, 'echo loop.A')
        b1 = add_vertex(g1, 'B', None, 'echo loop.B')
        c1 = add_vertex(g1, 'C', None, 'echo loop.c')
        d1 = add_vertex(g1, 'D', None, 'echo loop.d')

        #增加边, abc之间的环

        ba = add_edge(b1, a1, g1)
        ac = add_edge(a1, c1, g1)
        cb = add_edge(c1, b1, g1)
        bd = add_edge(b1, d1, g1)


        #创建DAG
        g2 = create_graph('my_test3', 'DAG')

        #增加顶点
        a2 = add_vertex(g2,'A', None, 'echo DAG.A')
        b2 = add_vertex(g2,'B', None, 'echo DAG.B')
        c2 = add_vertex(g2, 'C', None, 'echo DAG.C')
        d2 = add_vertex(g2, 'D', None, 'echo DAG.D')

        #增加边
        ba = add_vertex(b2, a2, g2)
        ac = add_vertex(a2, c2, g2)
        bc = add_vertex(b2, c2 ,g2)
        bd = add_vertex(b2, d2, g2)


        #创建第四个DAG
        g3 = create_graph('my_test4', "DAG")  #多入口


        #增加顶点
        a3 = add_vertex(g3, 'A', None, 'echo DAG.A')
        b3 = add_vertex(g3, 'B', None, 'echo DAG.B')
        c3 = add_vertex(g3, 'C', None, 'echo DAG.C')
        d3 = add_vertex(g3, 'D', None, 'echo DAG.D')

        #增加边
        ab = add_edge(a3, b3, g3)
        ac = add_edge(a3, c3, g3)
        cb = add_edge(c3, b3, g3)
        db = add_edge(d3, b3, g3)




    except Exception as e:
        print(e)





def check_graph(graph:Graph):

    vertex_query = db.session.query(Vertex).filter(Vertex.g_id == graph.id)  #找到图id与顶点id相同的所有顶点了

    vertexes = {v.id for v in vertex_query}  #把找到的顶点都放到一个集合里

    edge_query = db.session.query(Edge).filter(Edge.g_id == graph.id) #同样找到图的id与边的id相同的所有边

    edges = defaultdict(list)  #准备把所有的边放入一个defaultdict的list中，默认是空的

    ids = set() #有入度的顶点  这里的核心思想就是利用集合 顶点=有入度的+没有入度的

    for e in edge_query:
        edges[e.tail].append((e.tail, e.head))
        ids.add(e.head)  #把所有边的顶点都放入这个集合中

    print('*' * 20)
    print(edges)
    print('!' * 10)
    print(ids)


    if len(edges) == 0:  #这里指一条边都没有
        return False

    ods = vertexes - ids
    print('z' * 10)
    print(vertexes)
    print(ods)

    if len(ods):
        for o in ods:
            if o in edges:
                del edges[o]


        while edges:
            vertexes = ids
            ids = set()

            for lst in edges.values():
                for edge in lst:
                    ids.add(edge[1])

            ods = vertexes - ids

            if len(ods) == 0:
                break

            for o  in ods:
                if o in edges:
                    del edges[o]

            print(edges)


    if len(edges) == 0:
        #检验通过
        try:
            graph = db.session.query(Graph).filter(Graph.id == graph.id).first()
            if graph:
                graph.checked = 1

            db.session.add(graph)
            db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            raise e
    return  False





db = Database(URL, echo=DATABASE_DEBUG)

A = db.session.query(Graph).filter(Graph.name == 'my_test11').first()

# db.drop_all()
# db.create_all()
# test_create_dag()
# check_graph(A)
# start(1,'第一条测试数据')

ps1 = showpipeline(1)
print(ps1)