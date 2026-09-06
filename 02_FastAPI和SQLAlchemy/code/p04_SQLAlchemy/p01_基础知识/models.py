from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float,DECIMAL,Enum,CHAR
from sqlalchemy.dialects.mysql import SET

from sqlalchemy.ext.declarative import declarative_base

# 生成基类，所有模型需继承该类
Base = declarative_base()

#所有的实体类必须继承Base类
class Department(Base): #部门模型类
    """部门模型（一对多：一个部门包含多个员工）"""
    __tablename__ = "t_department"   #这个模型类与哪个表对应

    #类的实例属性，与表中的列/字段的对应关系，相关的数据类型，约束，要与表结构对应
    did = Column(Integer, primary_key=True, autoincrement=True) #部门编号
    dname = Column(String(20), nullable=False, unique=True)  # 部门名称
    description = Column(String(200))  # 部门简介

    #可选，这里重写它是为了方便用print直接打印对象，用于查看结果
    def __str__(self):
        return f"{self.did},{self.dname},{self.description}"

class Employee(Base): #员工模型类
    """员工模型（多对一：多个员工属于一个部门）"""
    __tablename__ = "t_employee"  #对应表名

    eid = Column(Integer, primary_key=True, autoincrement=True) #员工编号
    ename = Column(String(20), nullable=False)  # 姓名
    salary = Column(Float,nullable=False) #薪资
    commission_pct = Column(DECIMAL) #奖金比例
    birthday = Column(Date,nullable=False) #出生日期
    gender = Column(Enum('男','女'),default='男',nullable=False) #性别
    tel = Column(CHAR(11),nullable=False) #电话
    email = Column(String(32),nullable=False)#邮箱
    address = Column(String(150))#地址
    work_place = Column(SET('北京','深圳','上海','武汉','成都','西安'),default="北京",nullable=False) #工作地点
    hiredate = Column(Date,nullable=False)  # 入职日期
    job_id=Column(Integer,ForeignKey("t_job.jid", ondelete="SET NULL", onupdate="CASCADE")) #职位编号
    mid=Column(Integer,ForeignKey("t_employee.eid", ondelete="SET NULL", onupdate="CASCADE")) #领导编号
    did = Column(Integer,ForeignKey("t_department.did", ondelete="SET NULL", onupdate="CASCADE"))#部门编号

    def __str__(self):
        return (f"{self.eid},{self.ename},{self.salary},{self.commission_pct},{self.birthday},"
                f"{self.gender},{self.tel},{self.email},{self.address},{self.work_place},"
                f"{self.hiredate},{self.job_id},{self.mid},{self.did}")

class Job(Base): #职位模型类
    """职位模型（一对多：一个职位包含多个员工）"""
    __tablename__ = "t_job"  #对应表名

    jid = Column(Integer, primary_key=True, autoincrement=True)#职位编号
    jname = Column(String(20), nullable=False, unique=True)  # 职位名称
    description = Column(String(200))  # 职位简介

    def __str__(self):
        return f"{self.jid},{self.jname},{self.description}"