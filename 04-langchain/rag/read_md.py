"""
    测试：解析markdown文件
    mode = "single | elements"
    single:将加载的文档中所有的内容加载为一个Document对象
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader


# 创建文档加载器
loader = UnstructuredMarkdownLoader(
    # file_path=r"D:\workspace\BJ260318\langchain\rag\assets\sample.md",
    file_path="./assets/sample.md",
    mode="single"
)

# 加载文档
document = loader.load()

print(document)


# # 创建文档加载器
# loader = UnstructuredMarkdownLoader(
#     # file_path=r"D:\workspace\BJ260318\langchain\rag\assets\sample.md",
#     file_path="./assets/sample.md",
#     mode="elements"
# )
#
# # 加载文档
# documents = loader.load()
#
# for document in documents:
#     print(document)
#     print("="*100)