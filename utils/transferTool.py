import os
import re
from utils.Features import *
import pandas as pd


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

def TreetoHeight():
    #TODO: given a tree, get its each node's height.
    return 0
def ChunkFeatures(label_sents, chunked=[]):
    featurelist = []
    # the format of elements in featurelist: a list[idx of the verb chunk,all the chunks]
    for idx in range(len(label_sents)):
        # Deal with each sentence.
        sub_sent=label_sents[idx]
        sub_chunk = chunked[idx]
        each_sent_feature=[]
        for i in range(len(sub_sent)):
            sent_a_verb = sub_sent[i] # sent_a_verb: e.g.:[10,[.. , ... , ...]]
            chunkf_list=[]
            chunk_a_verb = sub_chunk[i]
            # Get the number of chunks in a sentence
            if(sent_a_verb[0] == -1):
                each_sent_feature.append([-1,[]])
                continue
            for word_idx in range(len(chunk_a_verb)):
                if('B' in chunk_a_verb[word_idx]):
                    chunkf_list.append(word_idx)
            # Construct chunks
            chunks=[]
            for j in range(len(chunkf_list)-1):
                begin = chunkf_list[j]
                end = chunkf_list[j+1]-1
                chunk = ChunkFeature()
                chunk.Extract(begin,end,sent_a_verb[0],sent_a_verb[1])
                label = chunked[idx][i][begin].split('-')[-1]
                chunk.setLabel(label)
                chunks.append(chunk)
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