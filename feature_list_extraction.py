#RUN THE GET ALL PRODUCTS FILE BEFORE THIS FILE

"""
GET ALL THE FEATURES IN THE PRODUCT RELATED FEATURES PRESENT IN THE REVIEWS. THE SELECTION PROCESS IS BASED ON TWO MAJOR FACTORS
    -> THE WORD BEING A NOUN, AND
    -> THE WORD HAVING A HIGH FREQUENCY

FOR GETTING THE TOKENS ANOTHER FILE IS USED THAT IS STORING AROUND 50 LAKH TOKENS WITH THEIR TAGS CORRESPONDING TO THE TEXT OF THE REVIEWS.

"""

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import glob
from nltk import pos_tag, stem
from math import log10

threshold = 5000

tokenizer = RegexpTokenizer(r'[\w\']+')
get_token = tokenizer.tokenize
snowball = stem.RegexpStemmer('ies$|s$')
swlist = stopwords.words('english')
noun_file_pointer = open("tokenized_noun_file.txt", "w");

noun_postags, tf = [], {}
curr_line = 0
tot = 5000000
percent = 0
print "Reading lines"
pos_tags_file = open("pos_tags_file.txt", "r")
line = pos_tags_file.readline()
while line:
    i = eval(line)
    if i[1].find("NN") != -1:
        noun_postags.append(i[0].strip(".,-?").lower())
    line = pos_tags_file.readline()
    curr_line += 1
    prev_percent = percent
    percent = (curr_line*100)//tot
    if percent != prev_percent:
    	print ":",
pos_tags_file.close()
print ""
print "Counting nouns..."

for i in noun_postags:
    if tf.has_key(snowball.stem(i)):
        tf[snowball.stem(i)] += 1
    else:
        tf[snowball.stem(i)] = 1

noun_postags = []
print "Sorting nouns"

for token, count in tf.iteritems():
    if count < threshold or (token in swlist) or len(token) < 4:
        continue
    noun_postags.append((count, token))
noun_postags.sort()
noun_postags.reverse()
print "Writing Features"

for count, token in noun_postags:
    noun_file_pointer.write(token+ ":  "+ repr(count) + "\n")

noun_file_pointer.close()
print "Process over"

raw_input("continue...")