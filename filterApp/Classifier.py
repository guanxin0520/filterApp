"""class for classifier 
	include train, load, update, dataset, update_dataset, predict
	
"""
import models
from svm import *
from svmutil import *

class Classifier:
	#parameter

	__dataset = []
	__label = []
	__classifier = None
	__id = 0
	__user = None


	def __init__(self, user, id=0):
		self.__user = user
		if id !=0:
			self.__id = id
			self.load()
		else:
			#emptry classifier
			pass
		

	def load(self):
		self.__classifier = svm_load_model('./resources/classifier/classifier_'+str(self.__id)+'.model')

	def getClassifier(self):
		return self.__classifier

	def setDataset(self, dataset,labelset):
		self.__dataset = dataset
		self.__label = labelset


	def train(self):
		if not self.__dataset:
			return
		self.__classifier = svm_train(self.__label,self.__dataset, '-s 1 -t 0 -c 4')
		

	def update(self,dataset,labelset):
		self.__dataset.extend(dataset)
		self.__label.extend(labelset)
		self.__classifier = svm_train(self.__label,self.__dataset, '-t 0 -s 1 -c 4')
		

	def predict(self, items, labels = None):
		if not labels:
			labels = [0]*len(items)
		p_label, p_acc, p_val = svm_predict(labels,[item.vector for item in items],self.__classifier)

		return p_label,p_acc,p_val

	def save(self):
		if self.__classifier is None:
			return

		c = models.UserFilter(user = self.__user)
		c.save()
		self.__id = c.id
		svm_save_model('./resources/classifier/classifier_'+str(self.__id)+'.model',self.__classifier)

	@property
	def id(self):
		return self.__id

	def __unicode__(self):
		return srt(self.__id)




