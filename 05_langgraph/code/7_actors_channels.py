"""
    测试：获取图对象的节点和通道
"""
import operator
from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph


class MyState(TypedDict):
    result: Annotated[list[str], operator.add]

def node_a(state : MyState):
    return {"result":["A"]}

def node_b(state : MyState):
    return {"result":["B"]}

def node_c(state : MyState):
    return {"result":["C"]}

def node_b_2(state : MyState):
    return {"result":["B_2"]}

def node_d(state : MyState):
    return {"result":["D"]}

builder = StateGraph(MyState)

builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)
builder.add_node(node_b_2)
builder.add_node(node_d)

builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_a", "node_c")
builder.add_edge("node_b", "node_b_2")
builder.add_edge("node_b_2", "node_d")
builder.add_edge("node_c", "node_d")
builder.add_edge("node_d", END)

graph = builder.compile()

result = graph.invoke({})

print("执行图的结果：")
print(result)
print("="*100)

print("获取图对象中所有的节点：")
print(graph.nodes)
print("="*100)

print("获取图对象中所有的通道：")
print(graph.channels)
print("="*100)

print("获取图对象中node_a的订阅和输出：")
print(graph.nodes["node_a"].triggers)
print(graph.nodes["node_a"].writers)
print("="*100)

print("获取图对象中node_d的订阅和输出：")
print(graph.nodes["node_d"].triggers)
print(graph.nodes["node_d"].writers)
print("="*100)