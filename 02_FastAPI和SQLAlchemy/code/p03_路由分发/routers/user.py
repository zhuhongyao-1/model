"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
from fastapi import APIRouter
# from main import app #出现循环导入的问题


# 实例化一个 APIRouter，可指定前缀（所有路由自动加上 /users）
router = APIRouter(
    prefix="/users",
    tags=["用户管理"]  # 文档中归类为「用户管理」
)

users_list = ["chai","lin","yan"]

#定义各个函数，对应url
#对应的url： http://主机地址:端口号/users/
# @app.get("/")
@router.get("/")
async def get_all_users():
    return users_list

#对应的url： http://主机地址:端口号/users/
# @app.get("/some")
@router.get("/some")
async def get_some_users(start:int=0, end:int=3):
    return users_list[start:end]
