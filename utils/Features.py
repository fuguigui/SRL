class ChunkFeature(object):
    def __init__(self, encoder):
        self.label='N'
        self.encoder = encoder

    def setLabel(self,label):
        self.label = label

    def getLabel(self):
        return self.label
    def encoding(self):
        dict = self.encoder.getDict()
        dict_len = len(dict)
        self.vec = [0]*(dict_len*3+3)
        splited_pos = self.POSchain.split('-')
        for pos in splited_pos:
            if(pos in dict):
                idx = dict.index(pos)
                self.vec[idx] = self.vec[idx]+1
        if(self.after_context in dict):
            after_idx = dict.index(self.after_context)
            self.vec[dict_len+after_idx] = self.vec[dict_len+after_idx] +1
        if(self.before_context in dict):
            before_idx = dict.index(self.before_context)
            self.vec[dict_len*2+before_idx] = self.vec[dict_len*2+before_idx]+1
        self.vec[dict_len*3] = self.len
        if(self.position<0):
            self.position = 0-self.position
            self.vec[dict_len*3+2] = 1
        self.vec[dict_len*3+1]=self.position
        return self.vec

    def Extract(self, beg,end, verb_idx, label_sent, if_test = False):
        self.len = end-beg+1
        if(beg>0):
            self.before_context = label_sent[beg-1].split('\t')[1]
        else:
            self.before_context = '*' # * means none.
        if(end + 1== len(label_sent)):
            self.after_context = '*'
        else:
            self.after_context = label_sent[end+1].split('\t')[1]
        self.POSchain=""
        i = beg
        while(i< end+1):
            label = label_sent[i].split('\t')[1]
            self.POSchain += label+'-'
            if(not if_test):
                self.encoder.addToDict(label)
            i+=1
        # self.POSchain = encoder(self.POSchain)
        self.position = 2 * verb_idx - (beg + end)
