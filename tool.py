from __future__ import division
import os
import cPickle as pickle
import similarity


critics={'cla':{'forest gump':8.8,'god http://www.baidu.com/father':8.6,'chunking':8.0,'Paris':9.0,'chow':8.5,'comedy':6.0},
	'kuuga':{'forest gump':8.0,'god father':8.0,'Paris':9.1,'chow':8.4,'comedy':7.0},
	'lee':{'forest gump':8.1,'god father':8.8,'chunking':9.0,'chow':7.8},
	'hyt':{'forest gump':9.0,'god father':9.5,'chunking':7.5,'chow':9.0,'comedy':7.5}
	}
root=os.getcwd()+'//sets/'
def dumpPickle(item,dirPath):
	output=open(root+dirPath,'wb')
	pickle.dump(item,output)
	output.close()
	
def loadPickle(dirPath):
	pkl_file = open(root+dirPath, 'rb')
	data= pickle.load(pkl_file)
	pkl_file.close()
	return data
		
def generate_itemSimOnTypeSet():
	prefs={}
	result={}
	try:
		with open(os.getcwd()+'//ml-100k'+'/u.item') as item:
			for line in item:
				typeVector=line.split('|')[5:24]
				itemId=line.split('|')[0]
				prefs[itemId]=typeVector
				result.setdefault(itemId,{})
	except IOError as err:
		print ('File error: '+ str(err))
	#print similarity.sim_itemType(prefs['1677'],prefs['1678'],19)
	for key1,value1 in prefs.items():
		for key2,value2 in prefs.items():
			if key1!=key2:
				s=similarity.sim_itemType(value1,value2,19)
				print key1,key2,s
				result[key1][key2]=s
	dumpPickle(result,'/itemSimOnType.pkl')
def test():	
	#dumpPickle(critics,'/abc.pkl')
	print r
#~ test()
#generate_itemSimOnTypeSet()
