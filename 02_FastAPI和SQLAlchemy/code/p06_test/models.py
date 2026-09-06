"""
    @Author:Irene
    @Time:2026/6/8
    @Desc:
"""
from sqlalchemy import   Integer, String,Column,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

#这里 Departments不能同时继承 Base 和 BaseModel，如果同时继承会导致冲突
#继承 Base ：与数据库自动映射
#继承 BaseModel：与客户端（浏览器）提交的请求参数自动映射
class Departments(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)  # 部门名称

    # 一对多关联员工：返回员工列表
    employees = relationship("Employees", back_populates="department",lazy="selectin")

class Employees(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)  # 姓名
    age =Column(Integer) #年龄
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL", onupdate="CASCADE"))  # 部门编号

    department = relationship("Departments", back_populates="employees", lazy="selectin")