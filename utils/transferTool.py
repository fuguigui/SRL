import os
import re
from utils.Features import *
import pandas as pd
import copy

def ReadIn(filename):
    in_list = []
    raw_list = []
    f = open(filename,'r',encoding='UTF-8')
    sent = []
    raw_sent = []
    lines = f.readlines()
    f.close()
    for line in lines:
        if(line == '\n'):
            in_list.append(sent)
            raw_list.append(raw_sent)
            sent = []
            raw_sent = []
        else:
            sent.append(line.split('\t')[0])
            raw_sent.append(line.rstrip('\n'))
    in_list.append(sent)
    raw_list.append(raw_sent)

    return raw_list, in_list

def ReadOut(filename):
    f = open(filename,'r',encoding='UTF-8')
    outlist=[]
    lines = f.readlines()
    unit_list = []
    for line_idx in range(len(lines)):
        line = lines[line_idx]
        if(line =='\n' or line_idx == len(lines)-1):
            unit_len = len(unit_list)
            cols = unit_list[0].rstrip('\t').split('\t')
            col_num = len(cols)
            # change a len*1 string to col_num * len table
            everyl=['-']*unit_len
            changed_unit = [everyl.copy() for i in range(col_num)]
            for idx in range(unit_len):
                each_line = unit_list[idx].rstrip('\t').split('\t')
                for col_idx in range(col_num):
                    changed_unit[col_idx][idx] = each_line[col_idx]
            # merge the first column with each of the other column and change
            if(col_num>1):
                changed_unit.pop(0)
            else:
                changed_unit[0]=[]
            outlist.append(changed_unit)
            unit_list=[]
        else:
            unit_list.append(line.rstrip('\n'))
    return outlist

def WriteUnlblSent(in_list,subpath, filename):
    folder = os.path.join('.','data',subpath)
    if(not os.path.exists(folder)):
        os.mkdir(folder)
    f = open(os.path.join(folder, filename),'w',encoding='UTF-8')
    for item in in_list:
        f.write(" ".join(str(i) for i in item))
        f.write('\n')
    f.close()

def WriteOut(outname, test_out, raw_sentences):
    filepath = './data/test/'
    if(not os.path.exists(filepath)):
        os.makedirs(filepath)
    out_file = os.path.join(filepath, outname)
    f = open(out_file, 'w', encoding='utf-8')
    for i in range(len(test_out)):
        each_sent = test_out[i]
        sent = raw_sentences[i]
        groups = len(each_sent)
        first_col = ['-']*len(sent[0][1])
        if(len(each_sent[0]) == 0):
            for j in range(len(first_col)):
                f.write(first_col[j])
                f.write('\n')
            f.write('\n')
            continue

        fchars = [0]*groups
        for j in range(groups):
            v_id = sent[j][0]
            verb = sent[j][1][v_id]
            verb = verb.split('\t')[0]
            first_col[v_id] = verb
        for line in range(len(first_col)):
            f.write(first_col[line])
            f.write('\t')
            for j in range(groups):
                if(each_sent[j][line] == fchars[j]):
                    f.write('*')
                    if(line<len(first_col)-1):
                        if(each_sent[j][line+1]!=fchars[j]):
                            f.write(fchars[j]+')')
                elif(each_sent[j][line] == 'N'):
                    f.write('*')
                else:
                    fchars[j] = each_sent[j][line]
                    f.write('('+fchars[j]+'*')
                    if (line < len(each_sent[j]) - 1):
                        if (each_sent[j][line + 1] != fchars[j]):
                            f.write(fchars[j] + ')')
                    else:
                        f.write(fchars[j] + ')')
                if (j == groups - 1):
                    f.write('\n')
                else:
                    f.write('\t')
        f.write('\n')
    f.close()


def SRtoChunk(all_out):
    chunk_list=[]
    for item_idx in range(len(all_out)):
        item_len = len(all_out[item_idx])
        sent_chunk=[]
        if(item_len!= 0):
            for sub_sent in all_out[item_idx]:
                sent_chunk.append(SRtoChunk_each(sub_sent))
        chunk_list.append(sent_chunk)
    return chunk_list

def SRtoChunk_each(out):
    chunk = ['*']*len(out)
    lnext='B'
    elabel='N'
    for idx in range(len(out)):
        chunk[idx],lnext,elabel = judgeSR(out[idx],lnext,elabel)
    return chunk

