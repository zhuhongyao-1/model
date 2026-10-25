"""
    测试：循环边
"""
from typing import TypedDict

from langgraph.constants import END, START
from langgraph.graph import StateGraph


class MyState(TypedDict):
    count: int
    result: str
    max_count: int

def node_a(state: MyState):
    state['count'] += 1
    print(f"当前第{state['count']}执行A节点")
    return {"count": state['count'], "result": f"第{state['count']}执行A节点"}

def node_b(state: MyState):
    print(f"当前第{state['count']}执行B节点")
    return {"result": f"第{state['count']}执行B节点"}

def route_condition(state: MyState):
    if state['count'] < state['max_count']:
        return "node_b"
    else:
        return END

builder = StateGraph(MyState)

builder.add_node(node_a)
builder.add_node(node_b)

builder.add_edge(START, "node_a")
builder.add_conditional_edges("node_a", route_condition)
builder.add_edge("node_b", "node_a")

graph = builder.compile()
result = graph.invoke({"count":0, "max_count":10}, config={"recursion_limit": 6})
print(result)