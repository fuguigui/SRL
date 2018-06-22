from sklearn.naive_bayes import MultinomialNB

class SRLabeler(object):
    def __init__(self):
        self.classifier = MultinomialNB()
