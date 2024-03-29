from copy import deepcopy
from math import pi, cos, sin
from Primitives.vectors import Vector2
from constants import *

def clamp(value, precision):
    '''Clamp a value'''
    val = round(value, precision)
    #val = round(value, 0)
    #val = round(value)
    if val == 0.0:
        val = abs(val)
    return val

def clampVector(vector, precision):
    '''Clamp a vector, similar to above.  Return the clamped vector'''
    x = clamp(vector.x, precision)
    y = clamp(vector.y, precision)
    return Vector2(x, y)

def vectorOnRight(segment, other):
    '''Check if the other vector is to the right of vector.  Return True'''
    print("RIGHT? " + str(segment) + " and " + str(other))
    #print(str(segment.direction) + " and " + str(other.direction))
    test1 = segment.direction == other.direction
    test2 = segment.direction == (other.direction*-1)
    #print(str(test1) + ", " + str(test2))
    #if not test1 and not test2:
    v1 = other.p1 - segment.p1
    v2 = other.p2 - segment.p1
    v1norm = v1.normalize()
    v2norm = v2.normalize()
    v1norm = clampVector(v1norm, 2)
    v2norm = clampVector(v2norm, 2)
    #print(str(v1norm) + " :: " + str(v2norm))
    if v1norm == v2norm == segment.direction:
        return False
    elif v1norm == v2norm == (segment.direction*-1):
        return False
    val1 = segment.vector.cross(v1)
    val2 = segment.vector.cross(v2)
    val1 = clamp(val1, 0)
    val2 = clamp(val2, 0)
    #print("NOT ON LINE")
    print(val1, val2)
    if val1 > 0 or val2 > 0:
        return True
    return False
    

def vectorOnLeft(segment, other):
    '''Check if the other vector is to the left of vector.  Return True'''
    print("LEFT? " + str(segment) + " and " + str(other))
    #print(str(segment.direction) + " and " + str(other.direction))
    test1 = segment.direction == other.direction
    test2 = segment.direction == (other.direction*-1)
    #print(str(test1) + ", " + str(test2))
    #if not test1 and not test2:
    v1 = other.p1 - segment.p1
    v2 = other.p2 - segment.p1
    v1norm = v1.normalize()
    v2norm = v2.normalize()
    v1norm = clampVector(v1norm, 2)
    v2norm = clampVector(v2norm, 2)
    if v1norm == v2norm == segment.direction:
        return False
    elif v1norm == v2norm == (segment.direction*-1):
        return False
    #print(str(v1norm) + " :: " + str(v2norm))
    val1 = segment.vector.cross(v1)
    val2 = segment.vector.cross(v2)
    val1 = clamp(val1, 0)
    val2 = clamp(val2, 0)
    #print("NOT ON LINE")
    print(val1, val2)
    if val1 < 0 or val2 < 0:
        return True
    return False

def sameDirection(segment, other):
    '''Check to see if the other segment points in the same direction as segment'''
    if segment.direction == other.direction:
    #angle = segment.vector.angle(other.vector)
    #angle = clamp(angle, 5)
    #if angle == 0:
        return True
    return False

def pairExists(pair, pairlist):
    '''Check if the pair is in the pairlist.  pairlist is a list of tuples and pair is a list'''
    pair2 = deepcopy(pair)
    pair2.reverse()
    if tuple(pair) in pairlist or tuple(pair2) in pairlist:
        return True
    return False

def getMinimumValue(someDict):
    '''Get the minimum value in the dictionary'''
    values = list(someDict.values())
    return min(values)

def otherPairValue(pair, value):
    '''Given a pair as a tuple or a list and a value, return the other value from the pair'''
    return pair[pair.index(value)-1]

def diffList(list1, list2):
    '''Return a list of objects in list1 that is not in list2'''
    result = []
    for obj in list1:
        if obj not in list2:
            result.append(obj)
    return result

def removeKeys(d, keys):
    '''Remove the keys from the dictionary'''
    for key in keys:
        if key in d.keys():
            d.pop(key)
    return d

def intersect(p1, p2, v1, v2):
    '''Find the intersect scalars for both segments/rays.  Just need 2 positions and 2 direction vectors.'''
    #print(str(p1)+" "+str(p2) + " " + str(v1) + " " + str(v2))
    s, t = None, None
    denom = float(v1.cross(v2))
    if denom != 0:
        p = p2 - p1
        s = p.cross(v2) / denom
        t = p.cross(v1) / denom
        s = clamp(s, 2)
        t = clamp(t, 2)
    return s, t

