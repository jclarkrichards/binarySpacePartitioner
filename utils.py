from copy import deepcopy
from Primitives.vectors import Vector2

def clamp(value, precision):
    '''Clamp a value'''
    #val = round(value, precision)
    val = round(value, precision)
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


