from sklearn.naive_bayes import MultinomialNB
import utils.Features as feature
import utils.transferTool as Transfer

class SRLabeler(object):
    def __init__(self):
        self.classifier = MultinomialNB()
    def train(self, train_in_feature):
        features=expandFeatures(train_in_feature)
        # encoding and training the classifier
        train_x,train_y = extractClass(features)

        self.classifier.fit(train_x,train_y)


def expandFeatures(features):
    sub_features=[]
    for each_sent_features in features:
        for each_feature in each_sent_features:
            sub_features.extend(each_feature[1])
    return sub_features

def extractClass(features):
    train_x = []
    train_y = []
    for each_feature in features:
        train_y.append(each_feature.getLabel())
        train_x.append(each_feature.encoding())
    return train_x, train_y