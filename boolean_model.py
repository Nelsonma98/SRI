from typing import List, Dict
import numpy as np

from corpus import Corpus
from constants import *
from model import Model


class BooleanModel(Model):
    def __init__(self, corpus: Corpus) -> None:
        self.corpus = corpus

    @staticmethod
    def query_tokens(query):
        query_token = []
        for t in query:
            if not query_token.__contains__(t):
                query_token.append(t)
        return query_token

    def process_query(self, query):
        q = self.corpus.cl.doc_to_tokens(query, use_lematizer=True)
        q_t = self.query_tokens(q)
        return q_t

    def similarity(self, query, limit=15):
        query_token = self.process_query(query)
        retrieved_id_documents = []
        # for dj in self.corpus.docs_id:
        #     var_boolean = True
        #     for t in query_token:
        #         if not self.corpus.doc_tf.__contains__((t,dj)):
        #             var_boolean = False
        #             break
        #     if var_boolean:
        #         retrieved_id_documents.append(self.corpus.docs_id[dj])#dj
        #         # if len(retrieved_id_documents) == limit: break
        var_bool = True
        temp = set([])
        for t in query_token:
            if var_bool:
                temp = self.corpus.index[t]
                var_bool = False
            else:
                temp = set(temp) & set(self.corpus.index[t])
        retrieved_id_documents = [(d,self.corpus.docs_id[d]) for d in temp]
            

        return retrieved_id_documents