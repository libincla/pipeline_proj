from pipeline.model import db
from pipeline.model import Graph, Vertex, Pipeline, Edge, Track
from pipeline.service import create_graph, add_edge, add_vertex
import json


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

        ba = add_edge(b, a, g1)
        ac = add_edge(a, c, g1)
        cb = add_edge(c, b, g1)
        bd = add_edge(b, d, g1)


        #创建DAG
        g2 = create_graph('my_test3', 'DAG')

        #增加顶点
        a2 = add_vertex(g2,'A', None, 'echo DAG.A')
        b2 = add_vertex(g2,'B', None, 'echo DAG.B')
        c2 = add_vertex(g2, 'C', None, 'echo DAG.C')
        d2 = add_vertex(g2, 'D', None, 'echo DAG.D')

        #增加边
        ba = add_vertex(b, a, g2)
        ac = add_vertex(a, c, g2)
        bc = add_vertex(b, c ,g2)
        bd = add_vertex(b, d, g2)


        #创建第四个DAG
        g3 = create_graph('my_test4', "DAG")  #多入口


        #增加顶点
        a3 = add_vertex(g3,'A', None, 'echo DAG.A')
        b3 = add_vertex(g3,'B', None, 'echo DAG.B')
        c3 = add_vertex(g3, 'C', None, 'echo DAG.C')
        d3 = add_vertex(g3, 'D', None, 'echo DAG.D')

        #增加边
        ab = add_edge(a, b, g3)
        ac = add_edge(a, c, g3)
        cb = add_edge(c, b, g3)
        db = add_edge(d, b, g3)




    except Exception as e:
        print(e)


test_create_dag()