"""
    测试：条件边
"""
from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


class MyState(TypedDict):
    value: int
    step: str

def node_a(state : MyState):
    print("节点A执行完毕")
    return {"step":"A执行完毕"}

def node_b(state : MyState):
    print("节点B执行完毕")
    return {"value":state["value"] * 2,"step":"B执行完毕"}

def node_c(state : MyState):
    print("节点C执行完毕")
    return {"value":state["value"] - 1,"step":"C执行完毕"}

# 创建路由条件函数
def route_condition(state : MyState):
    if state["value"] % 2 == 0:
        return "node_b"
    else:
        return "node_c"

builder = StateGraph(MyState)

builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)

builder.add_edge(START, "node_a")
builder.add_conditional_edges("node_a", route_condition)
builder.add_edge("node_b", END)
builder.add_edge("node_c", END)

graph = builder.compile()

result = graph.invoke({"value":1})
print(result)