import utils.transferTool as Transfer
import os
import time
import re
from model import Chunker
from model import SRLabeler
import utils.Encoder as En

class FGParser(object):
    def __init__(self):
        self.ChunkExp=[]# the list save all chunks, extracted features
        self.ChunkNegExp=[]
        self.chunker = Chunker.Chunker() # the SVM judgement model to chunk a given sentence
        self.SRLabler = SRLabeler.SRLabeler() # the NBclassification model on a chunk-level sentence.
        self.encoder = En.Encoder()

    def train(self, train_in_file,train_out_file):
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
        train_in_feature = Transfer.ChunkFeatures(train_in, train_chunk_out, encoder= self.encoder)
        Transfer.CFeatureWriteInCSV('./data/trn/features.csv', train_in_feature)

        #
        # # train the NB classifier
        # X = self.ChunkExp + self.ChunkNegExp
        # y = [1] * len(self.ChunkExp)
        # y.extend([0] * len(self.ChunkNegExp))
        # self.chunker.classifier.fit(X, y)

        # Second step: train the multi-classification SVM model
        print('Training the classer...')
        self.SRLabler.train(train_in_feature)

    def test(self, test_in_file):
        print('Reading the test data...')
        test_in, test_in_delabel  = Transfer.ReadIn(test_in_file)
        test_in = SelectVerb(test_in)

        test_out=[]
        test_id = 0

        for each_sent_grp in test_in:
            print("the test id is :", test_id)
            test_id +=1
            test_grp=[]
            for i in range(len(each_sent_grp)):
                verb_idx = each_sent_grp[i][0]
                whole_sent = each_sent_grp[i][1]
                if(verb_idx == -1):
                    test_grp.append([])
                    continue
                best_chunk = self.GreedyEachSent(verb_idx,whole_sent, if_test=True)  # given s sentence: verb_idx and the list of all words, get its best chunk
                test_grp.append(best_chunk)

            test_out.append(test_grp)
        # Beautify the output
        test_out = Transfer.BeautifyOut(test_out)
        time_str = time.strftime("%m-%d-%H-%M", time.localtime())
        filename = time_str+'.props'
        Transfer.WriteOut(filename, test_out, test_in)



    def GreedyEachSent(self, verb_idx, all_words ,if_test=False):
        split_strate = []
        labels = []
        topFiveScore=[0]
        splits=[]
        label = []
        # construt the seed of strategies,
        for j in range(len(all_words)):
            if (j == verb_idx):
                label.append('V')
            else:
                label.append('N')
            splits.append([j, j])
        split_strate.append(splits)
        labels.append(label)
        split_best, topScore= self.iterateBestSplit(verb_idx,all_words, split_strate, labels, topFiveScore ,if_test=if_test)
        return split_best[0]


    def RateSplit(self, raw_sent,chunks, if_test=False):
        feature_list = Transfer.ChunkFeaturesEachSent(raw_sent, chunks ,self.encoder, if_test=if_test)
        coded_features = []
        for feature in feature_list:
            coded_features.append(feature.encoding())
        y = self.SRLabler.classifier.predict(coded_features)
        y =  list(y)
        y_prob = self.SRLabler.classifier.predict_proba(coded_features)
        score = 0
        for each_prob in y_prob:
            best_prob = max(each_prob)
            score += best_prob

        return score,y

    def iterateBestSplit(self, v_idx, all_words, cur_strategies,labels, topFiveScore ,if_test=False):
        next_strategies = Transfer.generateNewStrateg(v_idx, cur_strategies)
        if_changed = False
        if(len(next_strategies) ==0):
            return labels, topFiveScore
        for new_strategy in next_strategies:
            temp_chunk = Transfer.SplitToChunk(new_strategy)
            to_rate = [v_idx, all_words]
            score ,generate_labels = self.RateSplit(to_rate, temp_chunk, if_test=if_test)
            score_len = len(topFiveScore)
            order = score_len
            for j in range(score_len):
                if(score > topFiveScore[score_len - j-1]):
                    if(score_len-j-2>=0):
                        if(score<topFiveScore[score_len-j-2]):
                            order = score_len-j-1
                            if_changed = True
                            break
                        break
                    else:
                        order = score_len-j-1
                        if_changed = True
                        break
            if(if_changed):
                topFiveScore.insert(order, score)
                cur_strategies.insert(order, new_strategy)
                labels.insert(order,generate_labels)
                if(score_len == 5):
                    topFiveScore.pop(4)
                    cur_strategies.pop(4)
                    labels.pop(4)
                return self.iterateBestSplit(v_idx, all_words, cur_strategies, labels, topFiveScore, if_test=if_test)
            else:
                return labels, topFiveScore


def SelectVerb(train_in):
    sent_list = []
    for sent in train_in:
        reform_sent = []
        for i in range(len(sent)):
            splits = sent[i].split('\t')
            if(len(splits) == 3):
                sent_item = splits[1]
            else:
                sent_item=splits[-1]
            if(re.search(r'(^V)',sent_item)):
                reform_sent.append([i, sent])

        if(len(reform_sent)==0):
            reform_sent.append([-1,[]])
        sent_list.append(reform_sent)
    return sent_list