def intersectSegments(segment1, segment2):
    '''Same as above, but this time we can just include the segments instead of positions and directions'''
    pass

def evenValue(value):
    '''Return True if the value is even, False if odd'''
    return not value % 2

def allPositive(L):
    '''From the list return if all of the values are positive'''
    positive = True
    for item in L:
        if item < 0:
            return False
    return True

def allNegative(L):
    '''From the list return True if all the items are negative'''
    negative = True
    for item in L:
        if item >=0:
            return False
    return True

def minmaxValues(D, key, M):
    '''Given a list of values, return a new list that includes the minimum positive value and the maximum negative value, M is the matrix of values that we need since L does not contain these values, just the names of the segments.'''
    positive = []
    negative = []
    minval = []
    maxval = []
    for item in D[key]:
        if M[item][key] >= 0: positive.append(item)
        else: negative.append(item)
    if len(positive) > 0:
        positiveValues = [M[item][key] for item in positive]
        index = positiveValues.index(min(positiveValues))
        minval = [positive[index]]
    if len(negative) > 0:
        negativeValues = [M[item][key] for item in negative]
        index = negativeValues.index(max(negativeValues))
        maxval = [negative[index]]
    return minval + maxval

def angleToRad(angle):
    return angle * pi / 180

def radToAngle(rad):
    return rad * 180 / pi

def getXFromAngle(angle):
    x = (SCREENWIDTH/2.0)*((angle/FOVR) + 1)
    return clamp(x, 0)

def getAngleFromX(x):
    return FOVR*(((2*x)/SCREENWIDTH) - 1)

def removeEmptyKeys(D):
    '''Given a dictionary, remove any key that has an empty entry for its value'''
    newD = {}
    for key in D.keys():
        if type(D[key]) is list:
            if len(D[key]) != 0:
                newD[key] = D[key]
    return newD

def getAnglesFromXdict(D):
    '''Given a dictionary of x positions, get a new dictionary that converts the x positions to angle'''
    newD = {}
    for key in D.keys():
        values = []
        for item in D[key]:
            newitem = []
            for val in item:
                newitem.append(getAngleFromX(val))
            values.append(newitem)
        newD[key] = values
    return newD

def getPointingVectorsFromAngleDict(alpha, D):
    '''Given the players pointing angle alpha and a dictionary of other angles, get the vectors.'''
    alpha = angleToRad(alpha)
    newD = {}
    for key in D.keys():
        values = []
        for item in D[key]:
            newitem = []
            for theta in item:
                newitem.append(Vector2(cos(alpha+theta), sin(alpha+theta)))
                #newitem.append(getAngleFromX(val))
            values.append(newitem)
        newD[key] = values
    return newD

def getDistancesFromDirectionDict(p1, D):
    '''Given the center position of the player and an angle dictionary, get the actual distances'''
    newD = {}
    for key in D.keys():
        values = []
        for item in D[key]:
            newitem = []
            for vec in item:
                s, t = intersect(p1, key.p1, vec, key.direction)
                newitem.append(s)
            values.append(newitem)
        newD[key] = values
    return newD

def fisheyeCorrection(distanceDict, angleDict):
    '''Given a bunch of distances and their angles from players pointing direction, find the distance corrected versions'''
    print("FISHEYE")
    print("......BEFORE.......")
    for key in distanceDict.keys():
        print(distanceDict[key])
    print("")
    newDict = {}
    for key in distanceDict.keys():
        newDict[key] = []
        for i, item in enumerate(distanceDict[key]):
            d1 = item[0] * cos(angleDict[key][i][0])
            d2 = item[1] * cos(angleDict[key][i][1])
            newDict[key].append([d1, d2])
        #print(str(distanceDict[key]) + " : angle is " + str(angleDict[key]))
    print("......AFTER.......")
    for key in newDict.keys():
        print(newDict[key])
    print("")
    print("(0)..................(0)")
    return newDict

def getWallHeightPair(d):
    '''Given an distance value, return the wall height pair that defines the height of the wall at that distance.
    Returns the pair in top to bottom order.  reverse is true then return in bottom to top order.'''
    H = SCREENHEIGHT
    D = 20.0
    y1 = (H/2.0) * (1 - (D/d))
    y2 = (H/2.0) * (1 + (D/d))
    return [clamp(y1, 2), clamp(y2, 2)]
    
