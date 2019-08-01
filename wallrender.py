import pygame
from math import pi
from constants import *
import utils
"""This class takes the BSP tree and the player in order to construct the 3D walls in the players viewport"""

class WallRender3D(object):
    def __init__(self, tree, player):
        self.tree = tree
        self.player = player
        self.xfill = [[-10000,0],[SCREENWIDTH, 10000]]
        
    def DP_Segments(self, node, position):
        if node is not None:
            if node.leaf():
                self.SP_XPosition(node.data)
                #node.printData()
                node.visited = True
                if len(self.xfill) > 1:
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
                    self.SP_XPosition(node.data)
                    if len(self.xfill) > 1:
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

    def SP_XPosition(self, data):
        '''Given a list of segments (or a single Segment) find where the segments p1 and p2 points would appear on the screens x position'''
        test = []
        if type(data) is list:
            for segment in data:
                self.segmentInFOV(segment)
                
        else:
            print(data.name + " : p1=" + str(data.p1) + " , p2="+str(data.p2))
            self.segmentInFOV(data)
        print("")

    def segmentInFOV(self, segment):
        '''Check if any of the segment is within the field of view of the player'''
        self.pointInFOV(segment.p1)
        self.pointInFOV(segment.p2)

        
        p1 = segment.p1 - self.player.position
        p2 = segment.p2 - self.player.position
        angle1 = self.player.facingDirection.angle(p1)
        angle2 = self.player.facingDirection.angle(p2)
        cross1 = self.player.facingDirection.cross(p1)
        cross2 = self.player.facingDirection.cross(p2)
        if (angle1 <= self.player.fovAngle_rads or
            angle2 <= self.player.fovAngle_rads):
            if cross1 < 0: angle1 *= -1
            if cross2 < 0: angle2 *= -1
            x1 = self.calculateXpositionFromAngle(angle1)
            x2 = self.calculateXpositionFromAngle(angle2)
            #print(segment.name + " : p1=" + str(segment.p1) + " , p2="+str(segment.p2))
            print(segment.name + " :: " + str(x1) + "    " + str(x2))
            self.updateXFill(x1, x2)
        else: #both points outside fov, but does the segment cross the pointing direction?
            if segment.intersectVector(self.player.position, self.player.facingDirection):
                if cross1 < 0: angle1 *= -1
                if cross2 < 0: angle2 *= -1
                x1 = self.calculateXpositionFromAngle(angle1)
                x2 = self.calculateXpositionFromAngle(angle2)
                #print(segment.name + " : p1=" + str(segment.p1) + " , p2="+str(segment.p2))
                print(segment.name + " :: " + str(x1) + "   " + str(x2))
                self.updateXFill(x1, x2)
            #else:
            #    print("NO")

    def pointInFOV(self, point):
        '''Check if a point is within the field of view of the player'''
        pass
    
    def updateXFill(self, x1, x2):
        '''Use these x values to fill in the x fill list'''
        pass
    
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
        self.xfill = [[-10000,0],[SCREENWIDTH, 10000]]
        self.unvisitNodes(self.tree.root)
        #print(str(self.player.facingDirection) + " :: " + str(self.player.facingAngle))
        print("START")
        self.DP_Segments(self.tree.root, self.player.position)
        print("Finished")
        print("")
