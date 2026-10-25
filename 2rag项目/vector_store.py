# 进行向量数据库中的向量检索，返回检索器，最后测试
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

import config_data as config

class VectorStoreService(object):
    # 需要初始化chroma
    def __init__(self):
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory
        )

    def RetriveVector(self):
        Retriver = self.chroma.as_retriever(search_kwargs = {"k":config.retrive_thresold})
        return Retriver
if __name__ == '__main__':
    service = VectorStoreService()
    retrive = service.RetriveVector()
    res = retrive.invoke("我的体重为50kg")
    print(res)
