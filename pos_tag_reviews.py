import glob
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag

tokenizer = RegexpTokenizer(r'[\w\']+')
get_token = tokenizer.tokenize
pos_tags_file = open("pos_tags_file.txt", "w")

total_files = len(glob.glob("list of products/*.txt"))
file_count = 0

for f in glob.glob("list of products/*.txt"):
    file_count += 1
    progress = open("Progress Report.txt", "w")
    progress.write("Processing file "+str(file_count)+"/" + str(total_files))
    progress.write("Percentage Done: " + str(file_count*100/total_files))
    progress.close()
    review_file_pointer = open(f, "r")
    postags = []
    line = review_file_pointer.readline()
    while line:
        token_list = get_token(line)
        postags = pos_tag(token_list)
        for i in postags:
        	pos_tags_file.write(repr(i) + "\n")
        line = review_file_pointer.readline()
    review_file_pointer.close()

pos_tags_file.close()
