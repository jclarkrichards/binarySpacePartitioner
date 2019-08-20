import pygame
from math import pi
from constants import *
import utils
from copy import deepcopy
from wallculler import WallCull
"""This class takes the BSP tree and the player in order to construct the 3D walls in the players viewport"""

class WallRender3D(object):
    def __init__(self, tree, player):
        self.tree = tree
        self.player = player
        self.wallcull = WallCull()
        self.distancesTest = {}
        
    def DP_Segments(self, node, position):
        if node is not None:
            if node.leaf():
                self.buildWalls(node.data)
                #node.printData()
                node.visited = True
                self.continueOrStop(node.parent, position)
            else:
                if node.rightOpen():
                    if node.leftOpen():
			if node.data.side(position) == "right":
                            self.DP_Segments(node.right, position)
			else:
                            self.DP_Segments(node.left, position)
                    else:
                        self.DP_Segments(node.right, position)
		elif node.leftOpen():
                    #node.printData()
                    self.buildWalls(node.data)
                    self.continueOrStop(node.left, position)
                    #if not self.wallcull.canstop():
                    #    self.DP_Segments(node.left, position)
                    #else:
                    #    print("STOP........ " + str(self.wallcull.segmentDict))
		else:
                    node.visited = True
                    self.DP_Segments(node.parent, position)


    def continueOrStop(self, node, position):
        if not self.wallcull.canstop():
            self.DP_Segments(node, position)
        else:
            print("STOP.............. " + str(len(self.wallcull.segmentDict)))
            print(self.wallcull.xrangeList)
            print("=============X Positions for each Segment====================")
            xDict = utils.removeEmptyKeys(self.wallcull.segmentDict)
            angleDict = utils.getAnglesFromXdict(xDict)
            dirDict = utils.getPointingVectorsFromAngleDict(self.player.facingAngle, angleDict)
            distanceDict = utils.getDistancesFromDirectionDict(self.player.position, dirDict)

            #just for testing
            self.distancesTest = {}
            for key in dirDict.keys():
                values = []
                for i, item in enumerate(dirDict[key]):
                    newitem = []
                    for j, vec in enumerate(item):
                        newitem.append(vec * distanceDict[key][i][j])
                    values.append(newitem)
                self.distancesTest[key] = values

            
                
            
            
            print(xDict)
            print(angleDict)
            print(dirDict)
            print("..................................")
            print(self.player.facingAngle)
            for key in xDict.keys():
                print(str(key.name) + " : " + str(xDict[key]))
                for item in dirDict[key]:
                    print(str(item[0]) + " , " + str(item[1]))
                print("DISTANCES")
                for item in distanceDict[key]:
                    print(item)
                print("")
                
            print("")
            print("")
            
    
        
    def unvisitNodes(self, node):
        '''Unvisit all of the nodes in the tree'''
        if node is not None:
            node.visited = False
            self.unvisitNodes(node.left)
            self.unvisitNodes(node.right)

    def buildWalls(self, data):
        '''Given a list of segments (or a single Segment) find where the segments p1 and p2 points would appear on the screens x position'''
        test = []
        if type(data) is list:
            for segment in data:
                self.transformSegment(segment)
                
        else:
            print(data.name + " : p1=" + str(data.p1) + " , p2="+str(data.p2))
            self.transformSegment(data)
        print("")

    def transformSegment(self, segment):
        '''Check if any of the segment is within the field of view of the player'''
        angle1 = self.getAngleFromFD(segment.p1)
        angle2 = self.getAngleFromFD(segment.p2)
        segmentValid = False
        if (abs(angle1) <= FOVR or abs(angle2) <= FOVR):
            segmentValid = True
        else: #both points outside fov, but does the segment cross the pointing direction?
            if segment.intersectVector(self.player.position, self.player.facingDirection):
                segmentValid = True
        if segmentValid:
            x1 = utils.getXFromAngle(angle1)
            x2 = utils.getXFromAngle(angle2)
            if x1 < x2: self.updateXFill(segment, [x1, x2])
            else: self.updateXFill(segment, [x2, x1])
        
    def getAngleFromFD(self, point):
        '''Check if a point is within the field of view of the player'''
        p = point - self.player.position
        angle = self.player.facingDirection.angle(p)
        cross = self.player.facingDirection.cross(p)
        if cross < 0: angle *= -1
        return angle

    def updateXFill(self, segment, valueRange):
        '''Use these x values to fill in the x fill list'''
        print(segment.name + "---------------->" + str(valueRange))
        print(self.wallcull.xrangeList)
        print(str(valueRange[0]) + " ===> " + str(utils.radToAngle(utils.getAngleFromX(valueRange[0]))))
        print(str(valueRange[1]) + " ===> " + str(utils.radToAngle(utils.getAngleFromX(valueRange[1]))))
        self.wallcull.update(segment, valueRange)
        
    def render(self, screen):
        '''Draw the 3D walls here'''
        self.wallcull.reset()
        self.unvisitNodes(self.tree.root)
        print("START")
        self.DP_Segments(self.tree.root, self.player.position)
        print("Finished")
        print("")

        #test to see the lines being drawn...
        if len(self.distancesTest) > 0:
            for key in self.distancesTest.keys():
                for item in self.distancesTest[key]:
                    for vec in item:
                        x1, y1 = self.player.position.toTuple()
                        x2, y2 = vec.toTuple()
                        pygame.draw.line(screen, (255,255,255), [x1, y1], [x1+x2, y1+y2], 2)
