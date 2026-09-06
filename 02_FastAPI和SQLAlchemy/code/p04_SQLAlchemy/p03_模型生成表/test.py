"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
from sqlalchemy import create_engine
from models import Base,Employees,Departments #必须要加

# 创建数据库引擎
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/fastapi_db", echo=True)

# 创建表
def create_table():
    print("注册的表名:", Base.metadata.tables.keys())
    # 创建所有模型对应的表
    Base.metadata.create_all(bind=engine)
    print("表创建成功")

if __name__ == '__main__':
    create_table()