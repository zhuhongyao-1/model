"""
    @Author:Irene
    @Time:2026/6/5
    @Desc:
"""
async def func():
    print("hello") #目前是有警告的，因为正常的协程函数中需要有await

if __name__ == "__main__":
    r = func() #不是直接执行函数体的语句，而是给你返回一个协程coroutine对象
    print(r)