from __future__ import division
from math import sqrt

def sim_distance(prefs, item1, item2):
    #get the list of shared items
    si = {};
    for item in prefs[item1]:
        if item in prefs[item2]:
            si[item] = 1;
    #if they have no shared items,return 0;
    if len(si) == 0: return 0;

    #Add the squares of all the differences
    sum_of_squares = sum(
        [pow(prefs[item1][item] - prefs[item2][item], 2) for item in prefs[item1] if item in prefs[item2]])
    return 1 / (1 + sqrt(sum_of_squares))


# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0: return 0

    # Sum calculations
    n = len(si)

    # Sums of all the preferences
    sum1 = float(sum([prefs[p1][it] for it in si]))
    sum2 = float(sum([prefs[p2][it] for it in si]))

    # Sums of the squares
    sum1Sq = float(sum([pow(prefs[p1][it], 2) for it in si]))
    sum2Sq = float(sum([pow(prefs[p2][it], 2) for it in si]))

    # Sum of the products
    pSum = float(sum([prefs[p1][it] * prefs[p2][it] for it in si]))

    # Calculate r (Pearson score)
    num = float(pSum - (sum1 * sum2 / n))
    den = float(sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n)))
    if den == 0: return 0

    r = float(num / den)

    return round(r, 7)


def sim_pearson1(prefs, person1, person2):
    #get the list of shared items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    #if they have no shared items, return 0
    if len(si) == 0: return 0

    #find the number of elements
    n = len(si)

    #add up all the prefs
    sum1 = sum([prefs[person1][item] for item in si])
    sum2 = sum([prefs[person2][item] for item in si])

    #calculate the mean of the critics of p1 and p2
    mean1 = sum1 / n;
    mean2 = sum2 / n;

    #calculate the covariance
    covariance = sum([(prefs[person1][item] - mean1) * (prefs[person2][item] - mean2) for item in si]) / n

    #calculate the standard_deviation
    sd1 = sqrt(sum([pow(prefs[person1][item] - mean1, 2) for item in si]) / n)
    sd2 = sqrt(sum([pow(prefs[person2][item] - mean2, 2) for item in si]) / n)

    if sd1 * sd2 == 0: return 0
    #calculate the pearson correlation improved
    pearson = (covariance / (sd1 * sd2))
    return pearson


def sim_pearson_improved(prefs, person1, person2):
    #get the list of shared items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    #if they have no shared items, return 0
    if len(si) == 0: return 0

    #find the number of elements
    n = len(si)

    #get the count of items rated by person
    count1 = 0
    count2 = 0
    for person in prefs[person1]:
        count1 += 1
    for item in prefs[person2]:
        count2 += 1

    totalCount = count1 + count2 - n

    #add up all the prefs
    sum1 = sum([prefs[person1][item] for item in si])
    sum2 = sum([prefs[person2][item] for item in si])

    #calculate the mean of the critics of p1 and p2
    mean1 = sum1 / n;
    mean2 = sum2 / n;

    #calculate the covariance
    covariance = sum([(prefs[person1][item] - mean1) * (prefs[person2][item] - mean2) for item in si]) / n
    #calculate the standard_deviation
    sd1 = sqrt(sum([pow(prefs[person1][item] - mean1, 2) for item in si]) / n)
    sd2 = sqrt(sum([pow(prefs[person2][item] - mean2, 2) for item in si]) / n)

    if sd1 * sd2 == 0: return 0
    #calculate the pearson correlation improved
    pearson = (covariance / (sd1 * sd2)) * (float(n) / float(totalCount))
    #print n,count,float(n)/float(count),pearson
    return pearson


def sim_cosine(prefs, item1, item2):
    si = {}
    for i in prefs[item1]:
        if i in prefs[item2]:
            si[i] = 1
    #print si
    if len(si) == 0: return 0
    x = sqrt(sum([prefs[item1][it] ** 2 for it in si]))
    y = sqrt(sum([prefs[item2][it] ** 2 for it in si]))
    xy = sum([prefs[item1][it] * prefs[item2][it] for it in si])
    cos = xy / (x * y)
    return cos


def sim_cosine_improved(prefs, item1, item2):
    si = {}
    for i in prefs[item1]:
        if i in prefs[item2]:
            si[i] = 1
    #print si
    n = len(si)
    if n == 0: return 0

    count1 = 0
    count2 = 0
    for item in prefs[item1]:
        count1 += 1
    for item in prefs[item2]:
        count2 += 1

    totalCount = count1 + count2 - n

    x = sqrt(sum([prefs[item1][it] ** 2 for it in si]))
    y = sqrt(sum([prefs[item2][it] ** 2 for it in si]))
    xy = sum([prefs[item1][it] * prefs[item2][it] for it in si])
    cos = xy / (x * y)
    return cos * (float(n) / float(totalCount))


def sim_Jaccard(s1, s2, length):
    count = 0
    for i in range(0, length):
        if s1[i] == '1' and s2[i] == '1':
            count += 1
        if s1[i] == '1\n' and s2[i] == '1\n':
            count += 1
    return count / (length - count)


def sim_itemType(s1, s2, length):
    count = 0
    for i in range(0, length):
        if s1[i] == '1' and s2[i] == '1':
            count += 1
        if s1[i] == '1\n' and s2[i] == '1\n':
            count += 1
    return count / 5


def sim_cosine_improved_tag(prefs, item1, item2, movieTags):
    common = 0
    for i in movieTags[item1]:
        if i in movieTags[item2]:
            common += 1
    if common >= 5:
        return 0.8
    else:
        si = {}
        for i in prefs[item1]:
            if i in prefs[item2]:
                si[i] = 1
        #print si
        n = len(si)
        if n == 0: return 0

        count1 = 0
        count2 = 0
        for item in prefs[item1]:
            count1 += 1
        for item in prefs[item2]:
            count2 += 1

        totalCount = count1 + count2 - n

        x = sqrt(sum([prefs[item1][it] ** 2 for it in si]))
        y = sqrt(sum([prefs[item2][it] ** 2 for it in si]))
        xy = sum([prefs[item1][it] * prefs[item2][it] for it in si])
        cos = xy / (x * y)
        return cos * (float(n) / float(totalCount))


#def sim_pearson_improved_typeAdded(prefs,item1,item2):
#	pearson_improved=sim_pearson_improved(prefs,item1,item2)
#	item_type=itemSimSet[item1][item2]
#	return 0.9*(pearson_improved+1)/2.0+0.1*item_type
