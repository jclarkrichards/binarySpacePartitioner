from copy import deepcopy

def clamp(value, precision):
    '''Clamp a value'''
    val = round(value, precision)
    if val == 0.0:
        val = abs(val)
    return val

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
        s = clamp(s, 5)
        t = clamp(t, 5)
    return s, t

def evenValue(value):
    '''Return True if the value is even, False if odd'''
    return not value % 2


