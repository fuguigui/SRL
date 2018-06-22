from sklearn.naive_bayes import MultinomialNB

class Chunker(object):
    def __init__(self):
        self.classifier = MultinomialNB()
    def predict(self, featureList):
        # if the output is the type 0,increase the score
        score = 0
        for feature in featureList:
            result = self.classifier.predict(feature)
            if(result == 0):
                score+=1
        return score

