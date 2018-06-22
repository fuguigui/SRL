import utils.transferTool as Transfer
import os
import time
from model import Chunker
from model import SRLabeler

class FGParser(object):
    def __init__(self):
        self.ChunkExp=[]# the list save all chunks, extracted features
        self.ChunkNegExp=[]
        self.chunker = Chunker.Chunker() # the SVM judgement model to chunk a given sentence
        self.SRLabler = SRLabeler.SRLabeler() # the NBclassification model on a chunk-level sentence.

    def train(self, train_in_file,train_out_file, tree_file=""):
        print('Reading the train data....')
        train_in, train_in_delabel  = Transfer.ReadIn(train_in_file)
        # f = open(tree_file,'r')
        # train_in_tree = f.readlines()
        # f.close()
        train_out = Transfer.ReadOut(train_out_file)
        train_chunk_out = Transfer.SRtoChunk(train_out)

        print('Preparing the data...')
        # First step: train the model to chunk the input.
        train_in = SelectVerb(train_in)
        train_in_feature = Transfer.ChunkFeatures(train_in, chunked=train_chunk_out)
        Transfer.CFeatureWriteInCSV('./data/trn/trn_chunk_features.csv',train_in_feature)

        print('Training the chunker...')
        # Enrich the training datasets.
        self.GreedyTrial(train_in, train_in_feature)

        # train the NB classifier
        X = self.ChunkExp + self.ChunkNegExp
        y = [1] * len(self.ChunkExp)
        y.extend([0] * len(self.ChunkNegExp))
        self.chunker.classifier.fit(X, y)

        # Second step: train the multi-classification SVM model
        print('Training the classer...')
        verb_feature = Transfer.VerbFeatures(train_in, chunked=train_chunk_out)
        self.SRLer.train(train_chunk_out, train_in_feature,verb_feature)

    def test(self, test_in_file,tree_file):
        print('Reading the test data...')
        test_in, test_in_delabel  = Transfer.ReadIn(test_in_file)

        test_out=[]

        for each_sent_grp in test_in:
            test_grp=[]
            for i in range(len(each_sent_grp)):
                verb_idx = each_sent_grp[i][0]
                whole_sent = each_sent_grp[i][1]
                best_chunk = self.GreedyEachSent(verb_idx,whole_sent)  # given s sentence: verb_idx and the list of all words, get its best chunk
                verb_features = Transfer.VerbFeature(each_sent_grp, best_chunk)
                chunk_features = Transfer.ChunkFeatures(each_sent_grp, chunked=best_chunk)
                each_test_out = self.SRLer.test(best_chunk, verb_features, chunk_features)
                beauty_out = Transfer.BeautifyOut(each_test_out)
                test_grp.append(beauty_out)
                # Transfer the output into appropriate format.
                # test: change the label attribute in the features and maintain an output list
            test_out.append(test_grp)

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

    def GreedyTrial(self, raw_in, chunk_out):
        for each_sent_grp in raw_in:
            for i in range(len(each_sent_grp)):
                verb_idx = each_sent_grp[i][0]
                whole_sent = each_sent_grp[i][1]
                best_chunk = self.GreedyEachSent(verb_idx, whole_sent) #given s sentence: verb_idx and the list of all words, get its best chunk
                self.CompareChunks(best_chunk, chunk_out) # if there are different chunks, add them into negative examples.

    def GreedyEachSent(self, verb_idx, all_words):
        split_strate = []
        topFiveScore=[0]
        splits=[]
        # construt the seed of strategies,
        for j in range(len(all_words)):
            if (j == verb_idx):
                continue
            splits.append([j, j])
        split_strate.append(splits)
        split_best, topScore= self.iterateBestSplit(verb_idx,all_words, split_strate, topFiveScore)
        return split_best[0]

    def CompareChunks(self, new_chunk, right_chunk):
        # Find the wrong chunks
        negchunk_features=[]
        # TODO: Add wrong chunks into negative sets.
        self.ChunkNegExp.extend(negchunk_features)

    def RateSplit(self, raw_sent,chunks):
        feature_list = Transfer.ChunkFeaturesEachSent(raw_sent, chunks)
        if(feature_list not in self.ChunkExp):
            self.ChunkNegExp.append(feature_list)

    def iterateBestSplit(self, v_idx, all_words, cur_strategies, topFiveScore):
        next_strategies = Transfer.generateNewStrateg(cur_strategies)
        if_changed = False
        for new_strategy in next_strategies:
            temp_chunk = Transfer.SplitToChunk(new_strategy)
            to_rate = [v_idx, all_words]
            score = self.RateSplit(to_rate, temp_chunk)
            score_len = len(topFiveScore)
            order = score_len
            for j in range(score_len):
                if (score < topFiveScore[score_len - j]):
                    order = score_len-j
                    if_changed = True
                    break
            topFiveScore.insert(order, score)
            cur_strategies.insert(order, new_strategy)
            if(score_len == 5):
                topFiveScore.pop(4)
                cur_strategies.pop(4)
            if(if_changed == False):
                return cur_strategies, topFiveScore
            else:
                return self.iterateBestSplit(all_words,cur_strategies, topFiveScore)



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




