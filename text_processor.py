import string

from nltk import *
from nltk.corpus import stopwords


class Cleaner:
    def __init__(self) -> None:
        pass

    def get_text(self, path_file):
        with open(path_file, encoding='utf8', errors='ignore') as file:
            text = file.read()
            file.close()
            return text

    def __remove_no_words(self, tokens):
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        stripped = [re_punc.sub('', w) for w in tokens]
        return stripped
    
    def __remove_especial_exp(self,text):
        easy_text = re.sub('from:(.*\n)', '', text)
        easy_text = re.sub('[\w]+[\._]?[\w]+[@]+[\w.]+', '', easy_text)
        easy_text = re.sub('Subject:|subject:', '', easy_text)
        return easy_text

    def doc_to_tokens(self, easy_text, use_stemmer=False, use_lematizer=True):
        easy_text = self.__remove_especial_exp(easy_text)
        tokens = word_tokenize(easy_text)
        tokens = [t.lower() for t in tokens]
        tokens = self.__remove_no_words(tokens)
        tokens = [word for word in tokens if word.isalpha()]
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if not t in stop_words] # word root
        if use_stemmer:
            stemmer = SnowballStemmer(language="english")
            tokens = [stemmer.stem(word) for word in tokens]

        if use_lematizer:
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(word) for word in tokens]
        return tokens