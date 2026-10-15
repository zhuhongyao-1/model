"""
    测试：向量检索
    1、通过稠密向量进行检索
    2、通过稀疏向量进行检索
    3、通过稠密向量和稀疏向量进行混合检索
"""
from langchain_openai import ChatOpenAI
from pymilvus import MilvusClient, AnnSearchRequest, RRFRanker
from FlagEmbedding import BGEM3FlagModel

def get_milvus_client():
    """创建连接Milvus的客户端对象"""
    return MilvusClient(
        uri="http://127.0.0.1:19530",
    )

def query_to_vector(query):
    """将用户的问题转换为向量"""
    embed_model = BGEM3FlagModel(
        model_name_or_path=r"D:\workspace\BJ260318\langchain\rag\assets\models\bge-m3"
    )
    all_vector = embed_model.encode([query], return_dense=True, return_sparse=True)
    return all_vector["dense_vecs"], all_vector["lexical_weights"]

def search_dense_vector(client : MilvusClient, query):
    """通过稠密向量进行检索"""
    dense_vector,_ = query_to_vector(query)
    results = client.search(
        collection_name="demo_collection", # collection名字
        data=dense_vector, # 要检索的数据
        anns_field="vector", # 要检索的字段
        limit=3, # TopK
        search_params={"metric_type": "L2"}, # 设置检索方式
        output_fields=["id", "text", "metadata"] # 设置查询的结果中需要输出的字典
    )
    print(results)

def search_sparse_vector(client : MilvusClient, query):
    """通过稠密向量进行检索"""
    _,sparse_vector = query_to_vector(query)
    results = client.search(
        collection_name="demo_collection", # collection名字
        data=sparse_vector, # 要检索的数据
        anns_field="sparse_vector", # 要检索的字段
        limit=3, # TopK
        search_params={"metric_type": "IP"}, # 设置检索方式
        output_fields=["id", "text", "metadata"] # 设置查询的结果中需要输出的字典
    )
    print(results)

def hybrid_search_vector(client : MilvusClient, query):
    """通过稠密向量和稀疏向量进行混合检索"""
    dense_vector,sparse_vector = query_to_vector(query)
    dense_vector_req = AnnSearchRequest(
        data=dense_vector,
        anns_field="vector",
        param={"metric_type": "L2"},
        limit=3
    )
    sparse_vector_req = AnnSearchRequest(
        data=sparse_vector,
        anns_field="sparse_vector",
        param={"metric_type": "IP"},
        limit=3
    )
    results = client.hybrid_search(
        collection_name="demo_collection",
        reqs=[dense_vector_req, sparse_vector_req], # 设置检索条件
        ranker=RRFRanker(), # 设置重排规则
        limit=3,
        output_fields=["id","text","metadata"]
    )
    return results

def final_generate(client, query):
    llm = ChatOpenAI(
        model="gpt-4o-mini"
    )

    # 获取混合检索的结果
    results = hybrid_search_vector(client, query)

    # 整理上下文
    context = "\n".join([result["entity"]["text"] for result in results[0]])

    response = llm.invoke(
        [
            ("user", f"请结合上下文进行总结，上下文：{context}，问题：{query}"),
        ]
    )

    print(response)

if __name__ == "__main__":
    client = get_milvus_client()
    # search_dense_vector(client, "监护人要履行什么职责")
    # search_sparse_vector(client, "监护人要履行什么职责")
    # hybrid_search_vector(client, "监护人要履行什么职责")
    final_generate(client, "监护人要履行什么职责")