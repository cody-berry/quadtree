# Cody
# 2021, August 25
# Quadtrees from Daniel Shiffman
# v0.01  - Point and rectangle
# v0.02  - quadtree with insert, subdivide, and make sure points added cause 
#         subdivide to activate
# v0.021 - count
# v0.03  - quadtree.show() with mousedragged add points



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
    

# Testing code for Point:
# p1 = Point(random(width), random(height))
# print(p1) 
# strokeWeight(10)
# point(p1.x, p1.y)

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def __repr__(self):
        return "I'm a Rectangle with coordinates of ({}, {}), a width of {}, and a height of {}.".format(self.x, self.y, self.w, self.h)
        
# Testing code for Rectangle
# r1 = Rectangle(random(width), random(height), random(1, 10), random(1, 10))
# print(r1)
# rect(r1.x, r1.y, r1.w, r1.h)


class Quadtree:
    def __init__(self, boundary, point_cap): # boundary is a Rectangle
        self.boundary = boundary
        self.point_cap = point_cap
        self.points = []
        self.divided = False
        
        
    def contains(self, p):
        b = self.boundary
        return p.x <= b.x + b.w and p.x >= b.x and p.y <= b.y + b.h and p.y >= b.y
    
    
    def subdivide(self):
        b = self.boundary
        nw = Rectangle(b.x, b.y, b.w/2.0, b.h/2.0)
        self.northwest = Quadtree(nw, self.point_cap)
        ne = Rectangle(b.x + b.w/2.0, b.y, b.w/2.0, b.h/2.0)
        self.northeast = Quadtree(ne, self.point_cap)
        sw = Rectangle(b.x, b.y + b.h/2.0, b.w/2.0, b.h/2.0)
        self.southwest = Quadtree(sw, self.point_cap)
        se = Rectangle(b.x + b.w/2.0, b.y + b.h/2.0, b.w/2.0, b.h/2.0)
        self.southeast = Quadtree(se, self.point_cap)
        self.divided = True
        
    
    def insert(self, p):
        # If you look at the code before "Spoilers from Daniel's code!", we only want to insert
        # so that only 1 of them gains it.
        if not self.contains(p):
            return False
        
        
        # Success! We can add a point as long as the quadtree rectangle boundary is not full.
        if len(self.points) < self.point_cap:
            self.points.append(p)
            return True
        
        
        # Oh no! Our quadtree boundary rectangle is full. We need to split up and give the point
        # to whichever point owns it. If it is somwhere near the edge or corner, the priority 
        # queue is from most important to least important: [nw, ne, sw, se], where nw stands for
        # northwest, ne stands for northeast, sw stands for southwest, and se stands for southeast.    
        else:
            if not self.divided:
                self.subdivide()
            # Spoilers from Daniel's code!
            if self.northwest.insert(p):
                return True
            if self.northeast.insert(p):
                return True
            if self.southwest.insert(p):
                return True
            if self.southeast.insert(p):
                return True
            
            
    def show(self):
        noFill()
        stroke(0, 0, 0, 100)
        strokeWeight(1)
        b = self.boundary
        rect(b.x, b.y, b.w, b.h)
        if self.divided:
            self.northwest.show()
            self.northeast.show()
            self.southwest.show()
            self.southeast.show()
    
                    
    # def __repr__(self):
    #     if self.divided:
    #         return "Self contents: I have {} points. Northwest contents: {} Northeast contents: {} Southwest contents: {} Southeast contents: {}".format(len(self.points), self.northwest, self.northeast, self.southwest, self.southeast)
    #     else:
    #         return "I have {} points.".format(len(self.points))
            
            
def setup(): 
    global points, quadtree
    colorMode(HSB, 360, 100, 100, 100)
    size(600, 600)         
    points = []
    quadtree = Quadtree(Rectangle(0, 0, width, height), 4)
    for i in range(10000):
        p = Point(random(width), random(height))
        points.append(p)
        quadtree.insert(p)
    
def draw():
    background(179, 75, 30)
    global points, quadtree
    for p in points:
        stroke(0, 0, 0, 100)
        strokeWeight(2)
        point(p.x, p.y)
        
    quadtree.show()
        
    
            
            
            
            
            
            
            
    
