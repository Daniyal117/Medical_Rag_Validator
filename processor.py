from docling.document_converter import DocumentConverter
from langchain_core.documents import Document
from text_cleaner import normalize_text


def load_document(file_path: str) -> Document:
    converter = DocumentConverter()
    result = converter.convert(file_path)

    raw_text = result.document.export_to_markdown()
    clean_text = normalize_text(raw_text)

    return Document(
        page_content=clean_text,
        metadata={"source": file_path}
    )