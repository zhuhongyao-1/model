"""
    @Author:Irene
    @Time:2026/6/5
    @Desc:
"""
import asyncio
import time


# 定义子协程任务
async def func(name, delay):
    print(f"{name}任务开始")
    #
    # await time.sleep(delay)  #用sleep函数的结果作为协程对象，但是sleep函数是普通函数，不会返回协程对象
    event_loop = asyncio.get_event_loop() #获取的是EventLoop大管家对象
    #None代表使用默认的线程池对象
    await event_loop.run_in_executor(None,time.sleep,delay)
       # 同步的休眠。如果没有特殊的隔离阻塞处理，会导致EventLoop的并发能力消失
    print(f"{name}任务结束")


# 定义主协程任务
async def main_coroutine():
    print("启动多个子协程...")

    """
    asyncio.create_task这种方式是并发注册任务。
    当main_coroutine遇到 asyncio.create_task(func("A", 5))，
        会把func("A", 5)协程对象包装为一个Task，然后注册到EventLoop大管家中。
        它不会把main_coroutine挂起来。
        目前就有2个就绪任务；main_coroutine() 和 func("A", 5)
    main_coroutine继续执行，遇到asyncio.create_task(func("B", 5))，
        会把func("B", 5)协程对象包装为一个Task，然后注册到EventLoop大管家中。
        它不会把main_coroutine挂起来。
        目前就有3个就绪任务；main_coroutine() 和 func("A", 5)、func("B", 5)
    """
    t1=asyncio.create_task(func("A", 5))
    t2=asyncio.create_task(func("B", 6))

    #如果EventLoop发现它的顶级Task(main_coroutine)已经完成，它立即触发退出机制。
    #此时EventLoop强制取消所有仍在运行的子Task，然后关闭EventLoop，程序退出。
    #await asyncio.gather()会把主协程挂起来，等所有的子协程任务(t1,t2)完成后，返回结果，如果没有子协程任务函数没有返回值，就返回None
    results = await asyncio.gather(t1,t2)
    print(results)


if __name__ == "__main__":
    start = time.time()

    # 启动主协程任务
    # main_coroutine()表示返回一个协程对象
    # asyncio.run()函数内部会创建一个EventLoop大管家，并且把main_coroutine()返回的协程对象包装为一个Task
    # 然后开始执行这个Task任务
    asyncio.run(main_coroutine())  # 注意：不main_coroutine后面不要少写()

    end = time.time()
    print(f"主任务和子任务的总耗时：{end - start}")