"""
    @Author:Irene
    @Time:2026/6/6
    @Desc:
"""
import subprocess
import sys
from database import url

# 生成模型类
def table_2_model(run=False):
    """将数据库表映射为Python类"""
    if not run:
        return
    output_path = "table_2_models.py"

    venv_python = sys.executable  # 若PyCharm使用虚拟环境，这里会返回.venv下的python.exe
    print("当前使用的Python路径：", venv_python)  # 确认输出是.venv/Scripts/python.exe

    cmd = [venv_python,
           "-m","sqlacodegen",
            # "--tables", "departments,employees", #如果没有指定table，就会把数据库中的所有表生成模型类
           url]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

    # 打印执行结果（定位问题核心）
    print("=== 命令执行结果 ===")
    print(f"返回码（0=成功，非0=失败）：{result.returncode}")
    print(f"标准输出：\n{result.stdout}")
    print(f"错误输出：\n{result.stderr}")  # 重点看这里，会显示失败原因

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.stdout)

if __name__ == "__main__":
    table_2_model(True)
