import random,re,sys,string,math,sets
from collections import defaultdict as dd
if __name__ == '__main__':
	arts = open('ArtsNews.tsv')
	biz = open('BusinessNews.tsv')
	obi = open('ObituariesNews.tsv')
	sports = open('SportsNews.tsv')
	world = open('WorldNews.tsv')
	stopWord  = open('stopword.txt')
	stopList = []
	for word in stopWord:
		word = word.strip()
		stopList.append(word)

	cat1 = []
	cat2 = []
	cat3 = []
	cat4 = []
	cat5 = []
	
	for line in arts:
		line = line.strip()
		line = line.split("\t")
		head = re.findall(r"[\w]+",line[1])
		text = []
		if (len(line ) > 2 ):
			body = re.findall(r"[\w]+",line[2])
			text  = head + body
		else:
			text = head
		#print text
		unique = set()
		for word in text:
			if word not in stopList:
				unique.add(word)
		cat1.append((line[0],unique))
	
	for line in biz:
		line = line.strip()
		line = line.split("\t")
		head = re.findall(r"[\w]+",line[1])
		body = re.findall(r"[\w]+",line[2])
		text  = head + body
		unique = set()
		for word in text:
			if word not in stopList:
				unique.add(word)
		
		cat2.append((line[0],unique))
	for line in obi:
		line = line.strip()
		line = line.split("\t")
		head = re.findall(r"[\w]+",line[1])
		body = re.findall(r"[\w]+",line[2])
		text  = head + body
		unique = set()
		for word in text:
			if word not in stopList:
				unique.add(word)
		cat3.append((line[0],unique))
	for line in sports:
		line = line.strip()
		line = line.split("\t")
		head = re.findall(r"[\w]+",line[1])
		text = []
		if (len(line) >2 ):
			body = re.findall(r"[\w]+",line[2])
			text  = head + body
		else:
			text = head
		unique = set()
		for word in text:
			if word not in stopList:
				unique.add(word)
		
		cat4.append((line[0],unique))
	for line in world:
		line = line.strip()
		line = line.split("\t")
		head = re.findall(r"[\w]+",line[1])
		#body = re.findall(r"[\w\d]+",line[2])
		text = []
		if (len(line) >2 ):
			body = re.findall(r"[\w]+",line[2])
			text  = head + body
		else:
			text = head
		unique = set()
		for word in text:
			if word not in stopList:
				unique.add(word)
		
		cat5.append((line[0],unique))
	
	random.shuffle(cat1)
	test1 = cat1[1:1001]
	cat1 = cat1[1001:2001]
	random.shuffle(cat2)
	test2 = cat2[1:1001]
	cat2 = cat2[1001:2001]
	random.shuffle(cat3)
	test3 = cat3[1:1001]
	cat3 = cat3[1001:2001]
	random.shuffle(cat4)
	test4 = cat4[1:1001]
	cat4 = cat4[1001:2001]
	random.shuffle(cat5)
	test5 = cat5[1:1001]
	cat5 = cat5[1001:2001]

	arts = dict()
	biz = dict()
	obi = dict()
	sports = dict()
	world = dict()

	for cat in cat1:
		for word in cat[1]:
			arts[word] = 0.0
			#print 'l'
	for word in arts:
		for cat in cat1:
			if word in cat[1]:
				arts[word] += 1

	for cat in cat2:
		for word in cat[1]:
			biz[word] = 0.0
	for word in biz:
		for cat in cat2:
			if word in cat[1]:
				biz[word] += 1
			
	for cat in cat3:
		for word in cat[1]:
			obi[word] = 0 
	for word in obi:
		for cat in cat3:
			if word in cat[1]:
				obi[word] += 1
		
	for cat in cat4:
		for word in cat[1]:
			sports[word] = 0 
	for word in sports:
		for cat in cat4:
			if word in cat[1]:
				sports[word] += 1
		
	for cat in cat5:
		for word in cat[1]:
			world[word] = 0 
	for word in world:
		for cat in cat5:
			if word in cat[1]:
				world[word] += 1

	alpha = 100
	beta = 1000

	wordsCount = dict()
	wordsCount['arts'] = arts
	wordsCount['biz'] = biz
	wordsCount['obi'] = obi
	wordsCount['sports'] = sports
	wordsCount['world'] = world

	allWords = set()
	categCount = dict()
	categCount['arts'] = len(cat1) 
	categCount['biz'] = len(cat2)
	categCount['obi'] = len(cat3)
	categCount['sports'] = len(cat4) 
	categCount['world'] = len(cat5)
	
	for categ in wordsCount:
		for word in wordsCount[categ]:
			allWords.add(word)
	bias = dd(lambda: float(0.0))

	for words in allWords:
		for categ in wordsCount:
			if word in wordsCount[categ]:
				bias[categ] += math.log(1 - ((float(wordsCount[categ][word] + alpha -1 )) / float(categCount[categ] + alpha + beta - 2)))
			else:
				bias[categ] += math.log(1 - ((float( alpha -1 )) / float( alpha + beta - 2)))
			if word in wordsCount['arts']:
				bias[categ] -= math.log(1 - ((float(wordsCount['arts'][word] + alpha -1 )) / float(categCount['arts'] + alpha + beta - 2)))
			else:	
				bias[categ] -= math.log(1 - ((float( alpha -1 )) / float( alpha + beta - 2)))


	print bias
	
	#print arts,artsCount
	
	confusionMatrix = dict()

	for i in range(1,6):
		confusionMatrix[i] = dict()
		confusionMatrix[i]['arts'] = 0
		confusionMatrix[i]['biz'] = 0
		confusionMatrix[i]['obi'] = 0
		confusionMatrix[i]['sports'] = 0
		confusionMatrix[i]['world'] = 0
		 
	for doc in test1:
		score = dict()
		for categ in bias:
			score[categ] = bias[categ]

		info_words = dict()
		for word in doc[1]:
			scoreWord = dict()
			scoreBase = 0 
			if word in wordsCount['arts']:
				scoreBase = (float(wordsCount['arts'][word] + alpha -1 )) / float(categCount['arts'] + alpha + beta - 2)
			else:
				scoreBase = (float( alpha -1 )) / float( alpha + beta - 2)
				
			for categ in wordsCount:
				if word in wordsCount[categ]:
					scoreWord[categ] = (float(wordsCount[categ][word] + alpha -1 )) / float(categCount[categ] + alpha + beta - 2)
				else:
					scoreWord[categ] = (float( alpha -1 )) / float( alpha + beta - 2)
				scoreWord[categ] = math.log ( scoreWord[categ] ) + math.log (1 - scoreBase)  - math.log(1 - scoreWord[categ] ) - math.log(scoreBase)
				score[categ] += scoreWord[categ]
		maxarg = ''
		max = -100000000000
		for categ in score:
			if score[categ] > max :
				max = score[categ]
				maxarg = categ

		confusionMatrix[1][maxarg] += 1
	for doc in test2:
		score = dict()
		for categ in bias:
			score[categ] = bias[categ]
		for word in doc[1]:
			scoreWord = dict()
			scoreBase = 0 
			if word in wordsCount['arts']:
				scoreBase = (float(wordsCount['arts'][word] + alpha -1 )) / float(categCount['arts'] + alpha + beta - 2)
			else:	
				scoreBase = (float( alpha -1 )) / float( alpha + beta - 2)
				
			for categ in wordsCount:
				if word in wordsCount[categ]:
					scoreWord[categ] = (float(wordsCount[categ][word] + alpha -1 )) / float(categCount[categ] + alpha + beta - 2)
				else:
					scoreWord[categ] = (float( alpha -1 )) / float( alpha + beta - 2)
				scoreWord[categ] = math.log ( scoreWord[categ] ) + math.log (1 - scoreBase)  - math.log(1 - scoreWord[categ] ) - math.log(scoreBase)
				score[categ] += scoreWord[categ]
		maxarg = ''
		max = -100000000000
		for categ in score:
			if score[categ] >= max :
				max = score[categ]
				maxarg = categ

		confusionMatrix[2][maxarg] += 1
	for doc in test3:
		score = dict()
		for categ in bias:
			score[categ] = bias[categ]
		for word in doc[1]:
			scoreWord = dict()
			scoreBase = 0 
			if word in wordsCount['arts']:
				scoreBase = (float(wordsCount['arts'][word] + alpha -1 )) / float(categCount['arts'] + alpha + beta - 2)
			else:	
				scoreBase = (float( alpha -1 )) / float( alpha + beta - 2)
				
			for categ in wordsCount:
				if word in wordsCount[categ]:
					scoreWord[categ] = (float(wordsCount[categ][word] + alpha -1 )) / float(categCount[categ] + alpha + beta - 2)
				else:
					scoreWord[categ] = (float( alpha -1 )) / float( alpha + beta - 2)
				scoreWord[categ] = math.log ( scoreWord[categ] ) + math.log (1 - scoreBase)  - math.log(1 - scoreWord[categ] ) - math.log(scoreBase)
				score[categ] += scoreWord[categ]
		maxarg = ''
		max = -100000000000
		for categ in score:
			if score[categ] > max :
				max = score[categ]
				maxarg = categ

		confusionMatrix[3][maxarg] += 1
	for doc in test4:
		score = dict()
		for categ in bias:
			score[categ] = bias[categ]
		for word in doc[1]:
			scoreWord = dict()
			scoreBase = 0 
			if word in wordsCount['arts']:
				scoreBase = (float(wordsCount['arts'][word] + alpha -1 )) / float(categCount['arts'] + alpha + beta - 2)
			else:	
				scoreBase = (float( alpha -1 )) / float( alpha + beta - 2)
				
			for categ in wordsCount:
				if word in wordsCount[categ]:
					scoreWord[categ] = (float(wordsCount[categ][word] + alpha -1 )) / float(categCount[categ] + alpha + beta - 2)
				else:
					scoreWord[categ] = (float( alpha -1 )) / float( alpha + beta - 2)
				scoreWord[categ] = math.log ( scoreWord[categ] ) + math.log (1 - scoreBase)  - math.log(1 - scoreWord[categ] ) - math.log(scoreBase)
				score[categ] += scoreWord[categ]
		maxarg = ''
		max = -100000000000
		for categ in score:
			if score[categ] > max :
				max = score[categ]
				maxarg = categ
		confusionMatrix[4][maxarg] += 1
	for doc in test5:
		score = dict()
		for categ in bias:
			score[categ] = bias[categ]
		for word in doc[1]:
			scoreWord = dict()
			scoreBase = 0 
			if word in wordsCount['arts']:
				scoreBase = (float(wordsCount['arts'][word] + alpha -1 )) / float(categCount['arts'] + alpha + beta - 2)
			else:	
				scoreBase = (float( alpha -1 )) / float( alpha + beta - 2)
				
			for categ in wordsCount:
				if word in wordsCount[categ]:
					scoreWord[categ] = (float(wordsCount[categ][word] + alpha -1 )) / float(categCount[categ] + alpha + beta - 2)
				else:
					scoreWord[categ] = (float( alpha -1 )) / float( alpha + beta - 2)
				scoreWord[categ] = math.log ( scoreWord[categ] ) + math.log (1 - scoreBase)  - math.log(1 - scoreWord[categ] ) - math.log(scoreBase)
				score[categ] += scoreWord[categ]
		maxarg = ''
		max = -100000000000
		for categ in score:
			if score[categ] > max :
				max = score[categ]
				maxarg = categ
		confusionMatrix[5][maxarg] += 1
	print confusionMatrix
