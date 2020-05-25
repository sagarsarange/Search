'''
Search class is used to perform search on given inverted index and vector sqaure sum file name.
'''
import nltk
import json
import numpy as np
from collections import defaultdict
from nltk.probability import FreqDist
import getopt
import sys


class Search:

    def __init__(self):
        self.vector_sqr_sum = None
        self.inverted_index = None
        pass

    def get_idf(self, total_documents, doc_freq):
        if doc_freq != 0:
            return np.log(total_documents / float(doc_freq))
        return 0

    def get_query_term(self, query_terms):
        query_tokens = [x.lower() for x in nltk.word_tokenize(query_terms)]
        return FreqDist(query_tokens)

    def search_query(self, query_terms, vector_file_name='vector-squared-sum.json',
                     inverted_index_file_name='term-inverted-index.json'):
        query_term_freq = self.get_query_term(query_terms)
        v_file = open(vector_file_name, 'r')
        self.vector_sqr_sum = json.load(v_file)
        total_documents = len(self.vector_sqr_sum)
        index_file = open(inverted_index_file_name, 'r')
        self.inverted_index = json.load(index_file)
        docs_scores = defaultdict(lambda: 0)
        for query, query_term_frequency in query_term_freq.items():
            try:
                if query in self.inverted_index:
                    doc_list = self.inverted_index[query]
                    tf_wt_query = 1 + np.log(query_term_frequency)
                    w_tq = tf_wt_query * self.get_idf(total_documents, len(doc_list))
                    for doc_id, tf in doc_list.items():
                        tf_wt_doc = 1 + np.log(tf)
                        docs_scores[doc_id] += (w_tq * tf_wt_doc)
            except KeyError as e:
                print("Key not found: ", query, " Error message: ", e)
        for doc_id, score in docs_scores.items():
            length = np.sqrt(self.vector_sqr_sum[doc_id])
            docs_scores[doc_id] /= length
        docs_scores = {k: v for k, v in sorted(docs_scores.items(), key=lambda item: item[1], reverse=True)}
        return docs_scores


def get_arguments(argument_list):
    global search_query, index_file_name, vector_file_name
    short_options = "s:i:v:"
    long_options = ["search=", "index_file=", "vector_file="]
    try:
        search_query = ''
        index_file_name = None
        vector_file_name = None
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
        print(arguments)
        if len(arguments) < 3:
            print("Invalid arguments")
            sys.exit(2)
        for t in arguments:
            if t[0] in ("-s", "--search"):
                search_query = t[1]
                print(search_query)
            elif t[0] in ("-i", "--index_file"):
                index_file_name = t[1]
            elif t[0] in ("-v", "--vector_file"):
                vector_file_name = t[1]
        return search_query, vector_file_name, index_file_name
    except getopt.error as err:
        print(str(err))
        sys.exit(2)


if __name__ == '__main__':
    search_query, vector_file_name, index_file_name = get_arguments(sys.argv[1:])
    search = Search()
    print(search.search_query(search_query, vector_file_name, index_file_name))
