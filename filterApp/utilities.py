"""
	this file include build dictionary, initial datbase,
	text2vector, 

"""
import random
import pickle

def build_dictionary(wordlist,lang = 'en'):
	stopwords = load_stop_word(lang)
	
	#remove stopword, change to set
	dictionary = [x for x in wordlist if x not in stopwords]

	#tf-idf or most freq item
	#limit to 3000
	if len(dictionary)> 3000:
		dictionary = random.sample(dictionary,3000)

	#save to dictionary
	save_dictionary(dictionary)
	return dictionary

def load_stop_word(lang='en'):
	#extend to other language in next version
	LANGUAGE ={'en': 'english'}
	filename = LANGUAGE['en']
	f = open('./resources/stopwords/'+filename,'r')
	stopwords = {x.rstrip() for x in f.readlines()}
	return stopwords

def save_dictionary(dictionary):
	f = open('./resources/dictionary','w')
	pickle.dump(dictionary,f)
	f.close()

def load_dictionary():
	f = open('../resources/dictionary','r')
	dictionary = pickle.load(f)
	f.close()
	return dictionary




