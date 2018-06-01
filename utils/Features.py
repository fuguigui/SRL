class Feature(object):
    def __init__(self):
        self.label = 0
        self.fList=[]
    def setLabel(self,label):
        self.label = label
        # ChunkFeature: has five labels: B-A,I-A,O-A,B-V, N. N: means that don't know what it will be. B-V only appears in manual setting.

class ChunkFeature(Feature):
    def __init__(self):
        super.__init__()
        self.fColum=[]
    def Extract(self, word_idx, raw_in, tree_in):
        return 0


class SRFeature(object):
    def __init__(self):
        self.num = 0