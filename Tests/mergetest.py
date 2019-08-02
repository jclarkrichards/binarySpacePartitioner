from copy import deepcopy
#python2 uses float("inf")
#python3 uses math.inf
values = [[-float("inf"), 0.0], [576.0, float("inf")]] #initial range, values outside these ranges get squashed to this range
#valueList = [[-380.0, 222.0], [222.0, 606.0], [353.0, 470.0]]
valueList = [[-380.0, 222.0], [222.0, 606.0], [353.0, 470.0], [351.0, 353.0], [351.0, 450.0], [450.0, 670.0]]

#newvalues = []
for newvalue in valueList:
    newvalues = []
    #print("")
    #print(".................................")
    #print("Values = " + str(values))
    #print("new value = " + str(newvalue))
    values.append(newvalue)
    if len(values) > 1:
        #print(values)
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
                    print("item " + str(item) + " not matching")
                    newvalues.append(item)

            #print("END OF THE LINE " + str(values))        
    #print("values now = " + str(newvalues))
    values = deepcopy(newvalues)
    if len(values) == 1:
        break
    
print("++++++++++++++++++++++++++++++++++++")
print(newvalues)
print(values)
