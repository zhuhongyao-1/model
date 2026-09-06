"""
    @Author:Irene
    @Time:2026/6/5
    @Desc:
"""
import asyncio
import time


#定义子协程任务
async def func(name,delay):
    print(f"{name}任务开始")
    """
    当A任务这里遇到await，又隐式的把asyncio.sleep(delay)包装为一个Task，注册到EventLoop大管家，
    但是它是一个耗时的IO操作，即很慢。
    当前A任务被挂起了，然后EventLoop大管家去执行其他已就绪的任务，目前没有，只能等着。
    等到asyncio.sleep(delay)完事，操作系统会通知EventLoop，该任务完事了，
    A任务恢复了，回到就绪状态，可以执行了，继续执行下面的代码print(f"{name}任务结束")
    """
    await asyncio.sleep(delay) #休眠，用于模拟一个耗时的任务
    print(f"{name}任务结束")


#定义主协程任务
async def main_coroutine():
    print("启动多个子协程...")
    #如果是串行，这里使用await，注册子协程任务
    """
    
    main_coroutine主协程任务遇到await之后，会隐式的把func("A", 5)返回的协程对象包装为一个Task，注册到EventLoop大管家
    紧接着main_coroutine被挂起了，然后EventLoop大管家去执行其他已就绪的任务，目前就是func("A", 5)。
    等到A任务结束后。main_coroutine恢复了，就可以继续往下走，遇到await func("B", 5)，开始执行B
    """
    await func("A", 5)
    await func("B", 5)

if __name__ == "__main__":
    start = time.time()

    #启动主协程任务
    # main_coroutine()表示返回一个协程对象
    #asyncio.run()函数内部会创建一个EventLoop大管家，并且把main_coroutine()返回的协程对象包装为一个Task
    #然后开始执行这个Task任务
    asyncio.run(main_coroutine()) #注意：不main_coroutine后面不要少写()

    end = time.time()
    print(f"主任务和子任务的总耗时：{end-start}")