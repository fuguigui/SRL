import os
from utils.Features import *


def ReadIn(filename):
    in_list = []
    raw_list = []
    f = open(filename,'r',encoding='UTF-8')
    sent = []
    raw_sent = []
    lines = f.readlines()
    for line in lines:
        if(line == '\n'):
            in_list.append(sent)
            raw_list.append(raw_sent)
            sent = []
            raw_sent = []
        else:
            sent.append(line.split('\t')[0])
            raw_sent.append(line.rstrip('\n'))
    f.close()
    return raw_list, in_list

def ReadOut(filename):
    f = open(filename,'r',encoding='UTF-8')
    outlist=[]
    lines = f.readlines()
    unit_list = []
    for line in lines:
        if(line =='\n'):
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
            changed_unit.pop(0)
            outlist.append(changed_unit)
            changed_unit=[]
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


def SentToTree(sents):
    #TODO: transter a labeled sentence to a tree.
    return 0
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
    #TODO: given the final labeled result, transfer it into chunk representation.
    chunk = ['*']*len(out)
    lnext='B'
    for idx in range(len(out)):
        chunk[idx],lnext = judgeSR(out[idx],lnext)
    return chunk
def judgeSR(label, lnext):
    cur = 0
    e_next = 0
    if('(' in label):
        cur = 'B-'
        if(')' in label):
            e_next = 'B-'
        else:
            e_next = 'I'
    elif(')' in label):
        cur = 'O-'
        e_next = 'B'
    else:
        if(lnext =='I'):
            cur='I-'
            e_next='I'
        else:
            cur = 'B-'
            e_next = 'B'
    if('V' in label):
        cur = cur+'V'
    else:
        cur = cur+'A'
    return cur,e_next

def TreetoHeight():
    #TODO: given a tree, get its each node's height.
    return 0
def ChunkFeatures(label_sents, tree_sents):
    featurelist = []
    # the format of elements in featurelist: a list[idx of the verb chunk,all the chunks]
    for idx in range(len(label_sents)):
        # Deal with each sentence.
        label_sent = label_sents[idx]
        tree_sent = tree_sents[idx]
        v_num, v_list = MoreInOne(label_sent)
        if(v_num >1):
            # Copy One sentence to v_num copies.
            for v_idx in v_list:
                chunkf_list = []
                for word_idx in range(len(label_sent)):
                    chunk = ChunkFeature()
                    chunk.Extract(word_idx, label_sent, tree_sent)
                    if(word_idx == v_idx):
                        chunk.setLabel('B-V')
                    chunkf_list.append(chunk)

                featurelist.append([v_idx, chunkf_list])

        else:
            chunkf_list=[]
            for word_idx in range(len(label_sent)):
                chunk = ChunkFeature()
                chunk.Extract(word_idx,label_sent, tree_sent)
                if(word_idx == v_list[0]):
                    chunk.setLabel('B-V')
                chunkf_list.append(chunk)

            featurelist.append([v_list[0],chunkf_list ])
    return featurelist

def MoreInOne(sent):
    idx_list=[]
    for idx in range(len(sent)):
        label = sent[idx].split('\t')[1]
        if('V' in label):
            idx_list.append(idx)
    return len(idx_list),idx_list


def SRFeatures(inlist, chunklist):
    # TODO: given the SRL output, extract features for each label.
    out_features=[]
    return out_features