"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
from typing import Optional
from sqlalchemy import ForeignKeyConstraint, Index, Integer, String,Column,ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

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

    department = relationship("Departments", back_populates="employees", lazy="joined")