from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = UnstructuredMarkdownLoader(
    file_path="./assets/sample.md",
    mode="single"
)

doc = loader.load()

# 创建文本切分对象
chunks = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "，", ""], # 分割符列表
    chunk_size=200, # 数据片段的长度
    chunk_overlap=50, # 重叠长度
    length_function=len, # 指定计算数据片段长度的函数
    add_start_index=True # 每个数据片段的元数据中添加start_index（起始索引）
).split_documents(doc)

for i in chunks:
    print(i)
    print("="*100)