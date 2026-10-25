"""
    通过Sqlite实现长期记忆
"""
import sqlite3
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

# 获取连接Sqlite的连接对象
conn = sqlite3.connect(database='./test_sqlite', check_same_thread=False)

# 创建长期记忆所对应的检查点对象
checkpointer = SqliteSaver(conn)

class MyState(TypedDict):
    key1: str
    key2: str
    key3: str

def node_one(state : MyState):
    print("node_one节点正在执行")
    return {"key1": "value1"}

def node_two(state : MyState):
    # raise Exception("node_two出现异常")
    print("node_two节点正在执行")
    return {"key2": "value2"}

def node_three(state : MyState):
    print("node_three节点正在执行")
    return {"key3": "value3"}

builder = StateGraph(MyState)

builder.add_node(node_one)
builder.add_node(node_two)
builder.add_node(node_three)

builder.add_edge(START, "node_one")
builder.add_edge("node_one", "node_two")
builder.add_edge("node_one", "node_three")
builder.add_edge("node_two", END)
builder.add_edge("node_three", END)

# 编译获取图对象，并设置检查点实现记忆功能
graph = builder.compile(checkpointer=checkpointer)

# 第一次模拟节点的异常
# result = graph.invoke({}, config={"configurable":{"thread_id":"abc123"}})
# 第二次若需要使用保存的状态，则必须传输None
result = graph.invoke(None, config={"configurable":{"thread_id":"abc123"}})

print(result)