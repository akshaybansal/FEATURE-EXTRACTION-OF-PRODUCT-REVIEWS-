from nltk import stem

class HelperFunctions:
	def __init__(self, feature_list):
		self.feature_list = feature_list
		self.snowball = stem.RegexpStemmer('ies$|s$')

	def strip_new_line(word):
		return word.strip('\n')

	def check_for_but(self, sentance):
		if sentance.find(" but ") != -1:
			return sentance.split(" but ")
		elif sentance.find(" but,") != -1:
			return sentance.split(" but,")
		else:
			return [sentance]

	def check_in_feature_list(self, word):
		if word in self.feature_list:
			return word
		for i in self.feature_list:
			if (len(word)*100)/len(i) > 75 and len(word) <= len(i):
				if i.find(word) != -1:
					return i
		return False

	def get_all_features(self, tokens):  
		""" a little editing required! """
		features, feature = [], None
		multiple, prev_token_feature = False, False
		for i in tokens:
			word = self.check_in_feature_list(self.get_root_word(i[0].lower()))
			if word:
				# print "'", i[0], "'", 
				if multiple:
					features.append(word)
				elif prev_token_feature or not feature:
					feature = word
				prev_token_feature = True
			elif i[0] == "and":
				prev_token_feature = False
				if feature:
					multiple = True
					features.append(feature)
			else:
				prev_token_feature = False
				# print i[0],
		# print ""
		if feature == None:
			return []
		elif not multiple or len(features) == 1:
			return [feature]
		else:
			return features

	def get_root_word(self, word):			# convert plural to singular!
		return self.snowball.stem(word)

	def get_product_names(self):
		product_file = open("product names.txt", "r")
		product = {}
		line = product_file.readline()
		while line:
			line = line.split(":")
			product[line[0]] = line[1].strip()
			line = product_file.readline()
		product_file.close()
		return product

	

if __name__ == "__main__":
	print "This script is not for execution. It only contains the helper functions used by other scripts."
	raw_input("Press any key to continue...")
	exit()