def judgeSR(label, lnext, elabel):
    cur = 0
    e_next = 0
    e_label = elabel
    if('(' in label):
        e_label = re.findall(r'([a-zA-Z0-9]+)',label)[0]
        cur = 'B-'+e_label
        if(')' in label):
            e_next = 'B-'
            e_label='N'
        else:
            e_next = 'I'
    elif(')' in label):
        cur = 'O-'+e_label
        e_next = 'B'
        e_label='N'
    else:
        if(lnext =='I'):
            cur='I-'+e_label
            e_next='I'
        else:
            cur = 'B-'+e_label
            e_next = 'B'
    return cur,e_next,e_label


def ChunkFeaturesEachSent(sent_a_verb, chunk_a_verb, encoder, if_test = False):
    chunkf_list=[]
    for word_idx in range(len(chunk_a_verb)):
        if ('B' in chunk_a_verb[word_idx]):
            chunkf_list.append(word_idx)
    # Construct chunks
    chunks = []
    begin = 0
    for j in range(len(chunk_a_verb)):
        chunk = ChunkFeature(encoder)
        if(j in chunkf_list):
            begin = j
            label = chunk_a_verb[j].split('-')[-1]
        else:
            label = chunk_a_verb[j].split('-')[-1]

        chunk.Extract(begin, j, sent_a_verb[0], sent_a_verb[1],if_test=if_test)
        if(not if_test):
            chunk.setLabel(label)
        chunks.append(chunk)
    return chunks

def ChunkFeatures(label_sents, chunked, encoder):
    featurelist = []
    # the format of elements in featurelist: a list[idx of the verb chunk,all the chunks]
    for idx in range(len(label_sents)):
        # Deal with each sentence.
        sub_sent = label_sents[idx]
        sub_chunk = chunked[idx]
        each_sent_feature=[]
        print("the idx is: ",idx,"\n")
        for i in range(len(sub_chunk)):
            sent_a_verb = sub_sent[i] # sent_a_verb: e.g.:[10,[.. , ... , ...]]
            chunk_a_verb = sub_chunk[i]
            # Get the number of chunks in a sentence
            if(sent_a_verb[0] == -1):
                each_sent_feature.append([-1,[]])
                continue
            chunks = ChunkFeaturesEachSent(sent_a_verb, chunk_a_verb, encoder)
            each_sent_feature.append([sent_a_verb[0], chunks])
        featurelist.append(each_sent_feature)
    return featurelist

def CFeatureWriteInCSV(filename, featurelist):
    list=[]
    for i in range(len(featurelist)):
        for j in range(len(featurelist[i])):
            sub_sent_feature = featurelist[i][j]
            if(sub_sent_feature[0]==-1):
                continue
            for k in range(len(sub_sent_feature)-1):
                features = sub_sent_feature[1+k]
                for l in range(len(features)):
                    list_item = []
                    feature = features[l]
                    list_item.append(feature.label)
                    list_item.extend([feature.len, feature.position, feature.POSchain,
                                      feature.after_context, feature.before_context])
                    list.append(list_item)

    name = ['label','len','position','POSchain','after_contect','before_context']
    test = pd.DataFrame(columns=name,data=list)
    test.to_csv(filename)

def SplitToChunk(split_strate):
    chunk = ['B']*(split_strate[-1][1]+1)
    for item in split_strate:
        beg = item[0]
        end = item[1]
        for i_beg in range(beg+1, end):
            chunk[i_beg]='I'
        if(beg<end):
            chunk[end]='O'
    return chunk

def generateNewStrateg(v_idx,cur_strategies):
    #  checked
    new_strateg=[]
    for strateg in cur_strategies:
        s_len = len(strateg)
        if(s_len == 1):
            continue
        for i in range(s_len-1):
            if(strateg[i][0] == v_idx):
                continue
            new_s = mergeList(i,1,strateg)
            new_strateg.append(new_s)
    return new_strateg

def mergeList(begin, seg_num, old_list):# the format of old_list:[[0,1],[1,2],...,[10,12]]
    # checked
    new_list = copy.deepcopy(old_list)
    beg_item = old_list[begin]
    end_item = old_list[begin+seg_num]
    new_list[begin] = [beg_item[0],end_item[1]]
    for i in range(seg_num):
        new_list.pop(begin+1)
    return new_list

def BeautifyOut(test_out):
    for each_sent in test_out:
        for i in range(len(each_sent)):
            begin = 'N'
            for j in range(len(each_sent[i])):
                each_item = each_sent[i][j]
                if(each_item!= 'N'):
                    if(each_item!= begin):
                        begin = each_item
                else:
                    if(begin!='V'):
                        each_sent[i][j] = begin
                    else:
                        begin='N'
    return test_out