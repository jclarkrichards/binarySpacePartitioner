from copy import deepcopy
from constants import *

class WallCull(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.xrangeList = [[-float("inf"),0],[SCREENWIDTH, float("inf")]]
        self.segmentDict = {}

    def canstop(self):
        if len(self.xrangeList) == 1:
            return True
        return False

    def update(self, segment, item):
        tempvalues = deepcopy(self.xrangeList)
        valuesCheck = []
        valuesNocheck = []
        print(str(item) + " -----> " + str(tempvalues))
        for value in tempvalues:
            if self.overlap(value, item):
                valuesCheck.append(value)
            else:
                valuesNocheck.append(value)
        if len(valuesCheck) == 0: #item does not overlap any of the other ranges                                                                                                      
            tempvalues.append(item)
        else:
            tempvalues = self.cullRanges(valuesCheck, [item])
            tempvalues += valuesNocheck
        print("Before merge....... " + str(self.xrangeList))
        print(tempvalues)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.segmentDict[segment] = []
        for value in tempvalues:
            if value not in self.xrangeList:
                self.segmentDict[segment].append(value)

        self.merge(tempvalues)
        self.xrangeList = deepcopy(tempvalues)

    def overlap(self, other, item):
        if (other[0] <= item[0] < other[1] or
            other[0] < item[1] <= other[1] or
            item[0] <= other[0] < item[1] or
            item[0] < other[1] <= item[1]):
            return True
        return False

    def difference(self, other, items):
        temp = []
        for item in items:
            if self.overlap(other, item):
                if other[0] <= item[0] <= other[1]:
                    if other[1] < item[1]: #situation 1                                                                                                                                   
                        temp.append([other[1], item[1]])
                elif other[0] <= item[1] <= other[1]:
                    if item[0] < other[0]: #situation 2                                                                                                                                   
                        temp.append([item[0], other[0]])
                elif item[0] < other[0] and other[1] < item[1]: #situation 4                                                                                                              
                    temp.append([item[0], other[0]])
                    temp.append([other[1], item[1]])
            else:
                temp.append(item)
        return temp

    def cullRanges(self, values, items):
        print("Overlapping " + str(len(values)) + " ranges.")
        for other in values:
            items = self.difference(other, items)
        return values + items

    def merge(self, values):
        allmerged = False
        while not allmerged:
            values.sort()
            merged = False
            for i in range(len(values)-1):
                print(str(values[i]) + " " + str(values[i+1]))
                if values[i][1] == values[i+1][0]:
                    values.append([values[i][0], values[i+1][1]])
                    values.pop(i)
                    values.pop(i)
                    merged = True
                    break
            if not merged:
                allmerged = True



    
