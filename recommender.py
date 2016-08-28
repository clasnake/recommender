#recommender.py includes a class 'Recommender' which provides
#basic functions of a certain recommender
from __future__ import division
import os
import pprint

import similarity
import cPickle as pickle
import tool


class Recommender:
    def __init__(self, outputFile, similarityMeasure, pathStr, trainingSet, predictingSet):
        self.outputFile = os.getcwd() + '//results/' + outputFile
        self.pathStr = pathStr
        self.trainingSet = trainingSet
        self.predictingSet = predictingSet
        self.prefs = {}
        self.predictPrefs = []
        self.movieTag = {}
        self.similarityMeasure = similarityMeasure

    def loadTrainingSet(self):
        prefs = {}
        #prefsOnTitle={}
        try:
            with open(self.pathStr + self.trainingSet) as train:
                for line in train:
                    (userId, movieId, rating, time) = line.split('\t')
                    prefs.setdefault(userId, {})
                    prefs[userId][movieId] = float(rating)

        except IOError as err:
            print('File error: ' + str(err))
        self.prefs = prefs

    def loadPredictingSet(self):
        prefs = []
        try:
            with open(self.pathStr + self.predictingSet) as predict:
                for line in predict:
                    (userId, movieId, rating, time) = line.split('\t')
                    movieId = movieId.replace('\r\r\n', '')
                    prefs.append((userId, movieId))

        except IOError as err:
            print('File error: ' + str(err))
        self.predictPrefs = prefs


    def transformPrefs(self, prefs):
        result = {}
        for person in prefs:
            for item in prefs[person]:
                result.setdefault(item, {})
                result[item][person] = prefs[person][item]
        return result

    def topMatches(self, prefs, item, similarityMeasure, n=100):
        if similarityMeasure == similarity.sim_cosine_improved_tag:
            scores = [(similarityMeasure(prefs, item, other, self.movieTag), other) for other in prefs if other != item]
        else:
            scores = [(similarityMeasure(prefs, item, other), other) for other in prefs if other != item]

        scores.sort()
        scores.reverse()
        return scores[0:n]

    def getRecommendedItems(self, user):
        return None

    def predictRating(self, user, movie):
        return None


class ItemBasedRecommender(Recommender):
    def __init__(self, outputFile, similarityMeasure):
        Recommender.__init__(self, outputFile, similarityMeasure=similarity.sim_cosine_improved,
                             pathStr=os.getcwd() + '//ml-100k/', trainingSet='u1.base',
                             predictingSet='u1.test')
        self.itemMatch = None

    def calculateSimilarItems(self, n, resultFile):
        # Create a dictionary of items showing which other items they
        # are most similar to.
        result = {}
        c = 0
        # self.loadMovieTag()

        # for i in prefsOnItem:
        #     if i not in self.movieTag:
        #         self.movieTag[i] = []
        prefsOnItem = self.transformPrefs(self.prefs)
        for i in prefsOnItem.keys():
            result.setdefault(i, [])
        for item in prefsOnItem:
            # Status updates for large datasets
            c += 1
            if c % 5 == 0: print
            "%d / %d" % (c, len(prefsOnItem))
            # Find the most similar items to this one
            scores = self.topMatches(prefsOnItem, item, similarityMeasure=self.similarityMeasure, n=n)
            result[item] = scores
        tool.dumpPickle(result, resultFile)

    #return result

    def loadItemMatch(self, itemFile):
        self.itemMatch = tool.loadPickle(itemFile)

    def predictRating(self, user, movie):
        totals = 0.0
        simSums = 0.0
        sim = 0.0
        predict = 0
        itemList = self.itemMatch[movie]
        for other in itemList:
            if other[1] == movie:
                continue
            sim = other[0]
            if sim <= 0:
                continue
            if movie not in self.prefs[user] or self.prefs[user][movie] == 0:
                if other[1] in self.prefs[user]:
                    #~ print 'test'
                    totals += self.prefs[user][other[1]] * sim
                    simSums += sim
        if simSums == 0:
            predict = 4.0
        else:
            predict = totals / simSums
        return predict


    def getRecommendedItems(self, user):
        prefsOnUser = self.loadBaseFileOnUser()
        #itemMatch=tool.loadPickle('/ItemSimOnSet1_n40_typeAdded.pkl')
        userRatings = prefsOnUser[user]
        scores = {}
        totalSim = {}
        # Loop over items rated by this user
        for (item, rating) in userRatings.items():

            # Loop over items similar to this one
            for (similarity, item2) in self.itemMatch[item]:
                if similarity <= 0: continue
                # Ignore if this user has already rated this item
                if item2 in userRatings: continue
                # Weighted sum of rating times similarity
                scores.setdefault(item2, 0)
                scores[item2] += similarity * rating

                # Sum of all the similarities
                totalSim.setdefault(item2, 0)
                totalSim[item2] += similarity

        # Divide each total score by total weighting to get an average
        rankings = [(round(score / totalSim[item], 7), item) for item, score in scores.items()]

        # Return the rankings from highest to lowest
        rankings.sort()
        rankings.reverse()
        return rankings


