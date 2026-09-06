import aiohttp
import asyncio

async def get_data(session, url):
    async with session.get(url) as response: #响应对象
        content = await response.text() #这是一个耗时的IO操作
        return {
            "url": url,
            "status": response.status,  # 状态码 200=成功
            "content_preview": content[:200] + "..."  # 只展示前200个字符
        }

async def main_func():
    urls = [
        "https://www.baidu.com",
        "https://www.atguigu.com"
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [get_data(session,url) for url in urls]
        results = await asyncio.gather(*tasks)
        for result in results:
            print(result)

if __name__ == "__main__":
    asyncio.run(main_func())
