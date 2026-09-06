"""
    @Author:Irene
    @Time:2026/6/5
    @Desc:
"""
import asyncio
import time
import traceback
from asyncio.exceptions import CancelledError


# 定义子协程任务
async def func(name, delay):
    try:
        print(f"{name}任务开始")
        await asyncio.sleep(delay)  # 休眠，用于模拟一个耗时的任务
        print(f"{name}任务结束")
        return f"{name}结果"
    except CancelledError:
        # traceback.print_exc()
        print(f"{name}任务超时了")


# 定义主协程任务
async def main_coroutine():
    print("启动多个子协程...")

    """
    wait_for本质上也是create_task方式，提交的并发的子协程任务，区别在于，wait_for会有时间限制
    """
    t1=asyncio.create_task(func("A", 5))
    t2=asyncio.create_task(func("B", 10))

    await asyncio.sleep(5)

    t2.cancel("任务B被取消了")

    results = await asyncio.gather(t1, t2)
    print(f"所有结果: {results}")

if __name__ == "__main__":
    start = time.time()

    # 启动主协程任务
    # main_coroutine()表示返回一个协程对象
    # asyncio.run()函数内部会创建一个EventLoop大管家，并且把main_coroutine()返回的协程对象包装为一个Task
    # 然后开始执行这个Task任务
    asyncio.run(main_coroutine())  # 注意：不main_coroutine后面不要少写()

    end = time.time()
    print(f"主任务和子任务的总耗时：{end - start}")