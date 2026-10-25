from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph, add_messages


# def add_message(message_list_left:list,message_list_right:list):
#     print("="*20)
#     print("正在执行add_message")
#     print('左边的',message_list_left)
#     print('右边的',message_list_right)
#     print("="*20)
#     return message_list_left + message_list_right

class MyState(TypedDict):
    # result: list[str]
    # result: Annotated[list[str], add_message]
    result: Annotated[list[str], lambda old, new: old + new]
    # result: Annotated[list[str], add_messages]

def node_one(state : MyState):
    return {"result": ["hello"]}

def node_two(state : MyState):
    return {"result": ["world"]}

builder = StateGraph(MyState)

builder.add_node(node_one)
builder.add_node(node_two)

builder.add_edge(START, "node_one")
builder.add_edge("node_one", "node_two")
builder.add_edge("node_two", END)

graph = builder.compile()

res = graph.invoke({"result": ["LangGraph"]})

print(res)