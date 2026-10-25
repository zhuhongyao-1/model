"""
    测试：langgraph的入门案例
    LangGraph中的三个组成：1、状态  2、节点（函数） 3、边

    LangGraph的使用流程：
    1、创建状态，本质就是一个模型类，其中设置了LangGraph中需要共享和传递的数据
    2、创建节点
    3、通过状态创建builder实例，并添加节点和边
    4、添加节点和边
    5、对builder进行编译，获取图对象
    6、执行图对象
"""
from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 创建状态，本质就是一个模型类，其中设置了LangGraph中需要共享和传递的数据
class MyState(TypedDict):
    query: str
    final_result: str

class SearchState(TypedDict):
    rag_search_result: str
    web_search_result: str

# 创建输入状态结构，约束执行图对象时输入的数据
class InputState(TypedDict):
    query: str

# 创建输出状态结构，约束执行图对象时输出的数据
class OutputState(TypedDict):
    final_result: str

# 创建节点，节点的形参列表中至少要包含状态参数
# 节点的返回值是一个字典，字典中的键要和状态中的属性保持一致
# 当执行了这个节点，节点所返回的数据就会保存在状态中所对应的属性中
def rag_search_node(state : MyState):
    print("rag_search_node:", state)
    # 获取query
    query = state["query"]
    return {"rag_search_result":f"这是关于{query}的RAG检索结果"}

def web_search_node(state : MyState):
    print("web_search_node:", state)
    # 获取query
    query = state["query"]
    return {"web_search_result":f"这是关于{query}的WEB搜索结果"}

def final_node(state : SearchState):
    print("final_node:", state)
    rag_seach_result = state["rag_search_result"]
    web_search_result = state["web_search_result"]
    return {"final_result": f"这是对{rag_seach_result}和{web_search_result}的总结"}

# 通过状态创建builder实例，并添加节点和边
builder = StateGraph(MyState, input_schema=InputState, output_schema=OutputState)

# 添加节点，使用函数对象添加节点
builder.add_node(rag_search_node)
builder.add_node(web_search_node)
builder.add_node(final_node)

# 添加边，指定节点名称，若未设置节点名称，则默认为函数名
builder.add_edge(START, "rag_search_node")
builder.add_edge(START, "web_search_node")
builder.add_edge("rag_search_node", "final_node")
builder.add_edge("web_search_node", "final_node")
builder.add_edge("final_node", END)

# 对builder进行编译，获取图对象
graph = builder.compile()

# 执行图对象
result = graph.invoke({"query":"什么是LangGraph"})

print(result)

print(graph.get_graph().draw_ascii())