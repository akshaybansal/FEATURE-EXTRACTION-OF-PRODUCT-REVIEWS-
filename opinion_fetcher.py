from __future__ import division
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag, stem
from nltk.corpus import stopwords
import sentiword_net_implementation as sni
from glob import glob
from re import compile, sub
from helper_functions import *

def strip_new_line(word):
	return word.strip('\n')

def check_for_but(sentance):
	if sentance.find(" but ") != -1:
		return sentance.split(" but ")
	elif sentance.find(" but,") != -1:
		return sentance.split(" but,")
	else:
		return [sentance]

def check_for_and(sentance):
	if sentance.find(" and ") != -1:
		return sentance.split(" and ")
	elif sentance.find(" and,") != -1:
		return sentance.split(" and,")
	else:
		return [sentance] 

def check_in_feature_list(word):
	global feature_list
	if word in feature_list:
		return word
	for i in feature_list:
		if (len(word)*100)/len(i) > 75 and len(word) <= len(i):
			if i.find(word) != -1:
				return i
	return False

def get_all_features(tokens):
	global feature_list
	features, feature = [], None
	multiple, prev_token_feature = False, False
	for i in tokens:
		word = check_in_feature_list(get_root_word(i[0].lower()))
		if word: 
			if multiple:
				features.append(word)
			elif prev_token_feature or not feature:
				feature = word
			prev_token_feature = True
		elif i[0] == "and":
			prev_token_feature = False
			if feature:
				features.append(feature)
		else:
			prev_token_feature = False

	if feature == None:
		return []
	elif not multiple or len(features) == 1:
		return [feature]
	else:
		return features

def get_product_names():
	product_file = open("product names.txt", "r")
	product = {}
	line = product_file.readline()
	while line:
		line = line.split(":")
		product[line[0]] = line[1].strip()
		line = product_file.readline()
	product_file.close()
	return product

def get_root_word(word):			# convert singular to plural!
	return snowball.stem(word)

# values to be initialised in constructor
SWN_FILENAME = "SentiWordNet_3.0.0_20130122.txt"
cv = sni.SentiWordNetCorpusReader(SWN_FILENAME)
snowball = stem.RegexpStemmer('ies$|s$|er$')
tokenizer = RegexpTokenizer(r"[\w\']+")
get_tokens = tokenizer.tokenize
stopwords_list = stopwords.words('english')
f = open("tokenized_noun_file.txt", "r")
# final_file = open("output_test.txt", "w")
feature_list, feature_name = [], []
err_file = open("error_file_copy.txt", "w")
opinion_file = open('opinion file.csv', 'w')
opinion_file.write('product id,review no,sentance no,feature,opinion,senti score +ve,senti score -ve\n')
negation_list = ['don\'t', 'not', 'never']
# tasks to be done in the constructor itself!
subs_list = [compile("\'ve"), compile("\'d"), compile("\'s")]
replace_list = ["have", "would", "is"]


for i in f.readlines():
	feature = i.split(":")[0]
	feature_list.append(feature)
