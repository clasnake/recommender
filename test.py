import recommender
import similarity
import math
import os
import cPickle as pickle
import pprint
import tool
import evaluation


critics={'cla':{'forest gump':8.8,'god http://www.baidu.com/father':8.6,'chunking':8.0,'Paris':9.0,'chow':8.5,'comedy':6.0},
'kuuga':{'forest gump':8.0,'god father':8.0,'Paris':9.1,'chow':8.4,'comedy':7.0},
'lee':{'forest gump':8.1,'god father':8.8,'chunking':9.0,'chow':7.8},
'hyt':{'forest gump':9.0,'god father':9.5,'chunking':7.5,'chow':9.0,'comedy':7.5}
}

def cal():
	rec=recommender.ItemBasedRecommender('cosine_improved_n150.txt')
	rec.loadTrainingSet()
	rec.loadPredictingSet()
	rec.loadMovieTag()
	#~ print rec.movieTag
	rec.calculateSimilarItems(150,'cosine_improved_n150.pkl')
	
	
def test():
	rec=recommender.ItemBasedRecommender('cosine_improved_n150.txt')
	rec.loadTrainingSet()
	rec.loadPredictingSet()
	#~ rec.calculateSimilarItems(70,'cosine_improved_n70.pkl')
	rec.loadItemMatch('cosine_improved_n150.pkl')
	output=file(rec.outputFile,'w')
	for p in rec.predictPrefs:
		print p[0], p[1], rec.predictRating(p[0],p[1])
		output.write(p[0]+'\t'+p[1]+'\t'+str(rec.predictRating(p[0],p[1]))+'\r\r\n')
	output.close()
	print 'Write success'	

def t():
	rec=recommender.UserBasedRecommender('ub_n80.txt')
	rec.loadTrainingSet()
	rec.loadPredictingSet()

	#~ rec.calculateSimilarUsers(80,'ub_n80.pkl')
	rec.loadUserMatch('ub_n80.pkl')
	output=file(rec.outputFile,'w')
	for p in rec.predictPrefs:
		print p[0], p[1], rec.predictRating(p[0],p[1])
		output.write(p[0]+'\t'+p[1]+'\t'+str(rec.predictRating(p[0],p[1]))+'\r\r\n')
	output.close()
	
def t1():
	print evaluation.Evaluation('/u1.test',rec=recommender.UserBasedRecommender('/u1.base')).evalByAccuracy()
	#print evaluation.Evaluation('/u1.test',rec=recommender.ItemBasedRecommender('/u1.base',itemMatch=tool.loadPickle('/cosineImproved_n90'))).evalByAccuracy()
	#a=recommender.ItemBasedRecommender('/u1.base')
	#a.calculateSimilarItems(n=90)

def tcos():
	a=recommender.Recommender('/u2.base')
	train=a.loadBaseFileOnItem()
	print similarity.sim_pearson(critics,'Cla','lee')

def t2():
	data1 = {'a': [1, 2.0, 3, 4+6j],
         'b': ('string', u'Unicode string'),
         'c': None}

	#selfref_list = [1, 2, 3]
	#selfref_list.append(selfref_list)

	output = open('data.pkl', 'wb')

	# Pickle dictionary using protocol 0.
	pickle.dump(critics, output)

	# Pickle the list using the highest protocol available.
	#pickle.dump(selfref_list, output, -1)

	output.close()
	
def t3():
	pkl_file = open('data.pkl', 'rb')

	data1 = pickle.load(pkl_file)
	pprint.pprint(data1)

	#data2 = pickle.load(pkl_file)
	#pprint.pprint(data2)

	pkl_file.close()

def t4():
	a=[]
	try:
		with open(os.getcwd()+'//ml-100k'+'/u.item') as item:
			for line in item:
				a=line.split('|')[5:24]
				print a
				#(itemId,title)=line.split('|')[0:2]
				#movies[itemId]=title
	except IOError as err:
		print ('File error: '+str(err))

t4()
