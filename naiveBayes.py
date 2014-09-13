#!/usr/bin/python

"""
A Python implementation of the Naive-Bayes algorithm.
Author: Vipul Raheja (vr2337@columbia.edu)
"""
import csv
import re
import string
from nltk.tokenize import word_tokenize
import collections
import operator
from collections import defaultdict
import random
import math
import numpy as np

def processData(artsRawData, tokenized_filtered_arts_docs):
	artsData = []
	tokenized_arts_docs = []
	for doc in artsRawData:
		doc[1] = doc[1] + " " + doc[2]
		url = doc[0]
		del doc[-1]
		x = [''.join(c for c in s if c not in string.punctuation) for s in doc]
		artsData.append([url,x[1]])
		tokenized_arts_docs.append([word_tokenize(field.lower()) for field in x[1:]])

	stopwords = [line.strip() for line in open('stopword.txt')]

	for tokenized_words_docs in tokenized_arts_docs:
		for w in tokenized_words_docs:
			non_stop_words = []
			for i in w:
				if not i in stopwords:
					non_stop_words.append(i)
			tokenized_filtered_arts_docs.append(non_stop_words)
	return tokenized_filtered_arts_docs


def createDict(counts_dict, tokenized_filtered_docs):
	for doc in tokenized_filtered_docs:
		unique_words = []
		for word in doc:
			if not word in unique_words:
				unique_words.append(word)

		for w in unique_words:
			if not w in counts_dict:
				counts_dict[w] = 1
			else:
				counts_dict[w] += 1


def randomizeIndices():
	a = range(0,2000)
	random.shuffle(a)
	return a

def main():
	# Initializations
	alpha = 2
	beta = 5000
	n_c = 2000
	classes = ['Arts', 'Business', 'Sports', 'Obituaries', 'World']
	classes_id = list(range(5))

	# Read Data
	artsRawData = csv.reader(open('ArtsNews.tsv','r'), delimiter='\t')
	businessRawData = csv.reader(open('BusinessNews.tsv','r'), delimiter='\t')
	sportsRawData = csv.reader(open('SportsNews.tsv','r'), delimiter='\t')
	obituariesRawData = csv.reader(open('ObituariesNews.tsv','r'), delimiter='\t')
	worldRawData = csv.reader(open('WorldNews.tsv','r'), delimiter='\t')

	# Initialize lists
	tokenized_arts_docs = []
	tokenized_filtered_arts_docs = []	
	tokenized_business_docs = []
	tokenized_filtered_business_docs = []
	tokenized_sports_docs = []
	tokenized_filtered_sports_docs = []
	tokenized_obituaries_docs = []
	tokenized_filtered_obituaries_docs = []
	tokenized_world_docs = []
	tokenized_filtered_world_docs = []

	# Process the data
	tokenized_filtered_arts_docs = processData(artsRawData, tokenized_filtered_arts_docs)
	tokenized_filtered_business_docs = processData(businessRawData, tokenized_filtered_business_docs)
	tokenized_filtered_sports_docs = processData(sportsRawData, tokenized_filtered_sports_docs)
	tokenized_filtered_obituaries_docs = processData(obituariesRawData, tokenized_filtered_obituaries_docs)
	tokenized_filtered_world_docs = processData(worldRawData, tokenized_filtered_world_docs)

	#print tokenized_filtered_arts_docs

	# Initialize Dictionaries
	arts_counts = dict()
	business_counts = dict()
	sports_counts = dict()
	obituaries_counts = dict()
	world_counts = dict()

	# Create Dictionaries
	createDict(arts_counts, tokenized_filtered_arts_docs)
	createDict(business_counts, tokenized_filtered_business_docs)
	createDict(sports_counts, tokenized_filtered_sports_docs)
	createDict(obituaries_counts, tokenized_filtered_obituaries_docs)
	createDict(world_counts, tokenized_filtered_world_docs)

	
	
#	a = range(0,2000)
#	random.shuffle(a)
#	testNews = [tokenized_filtered_arts_docs[b][c] for b in a[:20] for c in range(2,3)]
#	print testNews

#	print tokenized_filtered_arts_docs

	# CREATING TRAINING/TESTING DATA
	for c in classes_id:
		train_indices = randomizeIndices()
		tr = []
		te = []

		if c is 0:
			train_arts = []
			test_arts = []
			for i in range(0,1000):
				tr.append(tokenized_filtered_arts_docs[train_indices[i]])
			for i in range(1000,2000):
				te.append(tokenized_filtered_arts_docs[train_indices[i]])
			for i in tr:
				train_arts += i
			train_arts_doc = tr
			test_arts = te
		elif c is 1:
			train_business = []
			test_business = [] 
			for i in range(0,1000):
				tr.append(tokenized_filtered_business_docs[train_indices[i]])
			for i in range(1000,2000):
				te.append(tokenized_filtered_business_docs[train_indices[i]])
			for i in tr:
				train_business += i
			train_business_doc = tr
			test_business = te
		elif c is 2:
			train_sports = []
			test_sports = [] 
			for i in range(0,1000):
				tr.append(tokenized_filtered_sports_docs[train_indices[i]])
			for i in range(1000,2000):
				te.append(tokenized_filtered_sports_docs[train_indices[i]])
			for i in tr:
				train_sports += i
			train_sports_doc = tr
			test_sports = te
		elif c is 3:
			train_obituaries = []
			test_obituaries = []
			for i in range(0,1000):
				tr.append(tokenized_filtered_obituaries_docs[train_indices[i]])
			for i in range(1000,2000):
				te.append(tokenized_filtered_obituaries_docs[train_indices[i]])
			for i in tr:
				train_obituaries += i
			train_obituaries_doc = tr
			test_obituaries = te
		elif c is 4:
			train_world = []
			test_world = []
			for i in range(0,1000):
				tr.append(tokenized_filtered_world_docs[train_indices[i]])
			for i in range(1000,2000):
				te.append(tokenized_filtered_world_docs[train_indices[i]])
			for i in tr:
				train_world += i
			train_world_doc = tr
			test_world = te

	# MERGING TRAINING/TESTING DATA
	# Collection of words
	train_data = train_arts + train_business + train_sports + train_obituaries + train_world
	test_data = test_arts + test_business + test_sports + test_obituaries + test_world

	# CORRECT LABELS
	correct_labels = []
	for i in range(0,5):
		for j in range(0,1000):
			correct_labels.append(i)

	w_j_0 = dict()
	w_0_c = dict()
	w_j_c = dict()

	for i in range(0,len(classes)):
		w_j_c[i] = dict()
		w_0_c[i] = 0

	trainNews = train_data

