class Posting:
    # doc_id: the document id
    # tfidf: the score of each document, for now its the occurence of the word
    # fields: the types of token (is it a title, content, date, etc.)
    # position: the exact position of the token inside the document

    def __init__(self, doc_id, tfidf=-1):
        self.doc_id = doc_id
        self.tfidf = tfidf

    def get_id(self):   # accessor
        return self.doc_id

    def get_tfidf(self):
        return self.tfidf

    def set_tfidf(self, score):
        self.tfidf = score

    def result_posting(self):
        output = ""
        output += str(self.doc_id) + ": " + str(self.tfidf)
        return output

