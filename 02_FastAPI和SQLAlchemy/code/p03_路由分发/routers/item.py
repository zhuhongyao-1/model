"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["商品管理"]  # 文档中归类为「商品管理」
)

all_items_list = ["鼠标","键盘","显示器","U盘","耳机"]

#定义各个函数，对应url
@router.get("/")
async def get_all_items():
    return all_items_list