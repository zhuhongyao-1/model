"""
    测试：流式执行图对象
    values：每一个执行后，流式输出完整的状态
    updates：图执行过程中，每一步执行后流式输出增量更新。如果在同一个步当中产生了多个增量更新，这些增量更新会分别流式输出。
    custom：流式输出节点内部的自定义数据。
    messages：在任何调用了LLM的节点当中，流式输出两元组数据：（LLM Token，metadata）
    debug：流式输出所有能输出的信息
    混合模式：流模式传入列表，在列表当中添加多种不同的模式，可以得到多种流式输出
"""
import operator
from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime


class MyState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    step: str

def node_input(state : MyState):
    return {
        "messages": [HumanMessage("帮我写一段Python代码")],
        "step": "input"
    }

def node_processing(state : MyState, runtime : Runtime):
    # 获取流式执行的自定义输出对象
    wirter = runtime.stream_writer
    # 输出数据
    steps = ["正在分析意图...", "正在检索知识库...", "正在构建Prompt..."]
    for index, step in enumerate(steps):
        wirter(
            {
                "no": index + 1,
                "description": step
            }
        )
    return {"step":"processing"}

def node_generation(state : MyState):
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke(state["messages"])
    return {"messages": [response], "step": "generation"}

builder = StateGraph(MyState)

builder.add_node(node_input)
builder.add_node(node_processing)
builder.add_node(node_generation)

builder.add_edge(START, "node_input")
builder.add_edge("node_input", "node_processing")
builder.add_edge("node_processing", "node_generation")
builder.add_edge("node_generation", END)

graph = builder.compile()

"""
values：每一个节点执行后，流式输出完整的状态
updates：图执行过程中，每一步执行后流式输出增量更新。如果在同一个步当中产生了多个增量更新，这些增量更新会分别流式输出。
custom：流式输出节点内部的自定义数据。
messages：在任何调用了LLM的节点当中，流式输出两元组数据：（LLM Token，metadata）
debug：流式输出所有能输出的信息
混合模式：流模式传入列表，在列表当中添加多种不同的模式，可以得到多种流式输出
"""

for i in graph.stream({"step": "start"}, stream_mode=["values", "custom"]):
    print(i)