"""
    测试：获取图对象执行过程中的历史状态
"""
import operator
import sqlite3
from typing import TypedDict, Annotated

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

conn = sqlite3.connect('./test_sqlite', check_same_thread=False)
checkpointer = SqliteSaver(conn)

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

graph = builder.compile(checkpointer)

result = graph.invoke({}, config={"configurable":{"thread_id":"abc123"}})

last_state = graph.get_state(config={"configurable":{"thread_id":"abc123"}})
print(last_state)
print("="*100)
all_states = graph.get_state_history(config={"configurable":{"thread_id":"abc123"}})
for i in list(all_states):
    print(i)

