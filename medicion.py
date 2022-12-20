from cProfile import run
from typing import List, Dict, Any

from constants import *
from corpus import Corpus
from vectorial_model import VectorialModel
from boolean_model import BooleanModel
from fuzzy import FuzzyModel


def parse_query_rel(dir):
    with open(dir) as f:
        docs_for_query = {}
        queries_result = f.read().split('\n')

        for result in queries_result:
            elements = result.split(' ')
            try:
                docs_for_query[int(elements[0])].append(int(elements[1]))
            except KeyError:
                docs_for_query[int(elements[0])] = [int(elements[1])]
        f.close()
        return docs_for_query


def parse_query_request(dir):
    with open(dir) as f:
        queries = {}
        queries_splited = f.read().split('\n.I')

        for i, splited_text in enumerate(queries_splited):
            q = splited_text.split('\n.W\n')[1]
            try:
                queries[i + 1].append(q)
            except KeyError:
                queries[i + 1] = q
        f.close()
        return queries


def recoverd_docs(retrived_docs, relevant_docs):
        rr = 0
        nr = 0
        for dicc in retrived_docs:
            if dicc in relevant_docs:
                rr += 1
            else:
                nr += 1
        return rr, nr


def precision(retrived_docs, relevant_docs):
    rr, nr = recoverd_docs(retrived_docs, relevant_docs)
    if rr and nr:
        return (rr / (rr + nr)) * 100
    else:
        return 0

def recall(retrived_docs, relevant_docs):
    rr, _ = recoverd_docs(retrived_docs, relevant_docs)
    rn = abs(len(relevant_docs) - rr)
    if rr and rn:
        return (rr / (rr + rn)) * 100
    else:
        return 0

def f1(retrived_docs, relevant_docs):
        p = precision(retrived_docs, relevant_docs)
        r = recall(retrived_docs, relevant_docs)
        if p != 0 or r != 0:
            return (2 * p * r / (p + r))
        else:
            return 0

def run_tests(dir_results, dir_q, model):
    best = parse_query_rel(dir_results)
    queries = parse_query_request(dir_q)

    p = 0
    r = 0
    f = 0

    total_q = len(queries)

    for i,q in enumerate(queries.values()):
        respon = model.similarity(q)
        response = [(d) for d,_ in respon]
        p += precision(response,best[i+1])
        r += recall(response,best[i+1])
        x = f1(response,best[i+1])
        f += x

    print('mean precision: ', p / total_q, '%')
    print('mean recall: ', r / total_q, '%')
    print('mean f1: ', f / total_q, '%')
    print(" ")

def main():
    # corpus_name = Corpus(CRAN_CORPUS_NAME)
    # dir_results = CRAN_QUERY_RESULT
    # dir_q = CRAN_QUERIES

    corpus_name = Corpus(MED_CORPUS_NAME)
    dir_results = MED_QUERY_RESULT
    dir_q = MED_QUERIES

    # print("Vectorial")
    # modelv = VectorialModel(corpus_name)
    # run_tests(dir_results,dir_q,modelv)
    # print("Boolean")
    # modelb = BooleanModel(corpus_name)
    # run_tests(dir_results,dir_q,modelb)
    print("Fuzzy")
    modelf = FuzzyModel(corpus_name)
    run_tests(dir_results,dir_q,modelf)
    
if __name__ == '__main__':
    main()