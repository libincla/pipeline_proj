from .service import Graph, Vertex, Edge, Pipeline, Track
from .model import STATE_FAILED, STATE_FINISH, STATE_PENDING, STATE_RUNNING, STATE_SUCCED, STATE_WAITING
from .service import db


#开启一个流程，用户指定一个名称、描述


def start(g_id, name=None, desc=None):
    # checked 检查给的图id是否是一个经过DAG检查合格的图
    g = db.session.query(Graph).filter((Graph.id == g_id) & (Graph.checked == 1)).first()
    if not g:
        print('not DAG Graph')

    # 判断流程是否存在，且checked为1即检验过
    query_string = db.session.query(Graph).filter(Graph.id == g_id).filter(Graph.checked == 1).first()
    if query_string:
        print('*' * 10)
        print(query_string)
        print('%' * 5 )
    else:
        print('not found')

    # 当找到所有顶点，然后复制到Track中
    # 查询一下这个graph的所有顶点
    vertexes_query = db.session.query(Vertex).filter(Vertex.g_id == g_id)  #这个是一个sql语句
    vertexes  =  vertexes_query.all()  #sql.all()才是取出来的对象
    if not vertexes_query:
        return

    #query的值是找到的所有起点
    query = vertexes_query.filter(Vertex.id.notin_(
        db.session.query(Edge.head).filter(Edge.g_id == g_id)
    )).all()
    print('^' * 20)
    print(query)



    # 写入pipeline表

    p = Pipeline()
    p.name = name
    p.g_id = g_id
    p.desc = desc
    p.state = STATE_RUNNING  #开启第一个流程

    db.session.add(p)


    #track表初始化所有节点
    for v in vertexes:
        t = Track()
        t.v_id = v.id
        t.pipeline = p
        t.state = STATE_PENDING if t.v_id in query else STATE_WAITING

        db.session.add(t)


    #封闭graph  sealed    如果没人使用，就使用这个图，并把图的sealed的状态写成不许修改的
    if g.sealed == 0:
        g.sealed = 1
        db.session.add(g)

    try:
        db.session.commit()

    except Exception as e:
        print(e)
        db.session.rollback()



