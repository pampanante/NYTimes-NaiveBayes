#!/usr/bin/python

"""
A Python implementation of the Naive-Bayes algorithm.
Author: Vipul Raheja (vr2337@columbia.edu)
"""

import json
import csv
import simplejson
import requests

#class naiveBayes:
#	def __init__(self,n):


def main():
	r = requests.get('http://api.nytimes.com/svc/search/v1/article?format=json&query=nytd_section_facet:[Sports]&offset=0&rank=newest&api-key=30fe7b12e3d707828361677f9c6d42dd:8:68400593')
	c = r.content
	j = simplejson.loads(c)
	
	a = len(j["results"])
	
	for item in range(1,a):
		print j["results"][item]["body"]

main()
