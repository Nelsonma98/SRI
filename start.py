from cProfile import run
from typing import List, Dict, Any

from constants import *
from vectorial_model import VectorialModel
from boolean_model import BooleanModel
from fuzzy import FuzzyModel
from corpus import Corpus

def run(q,model):
    file_id = model.similarity(q)
    print('Id of the retrieved documents: ')
    for _,i in file_id:
        print(i)

def main():
    while True:
        corpus = input('Corpus: 1-Med 2-Cran ')
        if corpus == '1':
            corpus_name = Corpus(MED_CORPUS_NAME)
        else:
            corpus_name = Corpus(CRAN_CORPUS_NAME)
        type_model = input('Type Model(V : Vectorial, B : Boolean, F : Fuzzy): ')
        if type_model == 'V' or type_model == 'v':
            model = VectorialModel(corpus_name)
            break
        elif type_model == 'B' or type_model == 'b':
            model = BooleanModel(corpus_name)
            break
        elif type_model == 'F' or type_model == 'f':
            model = FuzzyModel(corpus_name)
            break
        else:
            print('Invalid command!!!')
    while True:
        queries = input('Insert a query or press Enter to exit: ')
        if queries == '':
            break
        run(queries,model)

if __name__=='__main__':
    main()