"""
    @Author:Irene
    @Time:2026/6/8
    @Desc:
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Departments
from database import SessionLocal

app = FastAPI()

def get_session():
    session = None
    try:
        session = SessionLocal()
        yield session
    finally:
        if session:
            session.close()

#session:Session= Depends(get_session)使用SQLAlchemy的依赖自动注入
#当用户请求发过来之后，执行add_department函数时，指定帮我们调用get_session函数，获取session对象
#调用结束之后，自动是否资源
@app.post("/departments/add") #固定的路径参数
def add_department(name:str, session:Session= Depends(get_session)): #只要是post方式，name就是请求参数
    try:
        #把这个接收的部门对象，存到数据库中
        # department = Departments(name) #改成自己new对象，位置传参和关键字传参，这个写法是位置传参
        department = Departments(name=name) #改成自己new对象，位置传参和关键字传参，这个写法是关键字传参
        session.add(department)
        session.commit()
        session.refresh(department)
        return {"result":"success","department":department}
    except:
        session.rollback()
        return "fail"

@app.get("/departments/get")
def get_department_by_id(id:int, session:Session= Depends(get_session)): #上面是get，id就是查询参数
    department = session.get(Departments,id)
    return department

@app.get("/departments/all")
def get_all_departments(session:Session= Depends(get_session)):
    return session.query(Departments).all()

@app.delete("/departments/rm")
def delete_by_id(id:int, session:Session= Depends(get_session)):
    try:
        department = session.get(Departments, id)
        session.delete(department)
        session.commit()
        return f"删除{id}部门成功"
    except:
        session.rollback()
        return "删除失败"

@app.put("/departments/update")
def update_department(id:int,name:str, session:Session= Depends(get_session)):
    try:
        department = session.get(Departments, id) #先从数据库查询这个对象
        department.name = name #直接修改属性
        session.commit()#然后重新提交新修改的属性值
        #下面的方式不对，是因为这个对象没有与数据库建立连接，没办法把新的数据更新到数据库
        # department = Departments(id=id,name=name)
        # session.refresh(department)
        # session.commit()
        return f"修改{id}部门成功"
    except:
        session.rollback()
        return "修改失败"

