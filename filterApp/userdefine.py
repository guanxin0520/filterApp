"""
User defined functions:

users need to program some code based on the format of their content.
XML, text file, cvs. And get the titlt, author, url, text, and date 
from original article, save it to item.
item class has title, author, url, date, and vector.

"""
import json
import sys,getopt
import utilities
from datetime import datetime
import nltk
import re
from collections import Counter

def init_database(path,lang = 'en'):
	"""
		initial the database when the website was create, 
		users need to code how to get item from original source
	"""
	#here is a sample
	#assume the initial database save in a file
	f = open(path,'r')
	
	#load/ or build dictionary by give the function a word set begin
	wordlist = set()
	for line in f.readlines():
		temp = re.sub(r'[^\w]|[\d+]',' ',line).lower()
		a = {x for x in nltk.word_tokenize(temp) if len(x) >2}
		wordlist = wordlist.union(a)
		if len(wordlist)> 10000:
			break
	#create a word set end

	dictionary = utilities.build_dictionary(wordlist,lang)

	stopwords = utilities.load_stop_word()

	#build the database fixture file begin
	f.seek(0)
	f_o = open('./filterApp/fixtures/initial_data.yaml','w')
	i = 0
	#f_o.write('[\n')
	for line in f.readlines():
		temp = re.sub(r'[^\w]|[\d+]',' ',line).lower()
		a = [x for x in nltk.word_tokenize(temp) if len(x) >2 and x not in stopwords and x in dictionary]
		text = dict(Counter(a))
		#change string key to index based on dictionary list
		vector = dict((dictionary.index(key),value) for key, value in text.iteritems())


		#create new item
		title = 'here is the title'
		author = 'authorA'
		date = datetime.now()
		url = 'http://www.gmu.edu/'

		#f_o.write('{"model":"filterApp.Item", "fields":{'+'"title": "{0}", "author": "{1}", "date": "{2}", "url": "{3}", "vector": \'{4}\'' \
		#	.format(title,author,str(date),url,json.dumps(vector))+'}},\n')
		i = i+1
		f_o.write('- model: filterApp.item \n  pk: '+str(i)+' \n'+'  fields: \n    '+'title: \'{0}\'\n    author: \'{1}\'\n    date: \'{2}\'\n    url: \'{3}\'\n    vector: \'{4}\' ' \
			.format(title,author,str(date),url,json.dumps(vector))+'\n')
		#save to fixture file
		
	#f_o.write(']\n')
	f_o.close()
	f.close()
	#build the database fixture file end
	#sample end
	return

#download future data and save it to database.
def download(timestamp):
	pass

def main(argv):

	try:
		opts, args = getopt.getopt(argv,"hi:d:",["ifile=","timestamp="])
	except getopt.GetoptError:
		print 'dataget.py -para\n -i <inputfile> initial database\n -d <timestamp>  download new data'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'dataget.py -para\n -i <inputfile> initial database\n -d <timestamp>  download new data'
			sys.exit()
		elif opt in ("-i", "--ifile","--initial"):
			inputfile = arg
			init_database(inputfile)
		elif opt in ("-d", "--download"):
			timestamp = arg
			download(timestamp)
	

if __name__ == "__main__":
   main(sys.argv[1:])
