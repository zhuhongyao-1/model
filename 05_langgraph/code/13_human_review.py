"""
    测试：LangGraph实现人工审核
"""
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command


class TransferState(TypedDict):
    recipient: str # 接收者
    amount: int # 金额
    memo: str # 备注
    approved: bool # 审核结果
    final_status: str # 最终状态

def review_transfer(state: TransferState):
    # 获取当前的转账信息
    pendding_transfer = {
        "recipient": state["recipient"],
        "amount": state["amount"],
        "memo": state["memo"],
    }
    # 使用interrupt()设置中断（暂停）操作，添加人工审核
    # 此时用户审核的结果会直接赋值user_review
    # user_review有两种模式：1、直接返回bool 2、返回dict{approved:bool,recipient:"xxx",amount:"xxx",memo:"xxx"}
    user_review = interrupt({
        "title":"转账审核",
        "pendding_transfer": pendding_transfer,
        "instruction": "请返回 bool(是否批准) 或 dict(可改 recipient/amount/memo，并带 approved 字段)。",
    })

    # 表示要修改的转账信息
    updated_transfer = pendding_transfer
    # 表示审核的结果bool
    approved = False

    if isinstance(user_review, bool):
        approved = user_review
    elif isinstance(user_review, dict):
        approved = user_review["approved"]
        for i in ("recipient", "amount", "memo"):
            if i in user_review:
                updated_transfer[i] = user_review[i]

    print(f"[Node] review_transfer：用户审核结果 approved={approved}，transfer={updated_transfer}")

    return {
        "approved": approved,
        "recipient": updated_transfer["recipient"],
        "amount": updated_transfer["amount"],
        "memo": updated_transfer["memo"],
    }

def review_result(state: TransferState):
    if not state["approved"]:
        # 用户审核不通过
        return {"final_status":"审核不通过"}
    recipient = state["recipient"]
    amount = state["amount"]
    memo = state["memo"]
    return {"final_status":f"用户审核通过：接收者{recipient},金额{amount},备注{memo}"}

builder = StateGraph(TransferState)

builder.add_node(review_transfer)
builder.add_node(review_result)

builder.add_edge(START, "review_transfer")
builder.add_edge("review_transfer", "review_result")
builder.add_edge("review_result", END)

graph = builder.compile(checkpointer=InMemorySaver())

initial_state: TransferState = {
    "recipient": "Alice",
    "amount": 100,
    "memo": "午饭AA",
    "approved": False,
    "final_status": "",
}

config = {
    "configurable":{
        "thread_id":"abc"
    }
}

# 第一次执行图对象，会因为转账节点中断
result = graph.invoke(initial_state, config=config)
print("节点执行中断，原因：")
print(result["__interrupt__"][0].value)

# 进行人工审核的答复
# user_review_result = True
# user_review_result = False
user_review_result={
    "approved":True,
    "recipient":"Jack",
    "amount":1000,
    "memo":"晚上请客"
}
result = graph.invoke(Command(resume=user_review_result),config=config)
print(result)
