# Cody
# 2021, August 25
# Quadtrees from Daniel Shiffman
# v0.01 - Point and rectangle
# v0.02 - quadtree with insert, subdivide, and make sure points added cause 
#         subdivide to activate
# v0.03 - quadtree.show9) with mousedraggoed add points



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
    

# Testing code for Point:
p1 = Point(random(width), random(height))
print(p1) 
strokeWeight(10)
point(p1.x, p1.y)

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def __repr__(self):
        return "I'm a Rectangle with coordinates of ({}, {}), a width of {}, and a height of {}.".format(self.x, self.y, self.w, self.h)
        
# Testing code for Rectangle
r1 = Rectangle(random(width), random(height), 5, 5)
print(r1)
