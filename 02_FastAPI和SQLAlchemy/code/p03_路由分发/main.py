"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
from fastapi import FastAPI
from routers import user  # 导入子模块路由
from routers import item

app = FastAPI(title="路由分发示例")

# 挂载用户路由：所有 /users 开头的请求由 user.router 处理
app.include_router(user.router)

# 挂载商品路由：所有 /items 开头的请求由 item.router 处理
app.include_router(item.router)

#定义各个函数，对应url
#对应的url： http://主机地址:端口号/
@app.get("/")
async def hello():
    return "hello"