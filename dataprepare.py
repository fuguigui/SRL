import utils.transferTool as Transfer
# # Read in provided files and manually do parsing
raw_res, in_res = Transfer.ReadIn('./data/trn/trn.text')
Transfer.WriteUnlblSent(in_res, 'trn','to_parsed.txt')

raw_res, in_res = Transfer.ReadIn('./data/dev/dev.text')
Transfer.WriteUnlblSent(in_res, 'dev','to_parsed.txt')

raw_res, in_res = Transfer.ReadIn('./data/test/test.text')
Transfer.WriteUnlblSent(in_res, 'test','to_parsed.txt')

# Manually doing jar tool: BerkeleyParser
# jar command: java -jar BerkeleyParser-1.7.jar -gr bpmodel <.\data\trn\to_parsed.txt> .\data\trn\to_parsed.txt
# jar command: java -jar BerkeleyParser-1.7.jar -gr bpmodel <.\data\dev\to_parsed.txt> .\data\dev\to_parsed.txt
# jar command: java -jar BerkeleyParser-1.7.jar -gr bpmodel <.\data\test\to_parsed.txt> .\data\test\to_parsed.txt

# Parsed results are not satisfactory. Emmmmmm, I am worrying whether to use them.