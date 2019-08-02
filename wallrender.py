import pygame
from math import pi
from constants import *
import utils
"""This class takes the BSP tree and the player in order to construct the 3D walls in the players viewport"""

class WallRender3D(object):
    def __init__(self, tree, player):
        self.tree = tree
        self.player = player
        self.xRangeList = [[-float("inf"),0],[SCREENWIDTH, float("inf")]]
        
    def DP_Segments(self, node, position):
        if node is not None:
            if node.leaf():
                self.buildWalls(node.data)
                #node.printData()
                node.visited = True
                if len(self.xRangeList) > 1:
                    self.DP_Segments(node.parent, position)
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
                    if len(self.xRangeList) > 1:
                        self.DP_Segments(node.left, position)
		else:
                    node.visited = True
                    self.DP_Segments(node.parent, position)

    
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
        if (abs(angle1) <= self.player.fovAngle_rads or
            abs(angle2) <= self.player.fovAngle_rads):
            segmentValid = True
        else: #both points outside fov, but does the segment cross the pointing direction?
            if segment.intersectVector(self.player.position, self.player.facingDirection):
                segmentValid = True
        if segmentValid:
            x1 = self.calculateXpositionFromAngle(angle1)
            x2 = self.calculateXpositionFromAngle(angle2)
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
        self.xRangeList.append(valueRange)
        print(self.xRangeList)
        
    def calculateXpositionFromAngle(self, angle):
        '''Find the x position on the screen given the angle found previously'''
        val = (SCREENWIDTH/2.0)*((angle/self.player.fovAngle_rads) + 1)
        return utils.clamp(val, 0)
    
    #def checkTree(self, node):                                                                                                                  
    #    if node is not None:                                                                                                                    
    #        print(node.visited)                                                                                                                 
    #        self.checkTree(node.left)                                                                                                           
    #        self.checkTree(node.right)
    
    def render(self, screen):
        self.xRangeList = [[-float("inf"),0],[SCREENWIDTH, float("inf")]]
        self.unvisitNodes(self.tree.root)
        #print(str(self.player.facingDirection) + " :: " + str(self.player.facingAngle))
        print("START")
        self.DP_Segments(self.tree.root, self.player.position)
        print("Finished")
        print("")