#	x_j = [[0 for i in range(1000)] for i in range(1000)]
#	for word in trainNews:
#		for i in range(1000):
#			x_j[word][i] = 1

	for c in range(0,5):	
		print c
		for word in trainNews:
			if c is 0:
				class_counts = arts_counts
				tokenized_docs = tokenized_filtered_arts_docs
			elif c is 1:
				class_counts = business_counts
				tokenized_docs = tokenized_filtered_business_docs
			elif c is 2:
				class_counts = sports_counts
				tokenized_docs = tokenized_filtered_sports_docs
			elif c is 3:
				class_counts = obituaries_counts
				tokenized_docs = tokenized_filtered_obituaries_docs
			elif c is 4:
				class_counts = world_counts
				tokenized_docs = tokenized_filtered_world_docs

			n = 5*1000
			
			# CATEGORY THETA
			n_c = len(tokenized_docs)
			if word in class_counts:
				n_j_c = class_counts[word]
			else:
				n_j_c = 0
			theta_c = n_c*(1.0)/n
			theta_j_c = (n_j_c + alpha - 1)*(1.0)/(n_c + alpha + beta - 2)

			# ARTS THETA
			n_0 = len(tokenized_filtered_arts_docs)
			if word in arts_counts:
				n_j_0 = arts_counts[word]
			else:
				n_j_0 = 0
			theta_0 = n_0*(1.0)/n
			theta_j_0 = (n_j_0 + alpha - 1)*(1.0)/(n_0 + alpha + beta - 2)
				
			# COMPUTING W_0_C
			w_0_c[c] += math.log(1-theta_j_c) - math.log(1-theta_j_0)

		# ADDING CONSTANT TERM
		w_0_c[c] += math.log(theta_c) - math.log(theta_0)
	
		print "W_0_C:"
		print w_0_c[c]

	print w_0_c

	confusionMatrix = dict()	
	for i in range(1,6):
		confusionMatrix[i] = dict()
		confusionMatrix[i]['Arts'] = 0
		confusionMatrix[i]['Business'] = 0
		confusionMatrix[i]['Sports'] = 0
		confusionMatrix[i]['Obituaries'] = 0
		confusionMatrix[i]['World'] = 0


	print "---------------------------------------"
	print "TESTING"

	print len(test_sports)

	predicted_labels = [0 for i in range(len(test_data))]
	k = 0
	for doc in test_data:
		score_category = [0 for i in range(5)]
		for c in range(0,5):
			score_category[c] = w_0_c[c]
			
		for word in doc:
			score_word = [0 for i in range(5)]
			for c in range(0,5):
				if c is 0:
					class_counts = arts_counts
					tokenized_docs = tokenized_filtered_arts_docs
				elif c is 1:
					class_counts = business_counts
					tokenized_docs = tokenized_filtered_business_docs
				elif c is 2:
					class_counts = sports_counts
					tokenized_docs = tokenized_filtered_sports_docs
				elif c is 3:
					class_counts = obituaries_counts
					tokenized_docs = tokenized_filtered_obituaries_docs				
				elif c is 4:
					class_counts = world_counts
					tokenized_docs = tokenized_filtered_world_docs				
			
				n = 1000
				# ARTS THETA
				n_0 = len(tokenized_filtered_arts_docs)
				if word in arts_counts:
					n_j_0 = arts_counts[word]
				else:
					n_j_0 = 0
				theta_0 = n_0*(1.0)/n
				theta_j_0 = (n_j_0 + alpha - 1)*(1.0)/(n_0 + alpha + beta - 2)

				# CATEGORY THETA
				n_c = len(tokenized_docs)
				if word in class_counts:
					n_j_c = class_counts[word]
				else:
					n_j_c = 0
				theta_c = n_c*(1.0)/n
				theta_j_c = (n_j_c + alpha - 1)*(1.0)/(n_c + alpha + beta - 2)

				# log-ratio
				score_word[c] = math.log(theta_j_c) + math.log(1 - theta_j_0)  - math.log(1 - theta_j_c) - math.log(theta_j_0)
				score_category[c] += score_word[c]

		maxarg = -100000
		max_v = -100000
		for c in range(0,5):
			score = score_category[c]
			if score > max_v:
				max_v = score
				maxarg = c

		predicted_labels[k] = maxarg
		k += 1


	print "ACCURACIES"
	print predicted_labels

	acc = 0
	for i in range(0,len(test_data)):
		if correct_labels[i] == predicted_labels[i]:
			acc += 1
	print acc
	

if __name__ == "__main__":
	main()
