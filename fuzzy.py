from typing import List, Dict
import numpy as np

from corpus import Corpus
from constants import *
from model import Model

class FuzzyModel(Model):
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
        q = self.corpus.cl.doc_to_tokens(query)
        q_t = self.query_tokens(q)
        return q_t

    def similarity(self, query, limit=15):
        q_t = self.process_query(query)
        sim = {}
        for d in self.corpus.docs_id:
            u = 1
            for t in q_t:
                try:
                    u *= self.corpus.fuzzy[t,d]
                except KeyError:
                    u = 0
                    break
            sim[d] = 1-(1-u)
            ranking = sorted(sim.items(), key=lambda kv: kv[1], reverse=True)[:limit]

        retrieved_id_documents = [(dj,self.corpus.docs_id[dj]) for dj,_ in ranking]
        return retrieved_id_documents