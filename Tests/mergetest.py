from copy import deepcopy
#python2 uses float("inf")
#python3 uses math.inf

def overlap(other, item):
    if (other[0] <= item[0] < other[1] or
        other[0] < item[1] <= other[1] or
        item[0] <= other[0] < item[1] or
        item[0] < other[1] <= item[1]):
        return True
    return False

def difference(other, items):
    '''Return the portions of item that do not overlap other'''
    temp = []
    for item in items:
        if overlap(other, item):
            #temp = [] #situation 3
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

def cullRanges(values, items):
    '''We already know that item overlaps all of the values.  Split item up into ranges that do not overlap the values'''
    print("Overlapping " + str(len(values)) + " ranges.")
    #temp = []
    for other in values:
        #temp.append(other)
        items = difference(other, items)
        #if overlaps is not None:
            #print(overlaps)
            #for i in overlaps:
            #    temp.append(i)
    return values + items

def orderValues(values):
    '''Order the values from lowest ranges to highest ranges'''
    test = [k[0] for k in values]
    test.sort()
    temp = []
    for t in test:
        for val in values:
            if t == val[0]:
                temp.append(val)
    return temp
    
    
def merge(values):
    '''We merge ranges together if they share the same points'''
    #values = orderValues(values)
    #values.sort()
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
        print(values)


def run(results):
    values = [[-float("inf"), 0.0], [576.0, float("inf")]] #initial range, values outside these ranges get squashed to this range
    #valueList = [[-380.0, 222.0], [353.0, 470.0], [351.0, 353.0], [222.0, 606.0], [351.0, 450.0], [450.0, 670.0]]
    #valueList = [[443.0, 943.0], [174.0, 313.0], [218.0, 313.0], [218.0, 326.0], [326.0, 443.0], [-268.0, 174.0]]
    #valueList = [[-324.0, 236.0], [236.0, 702.0], [419.0, 546.0], [419.0, 422.0], [422.0, 527.0], [527.0, 761.0]]
    valueList = [[-320.0, 80.0], [200.0, 320.0], [350.0,400.0], [50.0, 700.0]]
    for i, item in enumerate(valueList):
        tempvalues = deepcopy(values)
        valuesCheck = []
        valuesNocheck = []
        print(str(item) + " -----> " + str(tempvalues))
        for value in tempvalues:
            if overlap(value, item):
                valuesCheck.append(value)
            else:
                valuesNocheck.append(value)
        if len(valuesCheck) == 0: #item does not overlap any of the other ranges
            tempvalues.append(item)
        else:
            tempvalues = cullRanges(valuesCheck, [item])
            tempvalues += valuesNocheck
        print("Before merge....... " + str(values))
        print(tempvalues)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^")
        results[i] = []
        for value in tempvalues:
            if value not in values:
                results[i].append(value)
        
        merge(tempvalues)
        values = deepcopy(tempvalues)
        
    print("")
    print("-----------------------------------------")
    print(values)
    return results
#--------------------------------
values = [[-float("inf"), 0.0], [576.0, float("inf")]] #initial range, values outside these ranges get squashed to this range                                                     
#valueList = [[-380.0, 222.0], [353.0, 470.0], [351.0, 353.0], [222.0, 606.0], [351.0, 450.0], [450.0, 670.0]]                                                                    
#valueList = [[443.0, 943.0], [174.0, 313.0], [218.0, 313.0], [218.0, 326.0], [326.0, 443.0], [-268.0, 174.0]]                                                                    
#valueList = [[-324.0, 236.0], [236.0, 702.0], [419.0, 546.0], [419.0, 422.0], [422.0, 527.0], [527.0, 761.0]]
valueList = [[-320.0, 80.0], [200.0, 320.0], [350.0,400.0], [50.0, 700.0]]

print("")
print("+++++++START-------------")
results = run({})
print(results)
#values = [[-float("inf"), 0.0], [200.0, 400.0], [576.0, float("inf")], [0.0, 200.0], [400.0, 576.0]]
#values = [[5, 9], [2, 3], [12, 15], [0, 2], [3, 5]]
#merge(values)
print("-------END+++++++++++++++")
print("")


"""
for newvalue in valueList:
    newvalues = []
    print("")
    print(".................................")
    print("Values = " + str(values))
    print("new value = " + str(newvalue))
    values.append(newvalue)
    if len(values) > 1:
        print(values)
        while len(values) > 0:
            if len(values) == 1:
                junk = values.pop(0)
                #print("only 1 value: " + str(junk))
                newvalues.append(junk)
            else:
                #print("")
                #print("--------------LOOP OTHER VALUES--------------")
                #print(values)
                #print("length of values = " + str(len(values)))
                item = values.pop(0)
                found = False
                for other in values:
                    #print("ITEM = " + str(item) + " :: " + " OTHER = " + str(other))
                    if other[0] <= item[0] <= other[1]:
                        if item[1] > other[1]:
                            values.append([other[0], item[1]])
                        else:
                            values.append([other[0], other[1]])
                        values.remove(other)
                        #print("removed " + str(other))
                        found = True
                    elif other[0] <= item[1] <= other[1]:
                        if item[0] <= other[0]:
                            values.append([item[0], other[1]])
                        else:
                            values.append([other[0], other[1]])
                        values.remove(other)
                        #print("removed " + str(other))
                        found = True
                    #print("Values = " + str(values))

                if not found:
                    #print("item " + str(item) + " not matching")
                    newvalues.append(item)

            #print("END OF THE LINE " + str(values))        
    print("values now = " + str(newvalues))
    values = deepcopy(newvalues)
    if len(values) == 1:
        break
    
print("++++++++++++++++++++++++++++++++++++")
#print(newvalues)
print(values)
"""
