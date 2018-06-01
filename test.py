import utils.transferTool as Transfer
import FGParser
# Test: ReadOut and SRtoChunk
train_out = Transfer.ReadOut('./data/trn/trn_expr.props')
train_chunk_out = Transfer.SRtoChunk(train_out)
# print(train_chunk_out)

# Test: FGParser.SelectVerb
train_in, train_in_ulbl = Transfer.ReadIn('./data/trn_expr.text')
train_in = FGParser.SelectVerb(train_in)
feature_list = Transfer.ChunkFeatures(train_in,  chunked=train_chunk_out)
Transfer.CFeatureWriteInCSV('./data/feature.csv',feature_list)
print(feature_list)

