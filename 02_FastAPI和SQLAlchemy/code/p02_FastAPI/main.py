"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
from fastapi import FastAPI

import uvicorn

app = FastAPI() #表示创建了一个服务器的应用程序，它可以接收所有客户端的请求

#下面需要定义函数来接收客户端的不同的请求
#可以写同步的函数，也可以写异步的函数

#url的结构：http://主机地址:端口号/请求资源
@app.get("/")  #请求路径，http://主机地址:端口号/，例如：http://127.0.0.1:8000/
async def root():
    return {"message": "Hello World"}  #返回给客户端的内容
    #目前没有具体的HTML页面，只是返回一个文本字符串，以JSON串的形式返回。
    #如果想要返回页面，图片等，这里返回的是 页面的文件（即xxx.html），例如：index.html

#例如：http://127.0.0.1:8000/hello/xxx
#请求路径：http://主机地址:端口号/hello/xxx，这里的xxx就会被赋值给name路径参数的变量
#("/hello/{name}") 中{name}名称要与say_hello(name: str)函数参数的变量名相同，可以有1个或多个
#如果say_hello(name: str)的形参没有指定默认值，那么代表这个路径参数是必填的，
# 如果现在请求 http://127.0.0.1:8000/hello，会发生  "detail": "Not Found"后台404报错
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}   #返回给客户端的内容

@app.get("/hi") #固定的路径值，不带路径参数变量
async def say_hi():
    return {"message": f"hi"}   #返回给客户端的内容

@app.get("/item/iphone") #固定的路径值，不带路径参数变量
async def say_hi(): #这里的函数名与上一个函数名重名，虽然语法上允许，但是最好能取不同的函数名称。但是2个函数的@的路径值必须不同
    return {"message": f"固定的iphone"}   #返回给客户端的内容

@app.get("/item/{id}") #带路径参数变量
async def get_item_by_id(id:int):
    return {"message": f"item的id值{id}，id的类型：{type(id)}"}   #返回给客户端的内容

# @app.get("/item/{name}") #与上面的@app.get("/item/{id}")无法区分
@app.get("/items/{name}")
async def get_items_by_name(name:str):
    return {"message": f"item的name是{name}"}   #返回给客户端的内容

all_items_list = ["鼠标","键盘","显示器","U盘","耳机"]
all_items_dict = {"mouse": 96, "键盘": 100, "computer": 900, "U": 128, "ear": 23}

#如果查询参数没有默认值，表示必选的
#http://127.0.0.1:8000/items?start=1&end=3
#start与end的顺序随意，因为它们是通过参数名找形参的，相当于是关键字传参
# @app.get("/items")
# async def get_some_items(start:int,end:int):
#     return {"itmes": all_items_list[start:end]}

# @app.get("/items")
# async def get_some_items(start:int=0,end:int=len(all_items_list)):
#     return {"itmes": all_items_list[start:end]}

# @app.get("/items")
# async def get_some_items_name(name:str=None):
#     if name and name in all_items_dict:
#         return {"item":all_items_dict[name]}
#     else:
#         return {"item": "不存在"}

# @app.get("/items")
# async def get_some_items_flag(flag:bool=False):
#     if flag:
#         return "真"
#     else:
#         return "假"


#如果get_some_items()函数的形参没有默认值，那么顺序随意；如果部分有默认值，那么默认值参数在后面
#在url中http://127.0.0.1:8000/items/computer/atguigu, computer对应("/items/{name}/{info}")的name，atguigu对应info，按照位置对应
#在url中?end=8&start=4&flag=1 与 get_some_items()形参的顺序无所谓，因为它们是按照关键字传参
# @app.get("/items/{name}/{info}")
# async def get_some_items(name:str,info:str,flag:bool,start:int=0,end:int=len(all_items_list)):
#     result = {}
#     if flag:
#         result.update({"flag":"真"})
#     else:
#         result.update({"flag":"假"})
#
#     if name and name in all_items_dict:
#         result.update({"item":all_items_dict[name]})
#     else:
#         result.update({"item": "不存在"})
#
#     result.update({"info": info})
#     result.update({"items":all_items_list[start:end]})
#     return result

"""
    参数分为3种：
    （1）路径参数：  http://服务器的主机地址:端口号/路径参数1/路径参数2
    （2）查询参数：  http://服务器的主机地址:端口号/路径参数1/路径参数2?查询参数名1=值&查询参数名2=值
                 上面的2种参数请求方式可以对应Get
    （3）请求参数：  封装在请求体中，不会在URL地址栏中展示，请求方式对应的是POST，PUT,DELETE等
"""

# 定义数据模型类，需要继承 BaseModel 的类。
from pydantic import BaseModel

class Item(BaseModel): #所有的实体类，继承 BaseModel类
    #下面定义的都是实例属性，继承BaseModel类允许使用以下精简的方式定义实例属性
    name: str
    desc: str | None = None
    price: float

@app.post("/items/") #注意请求方式是post（post方式请求的数据在地址栏不会显示）
async def create_item(item: Item):
    return item



