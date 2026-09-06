"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
from models import Department,Employee
from database import SessionLocal
from datetime import date
from sqlalchemy import and_, or_,func,text

def insert_department_data():
    # 获取数据库会话，与数据库建立连接
    session = SessionLocal()

    try:
        # =========== 第一步：新增部门 =============
        new_dept = Department(dname="安保部", description="负责公司安保工作")
        session.add(new_dept)  # 将部门对象加入会话，即把这个对象添加到对应的表中，底层就会生成一条insert语句
        session.commit()  # 提交到数据库（执行 INSERT 语句）
        session.refresh(new_dept)  # 刷新对象，获取自增的 id 等字段
        # ===================== 输出结果 =====================
        print(f"新增部门：ID={new_dept.did}，名称={new_dept.dname}，描述={new_dept.description}")

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"新增失败：{e}")
    finally:
        session.close()  # 关闭会话

def insert_employee_data():
    # 获取数据库会话，与数据库进行连接
    session = SessionLocal()

    try:
        # =========== 第二步：新增关联的员工 ===========
        # 员工1：关联上面创建的安保部
        emp1 = Employee(
            ename="张三",
            salary = 15000,
            birthday = date(1995,5,1),
            gender = "男",
            tel = "18396587548",
            email = "zhangsan@atguigu.com",
            hiredate=date(2023, 1, 1),
            did=7
        )
        # 员工2：同部门的另一个员工
        emp2 = Employee(
            ename="李四",
            salary = 15000,
            birthday = date(1996,6,1),
            gender = "男",
            tel = "18396587546",
            email = "lisi@atguigu.com",
            work_place="北京,深圳",
            hiredate=date(2023, 1, 1),
            did=7
        )

        # 员工3：其他部门的另一个员工
        emp3 = Employee(
            ename="王五",
            salary = 15000,
            birthday = date(1996,6,1),
            gender = "男",
            tel = "18396587545",
            email = "wangwu@atguigu.com",
            work_place="北京,深圳",
            hiredate=date(2023, 1, 1),
            did=1
        )

        # 批量添加员工（也可逐个 add）
        session.add_all([emp1, emp2,emp3])
        session.commit()  # 提交员工数据
        # 刷新员工对象，获取自增 ID
        session.refresh(emp1)
        session.refresh(emp2)
        session.refresh(emp3)

        print(f"新增员工1：ID={emp1.eid}，姓名={emp1.ename}，所属部门={emp1.did}")
        print(f"新增员工2：ID={emp2.eid}，姓名={emp2.ename}，所属部门={emp2.did}")
        print(f"新增员工3：ID={emp3.eid}，姓名={emp3.ename}，所属部门={emp3.did}")


    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"新增失败：{e}")
    finally:
        session.close()  # 关闭会话

def delete_employee_data():
    # 获取会话
    session = SessionLocal()
    try:
        # 删除单个员工对象
        emp = session.query(Employee).filter(Employee.ename == "王五").first() #first()表示查询单个对象。如果结果有多个，也只取第1个
        if emp:#如果王五这个员工存在，就删除它
            session.delete(emp) #删除对象
            session.commit() #提交事务
            print(f"已删除员工：{emp.ename}")

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"刪除失败：{e}")
    finally:
        session.close()  # 关闭会话

def delete_department_data():
    # 获取会话
    session = SessionLocal()

    try:
        # 删除部门
        dept = session.query(Department).filter(Department.dname == "安保部").first()
        if dept:
            session.delete(dept)
            session.commit()
            print(f"已删除部门：{dept.dname}")
            #查看员工表，安保部门的员工的did此时为NULL了

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"刪除失败：{e}")
    finally:
        session.close()  # 关闭会话

