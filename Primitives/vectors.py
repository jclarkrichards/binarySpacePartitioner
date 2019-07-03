import math

class Vector2(object):
    def __init__(self, *values):
        self.x, self.y = self.determineType(values)
        
    def __str__(self):
        return "<" + str(self.x) + ", " + str(self.y)+ ">"
    
    def toTuple(self):
        '''Returns a tuple representation of this vector'''
        return (self.x, self.y)

    def magnitude(self):
        '''Returns length of this vector'''
        return math.sqrt(self.x**2 + self.y**2)

    def magnitudeSquared(self):
        return self.x**2 + self.y**2

    def __add__(self, rhs):
        return Vector2(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return Vector2(self.x - rhs.x, self.y - rhs.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / float(scalar), self.y / float(scalar))
    
    def __div__(self, scalar):
        return Vector2(self.x / float(scalar), self.y / float(scalar))

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __hash__(self):
        '''Needed for Python3'''
        return id(self)

    def dot(self, other):
        '''Dot product between 2 vectors'''
        return self.x*other.x + self.y*other.y
    
    def cross(self, other):
        '''Cross product between 2 vectors'''
        return self.x*other.y - self.y*other.x

    def normalize(self):
        '''Returns unit vector of this vector'''
        mag = self.magnitude()
        if mag != 0:
            return Vector2(self.x/mag, self.y/mag)
        else:
            return Vector2(self.x, self.y)

    def angle(self, other):
        '''Return the angle between 2 vectors in radians.  Always between 0 and 180 degrees, or 0 and pi in radians.  angle needs to be clamped between -1 and 1 since that's the range acos can handle.  acos will not work if value is 1.000006 for example.'''
        magnitude1 = self.magnitude()
        magnitude2 = other.magnitude()
        if magnitude1 != 0 and magnitude2 != 0:
            testvalue = self.dot(other) / (magnitude1 * magnitude2)
            if testvalue > 0:
                value = min(testvalue, 1)
            else:
                value = max(testvalue, -1)
            return math.acos(value)
        return 0 #only reached if one of the magnitudes is 0
    
    def copy(self):
        return Vector2(self.x, self.y)

    def determineType(self, values):
        '''x and y need to be floats.  But the inputs can be lists, tuples, Vector2s, ints, or floats.'''
        x, y = (0.0, 0.0)
        if len(values) == 1:
            if type(values[0]) is Vector2:
                temp = values[0].copy()
                x, y = temp.toTuple()
            elif type(values[0]) is tuple or type(values[0]) is list:
                if len(values[0]) == 2:
                    if type(values[0][0]) is int or type(values[0][0]) is float:
                        x = float(values[0][0])
                    if type(values[0][1]) is int or type(values[0][1]) is float:
                        y = float(values[0][1])
                
        elif len(values) == 2:
            if type(values[0]) is int or type(values[0]) is float:
                x = float(values[0])
            if type(values[1]) is int or type(values[1]) is float:
                y = float(values[1])
        return x, y
        
