from wallculler import WallCull
wallcull = WallCull()
#valueList = [[-380.0, 222.0], [353.0, 470.0], [351.0, 353.0], [222.0, 606.0], [351.0, 450.0], [450.0, 670.0]]
#valueList = [[443.0, 943.0], [174.0, 313.0], [218.0, 313.0], [218.0, 326.0], [326.0, 443.0], [-268.0, 174.0]]
#valueList = [[-324.0, 236.0], [236.0, 702.0], [419.0, 546.0], [419.0, 422.0], [422.0, 527.0], [527.0, 761.0]]
valueList = [[-320.0, 80.0], [50.0, 700.0], [200.0, 320.0], [350.0,400.0]]

print("")
print("+++++++START-------------")
print(wallcull.xrangeList)
for i, item in enumerate(valueList):
    if wallcull.canstop():
        break
    else:
        wallcull.update(i, item)

print(wallcull.xrangeList)
print(wallcull.segmentDict)
print("-------END+++++++++++++++")
print("")
