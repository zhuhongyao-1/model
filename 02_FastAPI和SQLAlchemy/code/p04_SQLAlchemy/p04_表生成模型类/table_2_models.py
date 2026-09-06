from typing import Optional
import datetime
import decimal
import enum

from sqlalchemy import CheckConstraint, Column, DECIMAL, Date, Double, Enum, ForeignKeyConstraint, Index, Integer, String, Table, text
from sqlalchemy.dialects.mysql import CHAR, ENUM, SET, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class TEmployeeGender(str, enum.Enum):
    男 = '男'
    女 = '女'


class Courses(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(VARCHAR(100, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'))

    student: Mapped[list['Students']] = relationship('Students', secondary='student_course', back_populates='course')


class Departments(Base):
    __tablename__ = 'departments'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    employees: Mapped[list['Employees']] = relationship('Employees', back_populates='department')


class Students(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(VARCHAR(50, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'))

    course: Mapped[list['Courses']] = relationship('Courses', secondary='student_course', back_populates='student')


class TDepartment(Base):
    __tablename__ = 't_department'
    __table_args__ = (
        Index('dname', 'dname', unique=True),
    )

    did: Mapped[int] = mapped_column(Integer, primary_key=True, comment='部门编号')
    dname: Mapped[str] = mapped_column(VARCHAR(20, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'), nullable=False, comment='部门名称')
    description: Mapped[Optional[str]] = mapped_column(VARCHAR(200, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'), comment='部门简介')

    t_employee: Mapped[list['TEmployee']] = relationship('TEmployee', back_populates='t_department')


class TJob(Base):
    __tablename__ = 't_job'
    __table_args__ = (
        Index('jname', 'jname', unique=True),
    )

    jid: Mapped[int] = mapped_column(Integer, primary_key=True, comment='职位编号')
    jname: Mapped[str] = mapped_column(VARCHAR(20, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'), nullable=False, comment='职位名称')
    description: Mapped[Optional[str]] = mapped_column(VARCHAR(200, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'), comment='职位简介')

    t_employee: Mapped[list['TEmployee']] = relationship('TEmployee', back_populates='job')


class TUsers(Base):
    __tablename__ = 't_users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(VARCHAR(50, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'))

    t_profiles: Mapped[list['TProfiles']] = relationship('TProfiles', back_populates='user')


class Employees(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='SET NULL', onupdate='CASCADE', name='employees_ibfk_1'),
        Index('department_id', 'department_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    department_id: Mapped[Optional[int]] = mapped_column(Integer)

    department: Mapped[Optional['Departments']] = relationship('Departments', back_populates='employees')


t_student_course = Table(
    'student_course', Base.metadata,
    Column('student_id', Integer, primary_key=True),
    Column('course_id', Integer, primary_key=True),
    ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='RESTRICT', onupdate='RESTRICT', name='student_course_ibfk_2'),
    ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='RESTRICT', onupdate='RESTRICT', name='student_course_ibfk_1'),
    Index('course_id', 'course_id')
)


class TEmployee(Base):
    __tablename__ = 't_employee'
    __table_args__ = (
        CheckConstraint('(`hiredate` > `birthday`)', name='t_employee_chk_2'),
        CheckConstraint('(`salary` > 0)', name='t_employee_chk_1'),
        ForeignKeyConstraint(['did'], ['t_department.did'], ondelete='SET NULL', onupdate='CASCADE', name='t_employee_ibfk_2'),
        ForeignKeyConstraint(['job_id'], ['t_job.jid'], ondelete='SET NULL', onupdate='CASCADE', name='t_employee_ibfk_1'),
        ForeignKeyConstraint(['mid'], ['t_employee.eid'], ondelete='SET NULL', onupdate='CASCADE', name='t_employee_ibfk_3'),
        Index('did', 'did'),
        Index('job_id', 'job_id'),
        Index('mid', 'mid')
    )

    eid: Mapped[int] = mapped_column(Integer, primary_key=True, comment='员工编号')
    ename: Mapped[str] = mapped_column(VARCHAR(20, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'), nullable=False, comment='员工姓名')
    salary: Mapped[decimal.Decimal] = mapped_column(Double(asdecimal=True), nullable=False, comment='薪资')
    birthday: Mapped[datetime.date] = mapped_column(Date, nullable=False, comment='出生日期')
    gender: Mapped[TEmployeeGender] = mapped_column(Enum(TEmployeeGender, values_callable=lambda cls: [member.value for member in cls]), nullable=False, server_default=text("'男'"), comment='性别')
    tel: Mapped[str] = mapped_column(CHAR(11, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'), nullable=False, comment='手机号码')
    email: Mapped[str] = mapped_column(VARCHAR(32, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'), nullable=False, comment='邮箱')
    work_place: Mapped[str] = mapped_column(SET('北京', '深圳', '上海', '武汉', '成都', '西安'), nullable=False, server_default=text("'北京'"), comment='工作地点')
    hiredate: Mapped[datetime.date] = mapped_column(Date, nullable=False, comment='入职日期')
    commission_pct: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(3, 2), comment='奖金比例')
    address: Mapped[Optional[str]] = mapped_column(VARCHAR(150, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'), comment='地址')
    job_id: Mapped[Optional[int]] = mapped_column(Integer, comment='职位编号')
    mid: Mapped[Optional[int]] = mapped_column(Integer, comment='领导编号')
    did: Mapped[Optional[int]] = mapped_column(Integer, comment='部门编号')

    t_department: Mapped[Optional['TDepartment']] = relationship('TDepartment', back_populates='t_employee')
    job: Mapped[Optional['TJob']] = relationship('TJob', back_populates='t_employee')
    t_employee: Mapped[Optional['TEmployee']] = relationship('TEmployee', remote_side=[eid], back_populates='t_employee_reverse')
    t_employee_reverse: Mapped[list['TEmployee']] = relationship('TEmployee', remote_side=[mid], back_populates='t_employee')


class TProfiles(Base):
    __tablename__ = 't_profiles'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['t_users.id'], ondelete='RESTRICT', onupdate='RESTRICT', name='t_profiles_ibfk_1'),
        Index('user_id', 'user_id', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bio: Mapped[Optional[str]] = mapped_column(VARCHAR(200, charset='utf8mb4', collation='utf8mb4_0900_ai_ci'))
    user_id: Mapped[Optional[int]] = mapped_column(Integer)

    user: Mapped[Optional['TUsers']] = relationship('TUsers', back_populates='t_profiles')
