import utils.transferTool as Transfer
# Test: ReadOut and SRtoChunk
train_out = Transfer.ReadOut('./data/trn/trn_expr.props')
train_chunk_out = Transfer.SRtoChunk(train_out)
print(train_chunk_out)