from langchain_community.document_loaders import UnstructuredWordDocumentLoader

"""
loader = UnstructuredWordDocumentLoader(
    file_path="./assets/sample.docx",
    mode="single",
)

document = loader.load()

print(document)
"""

loader = UnstructuredWordDocumentLoader(
    file_path="./assets/sample.docx",
    mode="elements",
)

documents = loader.load()

for document in documents:
    print(document)
    print("="*100)