import os
md5_path = './data/md5.txt'

#chroma
collection_name = 'rag'
persist_directory = './chroma_db'

# spliter
separators = ['\n\n','\n','.',',','?','!','。','，','？','！',' ','']
chunk_size = 1000
chunk_overlap = 100
max_split_char_number = 1000

# 向量检索的阈值，vector_store
retrive_thresold = 2

# rag文件中的聊天模型
chat_model = "qwen-plus"

session_config = {
    "configurable":{
        "session_id":"user_001"
    }
}