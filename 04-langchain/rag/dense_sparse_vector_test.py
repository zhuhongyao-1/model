"""
    测试：生成稠密向量和稀疏向量
"""
from FlagEmbedding import BGEM3FlagModel

# 创建模型对象
model = BGEM3FlagModel(
    model_name_or_path=r"D:\workspace\BJ260318\langchain\rag\assets\models\bge-m3"
)

# 通过模型对象生成稠密向量和稀疏向量
result = model.encode(
    ["标量字段通常用来存储一些元数据，并可以在搜索时通过元数据进行过滤"],
    return_dense=True,
    return_sparse=True
)

print("通过BGEM3转换向量之后的结果：")
print(result)
# print("="*100)
# print("稠密向量的长度：", len(result["dense_vecs"]))
# print("="*100)
# print("稠密向量：")
# print(result["dense_vecs"])
# print("="*100)
# print("稀疏向量：")
# print(result["lexical_weights"])
# print("="*100)
# print("将稀疏向量转换为是对应的token：")
# print(model.convert_id_to_token(result["lexical_weights"]))