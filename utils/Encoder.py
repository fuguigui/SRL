class Encoder(object):
    def __init__(self):
        self.POSDict = ['*']
    def getDict(self):
        return self.POSDict
    def addToDict(self, voc):
        if voc not in self.POSDict:
            self.POSDict.append(voc)
