"""
    测试：节点函数的输入
    节点函数可以有三个参数：状态，配置，运行时对象
"""
from typing import TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

class ContextTest:
    def invoke(self):
        print("hello world")

class MyState(TypedDict):
    key: str
    a1: str
    a2: str
    a3: str
    a4: str

def node_test(state : MyState, config : RunnableConfig, runtime : Runtime):
    """
        graph.invoke(init_state, config=config, context=context)
        init_state:初始化状态
        config:对应节点函数的config参数，在调用图对象时会将config封装为RunnableConfig
        context:对应节点函数的runtime参数，在调用图对象时会将context封装为Runtime
    """
    user_id = config["configurable"]["user_id"]
    print("config中的user_id:", user_id)

    context_test = runtime.context["context_test"]
    context_test.invoke()

    return {"key": "value"}

builder = StateGraph(MyState)

builder.add_node(node_test)

builder.add_edge(START, "node_test")
builder.add_edge("node_test", END)

graph = builder.compile()

# 初始化状态
init_state = {}

# 设置配置信息，对应节点函数的config参数
config = {
    "configurable":{
        "user_id": 1001
    }
}

# 设置上下文信息，对应节点函数的runtime参数
context = {
    "context_test": ContextTest()
}

result = graph.invoke(init_state, config=config, context=context)
print(result)