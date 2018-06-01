class ChunkFeature(object):
    def __init__(self):
        self.label='N'

    def setLabel(self,label):
        self.label = label

    def Extract(self, beg,end, verb_idx, label_sent):
        self.len = end-beg+1
        self.head_word=0 # TODO: Haven't done. refer 2004 Sun and Jurafsky to complete.
        self.head_POS = 0#TODO: like above.
        if(beg>0):
            self.before_context = label_sent[beg-1].split('\t')[-1]
        else:
            self.before_context = '*' # * means none.
        if(end + 1== len(label_sent)):
            self.after_context = '*'
        else:
            self.after_context = label_sent[end+1].split('\t')[-1]
        self.POSchain=""
        i = beg
        while(i< end+1):
            self.POSchain += label_sent[i].split('\t')[-1]+'-'
            i+=1
        # self.POSchain = encoder(self.POSchain)
        self.position = 2 * verb_idx - (beg + end)

class VerbFeature(object):
    def __init__(self, word):
        self.word = word