from pipeline.model import db
from pipeline.model import Graph, Vertex, Pipeline, Edge, Track
from pipeline.service import create_graph, add_edge, add_vertex
import json
from collections import defaultdict


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





#
#
# print('*' * 10)
# print(A)
check_graph(A)
