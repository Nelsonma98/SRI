import math
import pickle
from os import listdir
from os.path import join, isfile
from typing import List

from nltk import *

import numpy as np

from constants import *
from text_processor import Cleaner


class Corpus:
    def __init__(self, corpus_name) -> None:
        if corpus_name == CRAN_CORPUS_NAME:
            self.corpus_path = CRAN_CORPUS_PATH
        elif corpus_name == MED_CORPUS_NAME:
            self.corpus_path = MED_CORPUS_PATH
        else:
            self.corpus_path = NEWS_GROUP_CORPUS_PATH
        self.corpus_name = corpus_name
        self.cl: Cleaner = None
        self.doc_tf = {}  # termino, id: tf
        self.idf = {}  # termino: idf
        self.index = {}  # termino: List(doc en los que aparece)
        self.doc_weights = {}  # termino: peso
        self.doc_norm = {}  # id: norma
        self.docs_id = {}  # id: direccion en memoria
        self.docs = {}  # id : List(term q aparecen)
        self.fuzzy = {}  # (term,doc): valor

        self.start()
        self.create_tables()

    def start(self):
        if self.cl is None:
            self.cl = Cleaner()

        try:
            self.docs_id = self.get_tables(DOC_ID_TABLE)
        except:
            files = self.__scan_corpus(self.corpus_path)
            self.docs_id = {i + 1: f for i, f in enumerate(files)}
            self.save_tables(DOC_ID_TABLE, self.docs_id)

    def create_tables(self):
        try:
            self.doc_tf = self.get_tables(DOC_TF_TABLE)
            self.idf = self.get_tables(IDF_TABLE)
            self.index = self.get_tables(INDEX_TABLE)
            self.doc_weights = self.get_tables(DOC_WEIGHTS_TABLE)
            self.doc_norm = self.get_tables(DOC_NORM_TABLE)
            self.fuzzy = self.get_tables(FUZZY_TABLE)
            self.docs = self.get_tables(DOCS_TABLE)
        except:
            for dj, file in self.docs_id.items():
                text = self.cl.get_text(file)
                tokens = self.cl.doc_to_tokens(text, use_lematizer=True)
                self.docs[dj] = tokens
                self.__calc_tf(tokens, dj)

            self.__calc_idf()
            self.__calc_weights()

            self.save_tables(DOC_TF_TABLE, self.doc_tf)
            self.save_tables(IDF_TABLE, self.idf)
            self.save_tables(DOCS_TABLE, self.docs)
            self.save_tables(INDEX_TABLE, self.index)
            self.save_tables(DOC_WEIGHTS_TABLE, self.doc_weights)
            self.save_tables(DOC_NORM_TABLE, self.doc_norm)
            self.save_tables(FUZZY_TABLE, self.fuzzy)

    def __calc_tf(self, tokens, dj):
        aux = {}
        for t in tokens:
            try:
                aux[t, dj] += 1
            except KeyError:
                aux[t, dj] = 1
                try:
                    self.index[t].add(dj)
                except KeyError:
                    self.index[t] = set([dj])

        max_freq_tok = max(aux.values())
        aux = {(key, dj): aux[key, dj] / max_freq_tok for key, _ in aux}
        self.doc_tf.update(aux)

    def __calc_idf(self):
        for t in self.index:
            self.idf[t] = math.log10(len(self.docs_id) / len(self.index[t]))

    def __calc_weights(self):
        for t in self.index:
            for d in self.docs_id:
                try:
                    u = 1
                    if self.docs[d].__contains__(t):
                        self.fuzzy[t, d] = 1
                    else:
                        for i in self.docs[d]:
                            c = len(self.index[t] & self.index[i])
                            u *= 1 - c/(len(self.index[t])+len(self.index[i])-c)
                        self.fuzzy[t, d] = 1-u
                    self.doc_weights[t, d] = self.doc_tf[t, d] * self.idf[t]
                except KeyError:
                    pass
        for dj in self.docs_id:
            self.doc_norm[dj] = np.linalg.norm(
                [self.doc_weights[k] for k in self.doc_weights if k[1] == dj])

    def __scan_corpus(self, path) -> List[str]:
        if self.corpus_name == '20newsgroup':
            directories = listdir(path)
        else:
            directories = sorted(listdir(path), key=lambda e: int(e))

        files_found = []
        for e in directories:
            file_path = join(path, e)
            if not isfile(file_path):
                files_found += self.__scan_corpus(file_path)
            else:
                files_found.append(file_path)
        return files_found

    def save_tables(self, file_name, struct):
        try:
            file_name = f'tables/{self.corpus_name}/' + file_name
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, 'wb') as f:
                pickle.dump(struct, f)
                f.close()
        except:
            print("ERROR!!")

    def get_tables(self, file_name):
        with open(os.path.join(os.getcwd(), f'tables/{self.corpus_name}/{file_name}'), 'rb') as table:
            return pickle.load(table)
