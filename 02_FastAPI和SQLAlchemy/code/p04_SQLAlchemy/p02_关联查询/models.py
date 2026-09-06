from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float,DECIMAL,Enum,CHAR,Table
from sqlalchemy.dialects.mysql import SET
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# 生成基类，所有模型需继承该类
Base = declarative_base()

#  =========================一对多和多对一=========================================
#所有的实体类必须继承Base类
class Department(Base): #部门模型类
    """部门模型（一对多：一个部门包含多个员工）"""
    __tablename__ = "t_department"   #这个模型类与哪个表对应

    #类的实例属性，与表中的列/字段的对应关系，相关的数据类型，约束，要与表结构对应
    did = Column(Integer, primary_key=True, autoincrement=True) #部门编号
    dname = Column(String(20), nullable=False, unique=True)  # 部门名称
    description = Column(String(200))  # 部门简介

    # 一对多关联员工：返回员工列表
    employees = relationship("Employee", back_populates="department", lazy="selectin")

    #可选，这里重写它是为了方便用print直接打印对象，用于查看结果
    def __repr__(self):
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

    # 多对一关联
    #如果写 back_populates，对方的类中得有 employees属性的定义
    department = relationship("Department", back_populates="employees", lazy="joined")
    #如果写 backref，对方的类中（例如Job）类中不用写 employees，自动生成关联的employees，
    #默认生成的 employees中的关联关系的lazy默认是select，select表示每一条Job记录，都要单独再查询对应的所有员工
    #当我们访问每一个Job中的员工时，都是现查的员工
    job = relationship("Job", backref="employees", lazy="joined")

    def __repr__(self):
        return (f"{self.eid},{self.ename},{self.salary},{self.commission_pct},{self.birthday},"
                f"{self.gender},{self.tel},{self.email},{self.address},{self.work_place},"
                f"{self.hiredate},{self.job_id},{self.mid},{self.did}")

class Job(Base): #职位模型类
    """职位模型（一对多：一个职位包含多个员工）"""
    __tablename__ = "t_job"  #对应表名

    jid = Column(Integer, primary_key=True, autoincrement=True)#职位编号
    jname = Column(String(20), nullable=False, unique=True)  # 职位名称
    description = Column(String(200))  # 职位简介

    def __repr__(self):
        return f"{self.jid},{self.jname},{self.description}"

# ===========================一对一=================================
class User(Base):
    __tablename__ = "t_users"
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String(50))

    # 一对一：用户对应一个资料（uselist=False 表示非集合）
    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False,  # 关键：关联结果为单个对象（非列表）
        # cascade="all, delete-orphan"  # 有all 当删除用户时会删除资料，另外有delete-orphan 当解除user用户与profile关系，也会删除profile对象对应的记录
        # cascade="all, delete"  # 只有删除用户时才会删除资料，如果只是解除user用户与profile关系，不会删除profile对象对应的记录
        cascade="save-update,delete-orphan" #当解除user用户与profile关系，才会删除profile对象对应的记录
    )

    def __repr__(self):
        return f"{self.id},{self.username},{self.profile.bio}"

class Profile(Base):
    __tablename__ = "t_profiles"
    id = Column(Integer, primary_key=True,autoincrement=True)
    bio = Column(String(200))  # 个人简介
    user_id = Column(Integer, ForeignKey("t_users.id"), unique=True)  # 外键唯一

    # 反向关联用户
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"{self.id},{self.bio},{self.user.username}"

# ============================多对多========================================

# 1. 定义中间表（无需模型类，直接用 Table 定义）
student_course = Table(
    "student_course",  # 中间表名
    Base.metadata, #表的元数据信息，表结构的定义
     Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50))

    # 多对多：学生选修多个课程（通过 secondary 指定中间表）
    courses = relationship(
        "Course",
        secondary=student_course,  # 关联中间表
        back_populates="students",
        lazy="selectin"
)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100))

    # 反向关联：课程包含多个学生
    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )
