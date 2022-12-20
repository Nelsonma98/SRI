from typing import List, Dict
import numpy as np

from corpus import Corpus
from constants import *
from model import Model


class VectorialModel(Model):
    def __init__(self, corpus: Corpus) -> None:
        self.corpus = corpus

    @staticmethod
    def calc_query_tf(query):
        query_tf = {}
        for t in query:
            try:
                query_tf[t] += 1
            except KeyError:
                query_tf[t] = 1

        max_freq_tok = max(query_tf.values())
        query_tf = {key: query_tf[key] / max_freq_tok for key in query_tf}
        return query_tf

    def calc_query_weights(self, alpha, query_tf):
        query_weights = {}
        for t in query_tf:
            try:
                idf = self.corpus.idf[t]
            except KeyError:
                continue

            query_weights[t] = (alpha + (1 - alpha) * query_tf[t]) * idf

        return query_weights

    def process_query(self, query, alpha=0.5):
        q = self.corpus.cl.doc_to_tokens(query)
        q_tf = self.calc_query_tf(q)
        ans = self.calc_query_weights(alpha, q_tf)

        return ans

    def similarity(self, query, limit=15):
        query_weights = self.process_query(query)
        norm_q = np.linalg.norm(list(query_weights.values()))
        sim = {}
        for dj in self.corpus.docs_id:
            vect_prod = 0
            for t in query_weights:
                try:
                    vect_prod += self.corpus.doc_weights[t, dj] * query_weights[t]
                except KeyError:
                    pass
            sim[dj] = vect_prod / self.corpus.doc_norm[dj] * norm_q
            ranking = sorted(sim.items(), key=lambda kv: kv[1], reverse=True)[:limit]

        retrieved_id_documents = [(d,self.corpus.docs_id[d]) for d,_ in ranking]
        return retrieved_id_documents