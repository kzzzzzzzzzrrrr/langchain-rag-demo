# 利用前面已经构建好的数据库，得到的检索器，构建chain链条，进行模型的回复
# 提示词模板，检索器，模型，构建成链条
from langchain_core.documents import Document

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from file_history_store import FileChatMessageHistory
import config_data as config
from vector_store import VectorStoreService
class RagService(object):
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system","根据资料{context}回答下面的问题"),
                ("system","下面是历史会话记录"),
                MessagesPlaceholder("history"),
                ("human","解释并回答{input}")
            ]
        ) # 提示词
        self.model = ChatTongyi(model = config.chat_model,streaming = True) #模型
        self.retriver = VectorStoreService().RetriveVector()
        self.chain = self.__get_chain()
    def __get_chain(self):
        def format_doc(docs:list[Document]):
            res_str = ""
            for doc in docs:
                res_str += f"文本片段：{doc.page_content}\n 文档元数据：{doc.metadata}\n\n"
            return res_str
        def print_prompt(prompt):
            print("="*20)
            print(prompt.to_string())
            return prompt

        def get_history(session_id):
            return FileChatMessageHistory(session_id, "./chat_history")
        def format_for_retriver(value:dict) -> str:
            return value["input"]
        def format_for_prompt(value:str) -> dict:
            new_value = {
                "input":value["input"]["input"],
                "context":value["context"],
                "history":value["input"]["history"]
            }
            return new_value
        chain = ({
            "input":RunnablePassthrough(),
            "context": RunnableLambda(format_for_retriver) | self.retriver | format_doc
        } | RunnableLambda(format_for_prompt) | self.prompt | print_prompt |self.model | StrOutputParser())

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        return conversation_chain

# if __name__ == '__main__':
#     config_chain = {
#         "configurable":{
#             "session_id":"user_001"
#         }
#     }
#     service = RagService()
#     res = service.chain.invoke({"input":"我体重100斤，请推荐合适的尺码"},config_chain)
#     print(res)