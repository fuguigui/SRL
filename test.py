import utils.transferTool as Transfer
import FGParser as Parser
# # Test: ReadOut and SRtoChunk
# train_out = Transfer.ReadOut('./data/trn/trn.props')
# train_chunk_out = Transfer.SRtoChunk(train_out)
# # print(train_chunk_out)
#
# # Test: FGParser.SelectVerb
# train_in, train_in_ulbl = Transfer.ReadIn('./data/trn/trn.text')
# train_in = FGParser.SelectVerb(train_in)
# feature_list = Transfer.ChunkFeatures(train_in,  chunked=train_chunk_out)
# Transfer.CFeatureWriteInCSV('./data/trn_feature.csv',feature_list)
# # print(feature_list)

# split=[[0,0],[1,1],[2,5],[6,7],[8,8],[9,11],[12,12],[13,13],[14,17],[18,19]]
# chunk = Transfer.SplitToChunk(split)
# print(chunk)

# # Test: Transfer.mergeList
# old_len = len(split)
# beg = 4
# seg_num = 2
# new_split = Transfer.mergeList(beg, seg_num, split)
# print("new_split: ",new_split)
# print("old_split: ",split)

# # Test: Transfer.generateNewStrateg
# split_list = [split]
# new_strategies = Transfer.generateNewStrateg(split_list)
# print("old_split: ",split)
# for new_s in new_strategies:
#     print(new_s)
#     print(Transfer.SplitToChunk(new_s))

# Test:FGParser.train
fgparser = Parser.FGParser()
fgparser.train("./data/trn/trn_expr.text","./data/trn/trn_expr.props")
fgparser.test("./data/dev/dev_expr.text")

