"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
from table_2_models import Departments, Employees
from database import SessionLocal

# 向员工和部门表中插入数据
def insert_dept_emp():
    # 1. 创建员工对象
    emp = Employees(name='zs',age=20)

    # 2. 创建部门对象
    dept = Departments(name='研发部',employees=[emp]) # 关联员工

    # 3. 插入数据库
    with SessionLocal() as session:
        try:
            session.add(dept)
            session.commit()
            session.refresh(dept)
            session.refresh(emp)
            print(f"插入成功！部门ID：{dept.id}，员工ID：{emp.id}")
        except Exception as e:
            session.rollback()
            print(f"插入失败：{e}")
if __name__ == "__main__":
    insert_dept_emp()
