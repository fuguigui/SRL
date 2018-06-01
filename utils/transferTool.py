import os
def Read(filename):
    in_list = []
    raw_list = []
    f = open(filename,'r',encoding='UTF-8')
    sent = []
    raw_sent = []
    lines = f.readlines()
    for line in lines:
        print(line)
        if(line == '\n'):
            in_list.append(sent)
            raw_list.append(raw_sent)
            sent = []
            raw_sent = []
        else:
            sent.append(line.split('\t')[0])
            raw_sent.append(line.rstrip('\n'))
    return raw_list, in_list

def WriteUnlblSent(in_list, filename):
    folder = os.path.join('.','expr')
    if(not os.path.exists(folder)):
        os.mkdir(folder)
    f = open(os.path.join(folder, filename),'w')
    for item in in_list:
        f.write(" ".join(str(i) for i in item))
        f.write('\n')

def SentToTree(sents):
    #TODO: transter a labeled sentence to a tree.
    return 0

def SRtoChunk(out):
    #TODO: given the final labeled result, transfer it into chunk representation.
    return 0

def TreetoHeight():
    #TODO: given a tree, get its each node's height.
    return 0
def ChunkFeatures(label_sents, tree_sents, chunklist, if_train=False):
    # TODO: extract features from a list of chunks.
    featurelist = []
    return featurelist
def SRFeatures(inlist, chunklist, outlist, if_train=False):
    # TODO: given the SRL output, extract features for each label.
    out_features=[]
    return out_features