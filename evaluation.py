from __future__ import division
import os
from math import sqrt

import recommender
import similarity


class Evaluation:
    def __init__(self, testFile, rec=recommender.ItemBasedRecommender('/u2.base', similarity.sim_cosine),
                 pathStr=os.getcwd() + '//ml-100k', userFile='/u.user'):
        self.testFile = testFile
        self.rec = rec
        self.pathStr = pathStr
        self.userFile = userFile

    def loadTestFileOnUser(self):
        prefsOnId = {}
        #prefsOnTitle={}
        try:
            with open(self.pathStr + self.userFile) as user:
                for line in user:
                    (userId, userAge) = line.split('|')[0:2]
                    prefsOnId.setdefault(userId, {})
                #prefsOnTitle.setdefault(userId,{})
        except IOError as err:
            print ('File error: ' + str(err))
        try:
            with open(self.pathStr + self.testFile) as t:
                for line in t:
                    (userid, itemid, rating, ts) = line.split('\t')
                    prefsOnId[userid][itemid] = float(rating)
                #prefsOnTitle[userid][self.getMovieTitle()[itemid]]=float(rating)
        except IOError as err:
            print ('File error: ' + str(err))
        return prefsOnId

    def evalByAccuracy(self):
        sumForMAE = 0
        sumForRMSE = 0
        sumForMBDnum = 0
        sumForMBDdenum = 0
        count = 0
        testingSet = self.loadTestFileOnUser()
        for user in testingSet:
            print "------------", user, "--------"
            recList = self.rec.getRecommendedItems(user)
            for recItem in recList:
                if recItem[1] in testingSet[user]:
                    count += 1
                    dif = recItem[0] - testingSet[user][recItem[1]]
                    print count, ":", dif
                    sumForRMSE += abs(dif) ** 2
                    sumForMAE += abs(dif)
                    sumForMBDnum += dif
                    sumForMBDdenum += testingSet[user][recItem[1]]

        MAE = sumForMAE / count
        RMSE = sqrt(sumForRMSE / count)
        MBD = (float(sumForMBDnum) / count) / (float(sumForMBDdenum) / count) * 100 
        return MAE, RMSE, MBD, count

    def evalByAccuracy2(self):
        sumForMAE = 0
        sumForRMSE = 0
        sumForMBDnum = 0
        sumForMBDdenum = 0
        count = 0
        testingSet = self.loadTestFileOnUser()
        for user in testingSet:
            print "------------", user, "--------"
            recList = self.rec.getRecommendedItems(user)
            for item in testingSet[user]:
                for recItem in recList:
                    if recItem[1] == item:
                        count += 1
                        dif = recItem[0] - testingSet[user][recItem[1]]
                        print count, ":", dif
                        sumForRMSE += abs(dif) ** 2
                        sumForMAE += abs(dif)
                        sumForMBDnum += dif
                        sumForMBDdenum += testingSet[user][recItem[1]]

        MAE = sumForMAE / count
        RMSE = sqrt(sumForRMSE / count)
        MBD = (float(sumForMBDnum) / count) / (float(sumForMBDdenum) / count) * 100 
        return MAE, RMSE, MBD, count