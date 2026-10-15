"""
    测试：使用嵌入模型将文本转换为向量
"""

from langchain_huggingface import HuggingFaceEmbeddings

embed_model = HuggingFaceEmbeddings(
    model_name="./assets/models/bge-base-zh-v1.5"
)

result1 = embed_model.embed_query("你好，世界")
print(len(result1))
print(result1[0:20])