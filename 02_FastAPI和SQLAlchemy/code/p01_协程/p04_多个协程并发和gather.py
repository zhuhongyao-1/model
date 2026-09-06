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
    """
    当A任务这里遇到await，又隐式的把asyncio.sleep(delay)包装为一个Task，注册到EventLoop大管家，
    但是它是一个耗时的IO操作，即很慢。
    当前A任务被挂起了，然后EventLoop大管家去执行其他已就绪的任务，执行main_coroutine（它会再启动B）
    
    当B任务这里遇到await，又隐式的把asyncio.sleep(delay)包装为一个Task，注册到EventLoop大管家，
    但是它是一个耗时的IO操作，即很慢。
    当前B任务被挂起了，然后EventLoop大管家去执行其他已就绪的任务，执行main_coroutine（如果没有await asyncio.sleep(6)，主协程就结束了）
    
    当阻塞A的asyncio.sleep(delay)事件完成之后，A会继续
    当阻塞B的asyncio.sleep(delay)事件完成之后，B会继续
    但是它们必须在main_coroutine结束之前进行，否则会被取消任务。
    """
    await asyncio.sleep(delay)  # 休眠，用于模拟一个耗时的任务
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