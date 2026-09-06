"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
from database import SessionLocal
from models import Employee,Department,Job,User,Profile,Student,Course
from sqlalchemy.orm import joinedload

def read_data_all_emp():
    # 获取会话
    session = SessionLocal()
    try:
        # 多对一
        # ======查询所有员工========
        # 加载员工时同时加载对应的部门信息
        employees = session.query(Employee).all()
        for emp in employees:
            print(f"{emp.ename}"
                  f",部门：{emp.department.dname if emp.department else "无部门"}，"
                  f",职位：{emp.job.jname if emp.job else "无职位"}")
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_all_dept():
    # 获取会话
    session = SessionLocal()
    try:
        # 一对多
        # ======查询所有部门及其该部门的员工========
        departments = session.query(Department).all()
        # for dept in departments:
        #     print(f"{dept.dname}")
        #     employees = dept.employees
        #     print(f"\t{[emp.ename for emp in employees]}")

        for dept in departments:
            print(dept,dept.employees)
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_all_jop():
    # 获取会话
    session = SessionLocal()
    try:
        #一对多
        # ======查询所有职位========
        jobs = session.query(Job).all()
        for job in jobs:
            print(f"{job.jname}")
            employees = job.employees
            print(f"\t{[emp.ename for emp in employees]}")
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def one_by_one():
    # 获取会话
    session = SessionLocal()
    try:
        # 方式1：先创建用户，再创建资料并关联
        user1 = User(username="alice")
        session.add(user1)
        session.commit()  # 先提交用户，获取 ID
        session.refresh(user1)

        profile1 = Profile(bio="喜欢读书", user_id=user1.id)  # 通过 user_id 关联
        session.add(profile1)
        session.commit()

        # 方式2：直接通过 relationship 关联（更简洁）
        user2 = User(
            username="bob",
            profile=Profile(bio="热爱运动")  # 直接嵌套 Profile 对象
        )
        session.add(user2)
        session.commit()  # 自动同步 user_id

        user3 = User(
            username="Lucy",
            profile=Profile(bio="喜欢跳舞")  # 直接嵌套 Profile 对象
        )
        session.add(user3)
        session.commit()  # 自动同步 user_id
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def select_user():
    # 获取会话
    session = SessionLocal()
    try:
        users = session.query(User).all()
        print(users)
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def delete_orphan():
    # 获取会话
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.username=="bob").first()
        print(f"用户名：{user.username}，爱好：{user.profile.bio}")
        user.profile = None #解除关系
        print(f"解除关系用户名：{user.username}，爱好：{user.profile}")
        session.refresh(user)
        session.commit()

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"执行失败：{e}")
    finally:
        session.close()  # 关闭会话

def delete_user():
    # 获取会话
    session = SessionLocal()
    try:
        # user = session.query(User).filter(User.username=="alice").first()
        user = session.query(User).filter(User.username=="Lucy").first()
        print(f"用户名：{user.username}，爱好：{user.profile.bio}")
        session.delete(user) #删除用户
        session.commit()

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"执行失败：{e}")
    finally:
        session.close()  # 关闭会话

def many_to_many():
    # 获取会话
    session = SessionLocal()
    try:
        # 创建学生和课程
        student1 = Student(name="张三")
        student2 = Student(name="李四")
        course1 = Course(name="数学")
        course2 = Course(name="英语")

        # 建立关联
        student1.courses = [course1, course2] #学生张三选择了2门课
        student2.courses = [course1] #学生李四只选1门课

        #添加的时候，直接查询出关联的对象
        session.add_all([student1, student2, course1, course2])
        session.commit()

        # 查询：学生张三选修的课程
        print([c.name for c in student1.courses])

        # 查询：数学课程包含的学生
        print([s.name for s in course1.students])
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

if __name__ == "__main__":
    # read_data_all_dept()
    # read_data_all_emp()
    # read_data_all_jop()

    # one_by_one()
    # select_user()
    # delete_orphan()
    # delete_user()

    many_to_many()