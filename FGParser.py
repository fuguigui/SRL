import utils.transferTool as Transfer
import os
import time

class FGParser(object):
    def __init__(self):
        self.ChunkExp=[]# the list save all chunks, extracted features
        self.ChunkNegExp=[]
        self.chunker # the SVM judgement model to chunk a given sentence
        self.classer # the SVM multi-classification model on a chunk-level sentence.

    def train(self, train_in_file,tree_file, train_out_file):
        print('Reading the train data....')
        train_in, train_in_delabel  = Transfer.ReadIn(train_in_file)
        # f = open(tree_file,'r')
        # train_in_tree = f.readlines()
        # f.close()
        train_out = Transfer.ReadOut(train_out_file)
        train_chunk_out = Transfer.SRtoChunk(train_out)

        print('Training the parser...')
        # First step: train the model to chunk the input.
        train_in = SelectVerb(train_in)
        train_in_feature = Transfer.ChunkFeatures(train_in, chunked=train_chunk_out)
        self.ChunkExp.extend(train_in_feature) #TODO: maybe use set instead of list, do union operation for update.
        print('Training the chunker...')
        # TODO: train the 2-judgement SVM, problem: here, we only have postive examples. What should the input be?
        self.chunker.train(train_in, train_in_feature)

        # Second step: train the multi-classification SVM model
        print('Training the classer...')
        self.classer.train(train_in_feature)

    def test(self, test_in_file,tree_file):
        print('Reading the test data...')
        test_in, test_in_delabel  = Transfer.ReadIn(test_in_file)
        f = open(tree_file, 'r')
        test_in_tree = f.readlines()
        f.close()

        test_in_feature = Transfer.ChunkFeatures(test_in, test_in_tree,[])
        print('Testing the chunk results...')
        test_chunk_out = self.chunker.test(test_in_feature)

        test_out_feature = Transfer.SRFeatures(test_in, test_chunk_out,[])
        test_out = self. classer.test(test_out_feature)# test: change the label attribute in the features and maintain an output list

        time_str = time.strftime("%m-%d-%H-%M", time.localtime())
        filename = time_str+'.props'
        print('Saving outputs in ', filename)
        fpath = os.path.join('.','FGParser_results')
        if (not os.path.exists(fpath)):
            os.mkdir(fpath)
        f = open(os.path.join(fpath,filename),'w')
        for each_out in test_out:
            f.write(each_out)
    def valid(self, valid_in):
        # TODO ; how to use validation?
        return 0



def SelectVerb(train_in):
    sent_list = []
    for sent in train_in:
        reform_sent = []
        for i in range(len(sent)):
            if ('V' in sent[i]):
                reform_sent.append([i, sent])

        if(len(reform_sent)==0):
            reform_sent.append([-1,[]])
        sent_list.append(reform_sent)
    return sent_list




