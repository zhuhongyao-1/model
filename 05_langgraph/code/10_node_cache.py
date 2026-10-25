"""
    测试：节点的缓存
"""
import time
from typing import TypedDict

from langgraph.cache.memory import InMemoryCache
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import CachePolicy


class MyState(TypedDict):
    x: int
    result: int

def node_cache(state : MyState):
    print("node_cache开始执行")
    time.sleep(2)
    print("node_cache执行完毕")
    return {"result": state["x"] * 2}

checkpointer = InMemorySaver()
builder = StateGraph(MyState)

# 在添加节点时，设置节点的缓存策略
builder.add_node(node_cache, cache_policy=CachePolicy(ttl=300))

builder.add_edge(START, "node_cache")
builder.add_edge("node_cache", END)

# 在编译图对象时，可以设置缓存存储方式（即缓存保存的位置）
graph = builder.compile(checkpointer=checkpointer, cache=InMemoryCache())

result = graph.invoke({"x":5}, config={"configurable":{"thread_id":"abc"}})
print(result)
result = graph.invoke({"x":5}, config={"configurable":{"thread_id":"xyz"}})
print(result)