class UserBasedRecommender(Recommender):
    def __init__(self, outputFile, similarityMeasure):
        Recommender.__init__(self, outputFile, similarityMeasure=similarity.sim_cosine_improved,
                             pathStr=os.getcwd() + '//data-v/', trainingSet='training_set.txt',
                             predictingSet='predict.txt')
        self.userMatch = None

    def calculateSimilarUsers(self, n, resultFile):
        result = {}
        c = 0
        for i in self.prefs.keys():
            result.setdefault(i, [])
        for user in self.prefs:
            c += 1
            if c % 5 == 0:
                print
                "%d / %d" % (c, len(self.prefs))
            scores = self.topMatches(self.prefs, user, similarityMeasure=self.similarityMeasure, n=n)
            result[user] = scores
        #~ print result[user]
        tool.dumpPickle(result, resultFile)


    def loadUserMatch(self, userFile):
        self.userMatch = tool.loadPickle(userFile)

    def predictRating(self, user, movie):
        totals = 0.0
        simSums = 0.0
        sim = 0.0
        predict = 0
        userList = self.userMatch[user]
        for other in userList:
            if other[1] == user:
                continue
            sim = other[0]
            if sim <= 0:
                continue
            if movie not in self.prefs[user] or self.prefs[user][movie] == 0:
                if movie in self.prefs[other[1]]:
                    totals += self.prefs[other[1]][movie] * sim
                    simSums += sim
        if simSums == 0:
            predict = 4.0
        else:
            predict = totals / simSums
        return predict

    #~ def predictRating(self, user, movie):
    #~ totals=0.0
    #~ simSums=0.0
    #~ sim=0.0
    #~ predict=0
    #~ matchlist=self.topMatches(self.prefs, user, similarityMeasure=similarity.sim_pearson_improved,n=80)
    #~ for other in matchlist:
    #~ if other[1]==user:
    #~ continue
    #~ sim=other[0]
    #~ if sim<=0:
    #~ continue
    #~ if movie not in self.prefs[user] or self.prefs[user][movie]==0:
    #~ if movie in self.prefs[other[1]]:
    #~ totals+=self.prefs[other[1]][movie]*sim
    #~ simSums+=sim
    #~ print "simSums",simSums
    #~ print "totals",totals
    #~ if simSums==0:
    #~ predict=4.0
    #~ else:
    #~ predict=totals/simSums
    #~ print predict
    #~ return predict

    def getRecommendedItems(self, user):
        prefs = self.loadTrainingSet()
        totals = {}
        simSums = {}
        sim = 0.0
        for other in self.topMatches(prefs, user, similarityMeasure=similarity.sim_cosine, n=90):
            #don't compare me to myself
            if other[1] == user: continue
            sim = other[0]
            #ignore scores of zero or lower
            if sim <= 0: continue
            for item in prefs[other[1]]:
                #only score movies I haven't seen yet
                if item not in prefs[user] or prefs[user][item] == 0:
                    #similarity*score
                    totals.setdefault(item, 0)
                    totals[item] += prefs[other[1]][item] * sim
                    #sum of similarities
                    simSums.setdefault(item, 0)
                    simSums[item] += sim

        #create the normalized list
        rankings = [(total / simSums[item], item) for item, total in totals.items()]

        #return the sorted list
        rankings.sort()
        rankings.reverse()
        return rankings
