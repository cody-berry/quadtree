# Cody
# 2021, August 25
# Quadtrees from Daniel Shiffman
# v0.01  - Point and rectangle
# v0.02  - quadtree with contains, subdivide
# v0.03  - quadtree with insert
# v0.031 - count
# v0.04  - quadtree.show() with m12
# v0.05  - Query

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
    
    
    def contains(self, p):
        b = self
        return p.x <= b.x + b.w and p.x >= b.x and p.y <= b.y + b.h and p.y >= b.y
    
    
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
        
    
    def intersects(self, r):
        b = self.boundary
        return not (b.x > r.x + r.w or 
                   r.x > b.x + b.w or 
                   r.y > b.y + b.h or
                   b.y > r.y + r.h)
    
    
    def subdivide(self):
        b = self.boundary
        # northwest
        nw = Rectangle(b.x, b.y, b.w/2.0, b.h/2.0)
        self.northwest = Quadtree(nw, self.point_cap)
        # northeast
        ne = Rectangle(b.x + b.w/2.0, b.y, b.w/2.0, b.h/2.0)
        self.northeast = Quadtree(ne, self.point_cap)
        # southwest
        sw = Rectangle(b.x, b.y + b.h/2.0, b.w/2.0, b.h/2.0)
        self.southwest = Quadtree(sw, self.point_cap)
        # southeast
        se = Rectangle(b.x + b.w/2.0, b.y + b.h/2.0, b.w/2.0, b.h/2.0)
        self.southeast = Quadtree(se, self.point_cap)
        # We've divided! Now we can say that this quadtree has divided, and say that the others
        # have not (set in the constructor).
        self.divided = True
        
    
    def insert(self, p):
        # If you look at the code after "Spoilers from Daniel's code!", we only want to insert
        # so that only 1 of them gains it.
        if not self.boundary.contains(p):
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
        stroke(0, 0, 100, 100)
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
    
    
    # The total number of points inserted is what this function gives.
    def count(self):
        total = len(self.points)
        if self.divided:
            total += self.northwest.count()
            total += self.northeast.count()
            total += self.southwest.count()
            total += self.southeast.count()
            
        return total
    
    
    def query(self, r):
        found = []
        if not self.intersects(r):
            return found
        
        for p in self.points:
            if r.contains(p):
                found.append(p)
                
                
        if self.divided:
            found += self.northwest.query(r)
            found += self.northeast.query(r)
            found += self.southwest.query(r)
            found += self.southeast.query(r)
            
            
        return found
            
            
def setup(): 
    global points, quadtree
    colorMode(HSB, 360, 100, 100, 100)
    size(600, 600)         
    points = []
    quadtree = Quadtree(Rectangle(0, 0, width, height), 4)
    
def draw():
    background(210, 80, 32)
    global points, quadtree
    for p in points:
        stroke(0, 0, 50, 100)
        strokeWeight(5)
        point(p.x, p.y)
        
    quadtree.show()
    
    bound_width = 108
    bound_height = 76
    
    # Test query!
    bound = Rectangle(mouseX - bound_width/2, mouseY - bound_height/2, bound_width, bound_height)
    stroke(210, 70, 91)
    noFill()
    rect(bound.x, bound.y, bound.w, bound.h)
    points_found = quadtree.query(bound)
    for p in points_found:
        strokeWeight(3)
        point(p.x, p.y)
    
    # 0 movers, 1 mover, and 2 movers. We need a suffix telling us if we need to have an s.
    suffix = ''
    if len(points_found) != 1:
        suffix = 's'
    text(str(quadtree.count()) + " of " + str(len(points)), 30, 30)
    text(str(len(points_found)) + " point{} found in blue box".format(suffix), 30, 50)
    
    
def mouseDragged():
    global points
    if mouseX < width and mouseX > 0 and mouseY < height and mouseY > 0:
        if frameCount % 6 == 0:
            p = Point(mouseX, mouseY)
            points.append(p)
            quadtree.insert(p)
    
def mouseWheel(e):
    p = Point(mouseX, mouseY)
    points.append(p)
    quadtree.insert(p)
    
# def mousePressed():
#     global points
#     for p in points:
#         quadtree.insert(p)
        
#     points += points
        
    
            
            
            
            
            
            
            
    
