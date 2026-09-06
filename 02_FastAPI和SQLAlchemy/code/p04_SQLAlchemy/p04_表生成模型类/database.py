"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# 创建数据库引擎
url = "mysql+pymysql://root:123456@localhost:3306/fastapi_db"
engine = create_engine(url, echo=True)
# 配置会话工厂
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)