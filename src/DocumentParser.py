'''
This class is used to parse HTML document
Returns a list containing all document entries in the corpus file.
Each document entry is a dictionary containing document data along with Document metadata like
document title, document id.
This class inherits HTMLParser to parse HTML content.
'''
from html.parser import HTMLParser


class DocumentParser(HTMLParser):
    document_list = []

    def error(self, message):
        print("Error occurred: ", message)

    def handle_starttag(self, tag, attrs):
        if tag == "doc":
            self.document = {'data': '', 'id': attrs[0][1], 'title': attrs[2][1]}

    def handle_endtag(self, tag):
        if tag == "doc":
            self.document_list.append(self.document)

    def handle_data(self, data):
        self.document['data'] = self.document['data'] + data

    def get_document_list(self):
        return self.document_list
