import os

BASE_PATH = os.path.join(os.getcwd(), 'corpus')

DOC_TF_TABLE = "doc_tf"
IDF_TABLE = "idf"
INDEX_TABLE = "index"
DOC_WEIGHTS_TABLE = "doc_weights"
DOC_NORM_TABLE = "doc_norm"
DOC_ID_TABLE = "doc_id"
FUZZY_TABLE = "fuzzy"
DOCS_TABLE = "docs"

MED_CORPUS_PATH = f'{BASE_PATH}/corpus_med'
CRAN_CORPUS_PATH = f'{BASE_PATH}/corpus_cran'
NEWS_GROUP_CORPUS_PATH = f'{BASE_PATH}/corpus_20newsgroup'

MED_CORPUS_NAME = 'med'
CRAN_CORPUS_NAME = 'cran'
NEWS_GROUPS_CORPUS_NAME = '20newsgroup'

CRAN_QUERY_RESULT = f'{os.getcwd()}/queries_rel/cranqrel'
MED_QUERY_RESULT = f'{os.getcwd()}/queries_rel/MED.REL'
CRAN_QUERIES = f'{os.getcwd()}/queries_rel/cran.qry'
MED_QUERIES = f'{os.getcwd()}/queries_rel/MED.QRY'

VEC_MODEL_NAME = "vectorial"
BOOL_MODEL_NAME = "boolean"
FUZZY_MODEL_NAME = "fuzzy"