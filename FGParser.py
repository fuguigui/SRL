import utils.transferTool as Transfer
import os
import time
class FGParser(object):
    def __init__(self):
        self.ChunkSet=[]# the list save all chunks, extracted features
        self.chunker # the SVM judgement model to chunk a given sentence
        self.classer # the SVM multi-classification model on a chunk-level sentence.
        self.ClassSet=[] # saving different types and their features.
    def train(self, train_in_file, train_out):
        print('Reading the train data....')
        train_in, train_in_delabel  = Transfer.Read(train_in_file)
        print('Training the parser...')

        # First step: train the model to chunk the input.
        train_in_tree = Transfer.SentToTree(train_in_delabel) # the list of each sentence's tree
        train_chunk_out = Transfer.SRtoChunk(train_out)
        train_in_feature = Transfer.ChunkFeatures(train_in, train_in_tree, train_chunk_out, if_train=True)#if_train is used to define the label attribute in features
        self.ChunkSet.extend(train_in_feature) #TODO: maybe use set instead of list, do union operation for update.
        print('Training the chunker...')
        # TODO: train the 2-judgement SVM, problem: here, we only have postive examples. What should the input be?
        self.chunker.train(train_in_feature)

        # Second step: train the multi-classification SVM model
        train_out_features = Transfer.SRFeatures(train_in,train_chunk_out, train_out, if_train=True)
        print('Training the classer...')
        self.classer.train(train_out_features)

    def test(self, test_in_file):
        print('Reading the test data...')
        test_in, test_in_delabel  = Transfer.Read(test_in_file)
        test_in_tree = Transfer.SentToTree(test_in_delabel)
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