f.close()
# Start processing !!!
# filename = raw_input("Enter filename containing review(also mention the extension): ")
tot_files = len(glob("list of products/B00004W6*.txt"))
product = get_product_names()
file_count = 0
percent = 0
print "processing.. Go to Progress Report.txt for further details"
for filename in glob("list of products/B00004W6*.txt"):
	progress_file = open("Progress Report.txt", "w")
	review_category = {}
	file_count += 1
	# if (file_count*50)//tot_files > percent:
	# 	print ":",
	percent =  (file_count*100)//tot_files
	progress_file.write("Files Scanned: "+str(file_count)+"/"+str(tot_files) + "\n")
	progress_file.write("Progress: "+str(percent)+"%\n")
	progress_file.close()
	f = open(filename, "r")
	line = f.readline()
	reviews = []
	while line:
		reviews.append(line)
		line = f.readline()
	f.close()
	number_of_reviews = len(reviews)
	review_count = 0
	while len(reviews) > 0:
		review = reviews.pop(0)
		for i in range(3):
			review = subs_list[1].sub(replace_list[i], review)
		sentances = review.split(".")  #splitting the review on the basis of fullstop. 
		feature_score = {}								#processing each sentance for it's feature
		feature_adverb_score = {}
		review_count += 1
		final_sentances = []
		for i in sentances:
			if not i:
				continue
			sentance = check_for_but(i)
			for j in sentance:
				final_sentances.extend(check_for_and(j))   # split the sentances having but in them to 2 diff sentances
		for sentance_no in xrange(len(final_sentances)):				# scan the final set of sentances to check for features
			opinion_list = []
			t = final_sentances[sentance_no]
			reverse_polarity = False
			counter = False
			tokens = get_tokens(t)
			pos_tagged_tokens = pos_tag(tokens)
			tokens_without_stop_words = []
			prev_feature = feature_name
			feature_name = get_all_features(pos_tagged_tokens)  #extract features from review

			for i in feature_name:
				# opinion_list[i.strip('.,?/-').lower()] = []
				if not review_category.has_key(i.strip(".,?/-").lower()):
					review_category[i.strip(".,?/-").lower()] = {'pos_review':0, 'neg_review': 0, 'neutral_review': 0}

			if (t.find("it") != -1 or t.find("It") != -1) and not feature_name:
				feature_name = prev_feature 
			for i in pos_tagged_tokens:    #Remove the stop words!
				if (i[0].strip(".,?/-").lower() not in stopwords_list) or (i[0].strip(".,?/-").lower() == 'not'):
					tokens_without_stop_words.append(i)

			# print tokens_without_stop_words

			overall_pos_score, overall_neg_score = [], []
			# overall_pos_score_adverb, overall_neg_score_adverb = [], []
			for i in tokens_without_stop_words:
				if i[1].find("JJ") != -1:
					# print i[0], 
					pos_score, neg_score = 0, 0
					synsets_of_adjective = cv.senti_synsets(i[0], 'a')
					if synsets_of_adjective:
						synsets_of_adjective = cv.senti_synsets(i[0])
					for synset in synsets_of_adjective:
						pos_score = pos_score + synset.pos_score/len(synsets_of_adjective)
						neg_score = neg_score + synset.neg_score/len(synsets_of_adjective)
					if pos_score > 0 or neg_score > 0:
						if reverse_polarity:
							overall_pos_score.append(neg_score)
							overall_neg_score.append(pos_score)
							reverse_polarity= False
						else:
							overall_pos_score.append(pos_score)
							overall_neg_score.append(neg_score)
						opinion_list.append(i[0])
				elif i[0] in negation_list:
					reverse_polarity = True 
					


			if len(overall_neg_score) == 0:
				overall_neg_score.append(0)
			if len(overall_pos_score) == 0:
				overall_pos_score.append(0)
			
			for name in feature_name:
				for i in xrange(len(opinion_list)):
					opinion_file.write(filename.split('\\')[1].split('.')[0]+","+str(review_count)+","+str(sentance_no)+","+name+","+opinion_list[i]+","+str(overall_pos_score[i])+","+str(overall_neg_score[i]))
					opinion_file.write("\n")

				if feature_score.has_key(name):
					posi_score, negi_score = feature_score[name][0], feature_score[name][1]
					feature_score[name] = (posi_score + sum(overall_pos_score)/len(overall_pos_score), 
						negi_score + sum(overall_neg_score)/len(overall_neg_score))
				else:
					feature_score[name] = (sum(overall_pos_score)/len(overall_pos_score), 
										sum(overall_neg_score)/len(overall_neg_score))

print ""
raw_input("Review Processing Complete. An output file with the name 'output.txt' has been created in the current directory. Press any key to continue...")
opinion_file.close()
err_file.close()
# final_file.close()