def update_employee_data():
    # 获取会话
    session = SessionLocal()
    try:
        # 修改员工薪资
        emp = session.query(Employee).filter(Employee.ename == "张三").first()
        if emp:
            print(f"修改前{emp.ename}薪资：{emp.salary}")
            emp.salary += 2000  # 把从数据库查询的对象属性直接修改并且提交即可
            print(f"修改后{emp.ename}薪资：{emp.salary}")
            session.commit()  # 提交更新

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"修改失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_by_primary_key():
    # 获取会话
    session = SessionLocal()
    try:
        # ======按主键查询 get========
        #  查询id=1的部门
        dept = session.get(Department, 1)
        print(f"部门 ID=1：{dept.dname}（{dept.description}）")
    except Exception as e:
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_by_filter():
    # 获取会话
    session = SessionLocal()
    try:
        # ======过滤（filter）查询========
        emp = session.query(Employee).filter(Employee.eid == 1).first()
        print("员工编号为1的员工：",emp)

        # 查询研发部的所有员工 ,按部门ID过滤
        employees = session.query(Employee).filter(Employee.did == 1).all()
        print("研发部员工：")
        for e in employees:
            print(e)

        # 查询薪资大于15000的员工
        employees = session.query(Employee).filter(Employee.salary > 15000).all()
        print("薪资>15000的员工：")
        for e in employees:
            print(e)
    except Exception as e:
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_and_or():
    # 获取会话
    session = SessionLocal()
    try:
        # ======逻辑运算（and_/or_）查询========
        # 薪资[10000,15000]且属于研发部的员工（and_）
        employees = session.query(Employee).filter(and_(Employee.salary.between(10000, 15000), Employee.did == 1)).all()
        print("符合[10000,15000]且属于研发部条件的员工：")
        for e in employees:
            print(e)

        # 属于2号部门或薪资高于20000的员工（or_）
        employees = session.query(Employee).filter(or_(Employee.did == 2, Employee.salary > 20000)).all()
        print("符合属于2号部门或薪资高于20000条件的员工：")
        for e in employees:
            print(e)
    except Exception as e:
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_distinct():
    # 获取会话
    session = SessionLocal()
    try:
        # ======去重（distinct）========
        # 查询所有有员工的部门编号（去重）
        dids = session.query(Employee.did).distinct().all()  # distinct() 去重
        print("部门编号：", dids)

    except Exception as e:
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_group_by():
    # 获取会话
    session = SessionLocal()
    try:
        # ======分组查询========
        results = session.query(Employee.did,
                                func.max(Employee.salary).label("max_salary"), #label表示取别名
                                   func.avg(Employee.salary).label("avg_salary")
                                   ).group_by(Employee.did)

        # 获取所有字段信息列表
        # cols = results.column_descriptions
        # field_names = [col['name'] for col in cols]
        # print(field_names)
        for row in results:
            print(row)
    except Exception as e:
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话


