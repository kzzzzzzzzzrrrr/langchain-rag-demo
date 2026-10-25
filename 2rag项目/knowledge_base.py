# 处理数据库，主要是处理md5
import os
from datetime import datetime

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config_data as config
import hashlib
def check_md5(md5_str:str):
    """检查是否存在这个md5了，避免重复存储"""
    # 首先检查文件是否存在， 配置config_data.py文件保存文件的位置
    # 存在的话判断md5字符串是否存在，打开文件的内容，看是否右字符串和md5_str一致，不存在创建文件
    # 存在代表已经处理过
    if not os.path.exists(config.md5_path):
        open(config.md5_path,"w",encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path,"r",encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False


def save_md5(md5_str:str):
    """存储md5到文件中"""
    with open(config.md5_path,"a",encoding='utf-8') as f:
        f.write(md5_str + '\n')
def get_str_md5(input_str:str,encoding = 'utf-8'):
    """将传入的字符串转化为md5"""
    str_bytes = input_str.encode(encoding=encoding)  #将输入字符转换为字节数组
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()
    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model = "text-embedding-v4"),
            persist_directory=config.persist_directory
        )  #向量库对象
        self.split = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,
            chunk_overlap = config.chunk_overlap,
            separators=config.separators
        ) #文本分割器对象

    def upload_by_str(self,data,filename):
        """将传入的字符串进行向量化，存储到数据库中"""
#         首先判断这个字符串对应的md5是否存在，不存在的话下面操作
#         首先判断字符串的长度是否值得分割，阈值为 max_split_char_number
#         分割的话调用split进行处理，得到list[str],否则原始的字符串转化为list格式
#         将传入的字符串用唯一的md5表示，如果分割了，每一部分的md5应该是一样的  get_str_md5
#         判断md5是否存在  check,存在的话跳过，不存在的话，将字符存入向量数据库中，并保存md5
        md5_hex :str = get_str_md5(data)
        if check_md5(md5_hex):
            return '跳过，已经存在这个资料'
        # 下面是不存在的情况
        # 先判断值不值得分割，得到处理好的数据
        split_data = []
        if len(data) > config.max_split_char_number:
            split_data = self.split.split_text(data)
        else:
            split_data = [data]
#         存储到向量库中
        metadata = {
            "source":filename,
            "create_name":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"kzz"
        }
        self.chroma.add_texts(
            split_data,
            metadatas=[metadata for _ in split_data]
        )
#         保存当前字符的md5
        save_md5(md5_hex)
        return "用户已成功将数据载入向量库"

# if __name__ == '__main__':
#     service = KnowledgeBaseService()
#     r = service.upload_by_str("kzz",'./data.txt')
#     print(r)
