"""
    测试：删除Milvus的实体和标量检索
"""

from pymilvus import MilvusClient


def get_milvus_client():
    """创建连接Milvus的客户端对象"""
    return MilvusClient(
        uri="http://127.0.0.1:19530",
    )

def delete_data(client : MilvusClient):
    result = client.delete(
        collection_name="demo_collection",
        filter="id in [466872317797488509, 466872317797488510]"
    )

    print(result)

def query_text(client : MilvusClient):
    result = client.query(
        collection_name="demo_collection",
        filter="text like '%监护人%'",
        output_fields=["id", "text", "metadata"],
    )

    print(result)


if __name__ == '__main__':
    client = get_milvus_client()
    # delete_data(client)
    query_text(client)