"""
    测试：解析sample.docx文件，并切分，将切分后的文本片段通过bge-m3转换为向量，存储到向量数据库中
"""
import logging

from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import MilvusClient
from FlagEmbedding import BGEM3FlagModel

logging.basicConfig(level=logging.DEBUG)
def get_milvus_client():
    """创建连接Milvus的客户端对象"""
    return MilvusClient(
        uri="http://127.0.0.1:19530",
    )



def insert_data(client : MilvusClient, collection_name):

    # 加载sample.docx文件
    documents = UnstructuredWordDocumentLoader(
        file_path="./assets/sample.docx",
        mode="single"
    ).load()

    # 对documents中的文本内容进行切分
    chunks = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。"], # 分隔符列表
        chunk_size=500, # 切分的每个数据片段的最大长度
        chunk_overlap=50, # 每个数据片段的重叠大小
    ).split_documents(documents)

    chunks = chunks[0:50]

    # 创建嵌入模型实例
    embed_model = BGEM3FlagModel(
        model_name_or_path=r"D:\workspace\BJ260318\langchain\rag\assets\models\bge-m3"
    )

    # 使用bge-m3将数据片段转换为稠密向量和稀疏向量
    # all_vectors:{"dense_vecs":[[指定维数的浮点],...], "lexical_weights":[[数据片段所对应的稀疏向量],...]}
    all_vectors = embed_model.encode(
        sentences=[chunk.page_content for chunk in chunks],
        return_dense=True,
        return_sparse=True
    )

    # 分别获取数据片段所对应的所有稠密向量和稀疏向量
    dense_vectors = all_vectors["dense_vecs"]
    sparse_vectors = all_vectors["lexical_weights"]

    # 构建添加到milvus中的数据列表
    data_list = []
    for chunk,dense_vector,sparse_vector in zip(chunks, dense_vectors, sparse_vectors):
        data_list.append(
            {
                "vector": dense_vector,
                "sparse_vector": sparse_vector,
                "text": chunk.page_content,
                "metadata": chunk.metadata,
            }
        )

    client.insert(
        collection_name=collection_name,
        data=data_list
    )

if __name__ == '__main__':
    client = get_milvus_client()
    insert_data(client, "demo_collection")