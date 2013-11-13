#!/usr/bin/python

'''
Python script to fetch 2000 most recent articles from New York Times for 5 categories 
Author: Vipul Raheja (vr2337@columbia.edu)
'''

import csv
import json
import requests
import simplejson

categories = ['Arts','Business','Obituaries','Sports','World']

artsNews = []
businessNews = []
sportsNews = []
obituariesNews = []
worldNews = []

def writeTSV(newsList, category):
	filename = category + 'News.tsv'
	with open(filename, 'w') as the_file:
		csv.register_dialect("custom", delimiter=" ", skipinitialspace=True)
		writer = csv.writer(the_file, dialect="custom")
		for tup in newsList:
			writer.writerow(tup)

def storeNews(newsList, newsJSONContent):
	newsList.append([newsJSONContent["web_url"].encode('utf-8'),
		newsJSONContent["headline"]["main"].encode('utf-8'),
		newsJSONContent["lead_paragraph"].encode('utf-8')])

for category in categories:
	num_articles = 0
	page = 0
	while num_articles < 2000:
		URL = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=30fe7b12e3d707828361677f9c6d42dd:8:68400593&fq=news_desk:("' + category + '")&fl=web_url,headline,news_desk,lead_paragraph,word_count&begin_date=19810601&end_date=20131112&page=' + str(page)
		print URL

		r = requests.get(URL)
		c = r.content
		j = simplejson.loads(c)
		num_articles += len(j["response"]["docs"])
		page += 1
		print num_articles

#		print j["response"]["docs"][9]["news_desk"]
		for i in range(0,10):
			if category is 'Arts':
				storeNews(artsNews,j["response"]["docs"][i])
				writeTSV(artsNews,"Arts")
			elif category is 'Business':
				storeNews(businessNews,j["response"]["docs"][i])
				writeTSV(businessNews,"Business")
			elif category is 'Sports':
				storeNews(sportsNews,j["response"]["docs"][i])
				writeTSV(sportsNews,"Sports")
			elif category is 'Obituaries':
				storeNews(obituariesNews,j["response"]["docs"][i])
				writeTSV(obituariesNews,"Obituaries")
			elif category is 'World':
				storeNews(worldNews,j["response"]["docs"][i])
				writeTSV(worldNews,"World")
