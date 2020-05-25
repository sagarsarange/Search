'''
This class is used to extract data from corpus file.
This class make use of DocumentParser to parse HTML content.
'''

from DocumentParser import DocumentParser
import json


class DataExtractor:
    def __init__(self):
        self.document_list = []
        self.parser = DocumentParser()

    def extract_data(self, file_name='./document/wiki_10'):
        file = open(file_name, "r", encoding='utf-8')
        self.parser.feed(file.read())
        self.document_list = self.parser.get_document_list()
        print("Total number of Documents: ", str(len(self.document_list)))
        file.close()
        return self.store_document(file_name)

    def store_document(self, file_name):
        output_file_name = file_name + "-structured-documents.json"
        f = open(output_file_name, "w", encoding='utf-8')
        json.dump(self.document_list, f)
        f.close()
        return output_file_name
