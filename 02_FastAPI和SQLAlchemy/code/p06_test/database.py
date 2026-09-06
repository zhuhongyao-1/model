"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL 连接格式：mysql+pymysql://用户名:密码@主机地址:端口/数据库名
url = "mysql+pymysql://root:123456@localhost:3306/fastapi_db"
# 创建数据库引擎, echo=True启用日志输出 开发环境启用，生产环境关闭
engine = create_engine(url, echo=True)
# 配置会话工厂
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)