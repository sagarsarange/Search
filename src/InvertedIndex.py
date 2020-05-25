'''
The build_term_index method of this class build inverted index and vector square sum file for the given file name
Generate two files
1. Index file name : <Given file name> + '-term-inverted-index.json'
2. Vector Square sum file: <Given file name> + '-vector-squared-sum.json'
'''

import getopt
import json
import sys
import nltk
from collections import defaultdict
from nltk.probability import FreqDist
import numpy as np
from DataExtractor import DataExtractor


class InvertedIndex:

    def __init__(self):
        self.term_index = defaultdict(dict)
        self.vector_squared_sum = defaultdict(lambda: 0)

    @staticmethod
    def get_tokens_text(text):
        tokens = [x.lower() for x in nltk.word_tokenize(text)]
        return tokens

    def build_term_index(self, structure_filename, file_name):
        doc_list_file = open(structure_filename, 'r')
        doc_list = json.load(doc_list_file)
        for d in doc_list:
            print("Building term index for doc id: ", d['id'])
            tokens = self.get_tokens_text(d['data'])
            fd = FreqDist(tokens)
            for key, value in fd.items():
                self.term_index[key].update({d['id']: value})
                self.vector_squared_sum[d['id']] += (1 + np.log(value)) ** 2
        doc_list_file.close()
        return self.store_index_and_vector(file_name)

    def store_index_and_vector(self, file_name):
        index_json = file_name + '-term-inverted-index.json'
        vector_squared_sum_json = file_name + '-vector-squared-sum.json'
        with open(index_json, 'w') as json_file:
            json.dump(self.term_index, json_file)
        with open(vector_squared_sum_json, 'w') as v_file:
            json.dump(self.vector_squared_sum, v_file)
        return index_json, vector_squared_sum_json


def get_arguments(argument_list):
    short_options = "d:"
    long_options = ["document="]
    try:
        document_file = ''
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
        print(arguments)
        if len(arguments) < 1:
            print("Invalid arguments")
            sys.exit(2)
        for t in arguments:
            if t[0] in ("-d", "--document"):
                document_file = t[1]
                print(document_file)
        return document_file
    except getopt.error as err:
        print(str(err))
        sys.exit(2)


if __name__ == '__main__':
    wiki_10_file = get_arguments(sys.argv[1:])
    inverted_index = InvertedIndex()
    data_extractor = DataExtractor()
    structure_file_name = data_extractor.extract_data(wiki_10_file)
    index_file, vector_file = inverted_index.build_term_index(structure_file_name, wiki_10_file)
    print("Index file name: ", index_file)
    print("Vector file name: ", vector_file)
