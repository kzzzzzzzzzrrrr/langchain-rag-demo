# 这个是长期存储的代码，主要就是将用户会话存储到json文件中
import json
import os
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,store_path):
        self.session_id = session_id
        self.store_path = store_path
        self.file_path = os.path.join(self.store_path,self.session_id)
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)
    def add_messages(self,messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        # messages转换为字典格式，然后转化为json格式
        new_messages = []
        for message in all_messages:
            m = message_to_dict(message)
            new_messages.append(m)
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f)
    # 获取文件中的message,文件中都是json格式存存放的，先整成字典列表，然后 用官方进行转成message
    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                list_messages = json.load(f)
            return messages_from_dict(list_messages)
        except FileNotFoundError:
            return []
    # 清空文件
    def clear(self) -> None:
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f)
