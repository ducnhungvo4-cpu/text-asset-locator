import pandas as pd
from docx import Document
import os


def read_text_file(file_path):
    """读取文本文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def read_docx_file(file_path):
    """读取Word文档"""
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def read_spreadsheet_file(file_path):
    """读取Excel或CSV文件"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.xlsx':
        return pd.read_excel(file_path)
    elif ext == '.csv':
        return pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported spreadsheet format")


def read_file(file_path):
    """根据文件扩展名调用相应的读取函数"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return read_text_file(file_path)
    elif ext == '.docx':
        return read_docx_file(file_path)
    elif ext in ['.xlsx', '.csv']:
        return read_spreadsheet_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")