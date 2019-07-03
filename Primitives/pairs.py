from copy import deepcopy
"""A Pair is a list of only 2 objects.  The order of the objects do not matter.  For example:  [a,b] == [b,a].  """

class Pair(object):
    def __init__(self, objects=[]):
        if len(objects) == 2:
            self.objects = objects
        else:
            self.objects = []

    def __str__(self):
        return str(self.objects)

    def __eq__(self, other):
        if len(self.objects) == len(other.objects) == 2:
            reversed = deepcopy(self.objects)
            reversed.reverse()
            test = [self.objects, reversed]
            if other.objects in test:
                return True
        return False

    def hash(self):
        return id(self)

    def addObject(self, obj):
        if len(self.objects) < 2:
            self.objects.append(obj)

    def asTuple(self):
        '''Return this pair as a tuple'''
        return tuple(self.objects)

    def __hash__(self):
        return super().__hash__()
    