def read_data_subquery():
    # 获取会话
    session = SessionLocal()
    try:
        # ======子查询（subquery）========
        # 步骤1：子查询：查询最高薪资值
        max_salary = session.query(func.max(Employee.salary).label("max_salary")).subquery()  # 转为子查询
        # 步骤2：主查询  ，子查询对象.c.字段名
        emps = session.query(Employee).filter(Employee.salary == max_salary.c.max_salary).all() #筛选薪资最高的员工

        print("薪资最高的员工：")
        for emp in emps:
            print(emp)
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_inner_join():
    # 获取会话
    session = SessionLocal()
    try:
        # ======表连接（join）查询========
        # 内连接：查询员工及其所属部门名称
        # query(A表，B表).join(A或B表, 关联条件)
        #如果是内连接，join里面写A表或B表都可以
        # result = session.query(Employee, Department)\
        #                 .join(Department, Employee.did == Department.did)\
        #                 .all()
        result = session.query(Employee, Department) \
                        .join(Employee, Employee.did == Department.did) \
                        .all()
        for emp, dept in result:
            print(f"{emp.eid:<5}\t{emp.ename:<5}\t{emp.salary:<8}\t{dept.did:<5}\t{dept.dname:<5}")
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_left_join():
    # 获取会话
    session = SessionLocal()
    try:
        # ======表连接（join）查询========
        # 左连接：查询员工及其所属部门名称，包括那些没有部门的员工
        # query(A表，B表).outerjoin(B表, 关联条件) 查询A
        # 左连接 outerjoin()里面写B，就表示 A left join B 查询A
        # 左连接 outerjoin()里面写A，就表示 B left join A 查询B
        # left_result = session.query(Employee, Department)\
        #                 .outerjoin(Department, Employee.did == Department.did)\
        #                 .all()

        # for emp, dept in left_result:
        #     if dept:
        #         print(f"{emp.eid:<5}\t{emp.ename:<5}\t{emp.salary:<8}\t{dept.did:<5}\t{dept.dname:<5}")
        #     else:
        #         print(f"{emp.eid:<5}\t{emp.ename:<5}\t{emp.salary:<8}\t无部门")

        left_result = session.query(Employee, Department)\
                        .outerjoin(Employee, Employee.did == Department.did)\
                        .all()

        for emp, dept in left_result:
            if emp:
                print(f"{emp.eid:<5}\t{emp.ename:<5}\t{emp.salary:<8}\t{dept.did:<5}\t{dept.dname:<5}")
            else:
                print(f"无员工\t{dept.did:<5}\t{dept.dname:<5}")

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_right_join():
    # 获取会话
    session = SessionLocal()
    try:
        # ======表连接（join）查询========
        # 右连接：查询员工及其所属部门名称
        # query(A表，B表).join(A表, 关联条件, isouter=True) 查询B   A right join B
        # query(A表，B表).join(B表, 关联条件, isouter=True) 查询A  B right join A
        # 查询所有部门
        # right_result = session.query(Employee, Department)\
        #                 .join(Employee, Employee.did == Department.did,isouter=True)\
        #                 .all()
        # for emp, dept in right_result:
        #     if emp:
        #         print(f"{emp.eid:<5}\t{emp.ename:<5}\t{emp.salary:<8}\t{dept.did:<5}\t{dept.dname:<5}")
        #     else:
        #         print(f"无员工\t{dept.did:<5}\t{dept.dname:<5}")

        # 查询所有员工
        # right_result = session.query(Employee, Department) \
        #     .join(Department, Employee.did == Department.did, isouter=True) \
        #     .all()
        # for emp, dept in right_result:
        #     if dept:
        #         print(f"{emp.eid:<5}\t{emp.ename:<5}\t{emp.salary:<8}\t{dept.did:<5}\t{dept.dname:<5}")
        #     else:
        #         print(f"{emp.eid:<5}\t{emp.ename:<5}\t{emp.salary:<8}\t无部门")

        # 或 query(A表，B表).select_from(B).outerjoin(A表, 关联条件) 查询B   A right join B
        # 或 query(A表，B表).select_from(A).outerjoin(B表, 关联条件) 查询A   B right join A
        # 查询所有部门
        # right_result = session.query(Employee, Department) \
        #                     .select_from(Department) \
        #                     .outerjoin(Employee, Employee.did == Department.did) \
        #                     .all()

        # for emp, dept in right_result:
        #     if emp:
        #         print(f"{emp.eid:<5}\t{emp.ename:<5}\t{emp.salary:<8}\t{dept.did:<5}\t{dept.dname:<5}")
        #     else:
        #         print(f"无员工\t{dept.did:<5}\t{dept.dname:<5}")

        #查询所有员工
        right_result = session.query(Employee, Department) \
            .select_from(Employee) \
            .outerjoin(Department, Employee.did == Department.did) \
            .all()
        for emp, dept in right_result:
            if dept:
                print(f"{emp.eid:<5}\t{emp.ename:<5}\t{emp.salary:<8}\t{dept.did:<5}\t{dept.dname:<5}")
            else:
                print(f"{emp.eid:<5}\t{emp.ename:<5}\t{emp.salary:<8}\t无部门")

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_full_join():
    # 获取会话
    session = SessionLocal()
    try:
        # ======表连接（join）查询========
        # 全连接：查询员工及其所属部门名称
        # query(A表，B表).join(B表, 关联条件, full=True) A表 full outer join B表
        # full_result = session.query(Employee, Department) \
        #     .join(Department, Employee.did == Department.did, full=True) \
        #     .all()
        # 但是MySQL不支持，所以需要使用union
        full_result = session.query(Employee, Department)\
                        .outerjoin(Department, Employee.did == Department.did)\
                        .union(
                            session.query(Employee, Department)\
                                .select_from(Department)\
                                .outerjoin(Employee, Employee.did == Department.did)
                        ).all()
        for emp, dept in full_result:
            print(emp,dept)
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

def read_data_by_sql():
    # 获取会话
    session = SessionLocal()
    try:
        # ======基于原生SQL查询========
        # 查询每一个部门的人数
        result = session.execute(
                text("""
                        SELECT dname,count(eid)
                        FROM t_employee e RIGHT JOIN t_department d 
                        ON e.did = d.did
                        group by dname
                    """)
                    ).all()
        print("查询结果是：",result)
    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

if __name__ == "__main__":
    # insert_department_data()
    # insert_employee_data()
    # delete_employee_data()
    # delete_department_data()
    # update_employee_data()

    # read_data_by_primary_key()
    # read_data_by_filter()
    # read_data_and_or()
    # read_data_distinct()
    # read_data_group_by()
    # read_data_subquery()
    # read_data_inner_join()
    # read_data_left_join()
    # read_data_right_join()
    # read_data_full_join()
    read_data_by_sql()