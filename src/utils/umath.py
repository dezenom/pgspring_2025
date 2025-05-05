import pygame

class Vec2:
    __slots__ = ("x", "y")

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def magnitude(self) -> float:
        return (self.x**2 + self.y**2)**0.5

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def perpendicular(self) -> "Vec2":
        return Vec2(-self.y, self.x)

    def normalize(self) -> "Vec2":
        if self.magnitude() == 0:
            return Vec2(0, 0)
        return Vec2(self.x / self.magnitude(), self.y / self.magnitude())

    def __add__(self, other) -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other) -> "Vec2":
        return Vec2(self.x * other, self.y * other)

    def __neg__(self) -> "Vec2":
        return Vec2(-self.x, -self.y)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __lt__(self, other) -> bool:
        return self.magnitude() < other.magnitude()

    def __le__(self, other) -> bool:
        return self.magnitude() <= other.magnitude()

    def __gt__(self, other) -> bool:
        return self.magnitude() > other.magnitude()

    def __ge__(self, other) -> bool:
        return self.magnitude() >= other.magnitude()

    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"

class minmax():
    __slots__ = ('min', 'max')
    def __init__(self,min,max):
        self.min = min
        self.max = max
    def __repr__(self) -> str:
        return f"minmax({self.min}, {self.max})"

#getOffset - get position in view space
def getOffset(pos,scroll,type = "TD"):
    x = pos[0]-scroll[0]
    y = pos[1]-scroll[1]
    return x,y

#moveTowards - move one value to another incremently over time
def increment(start,speed,end):
    current = start
    if end <0 and start>end:
        current -= speed
    elif end>0 and start<end:
        current +=speed

    if end == 0:
        if start > end:
            current-=speed
        elif start < end:
            current += speed


    if abs(start) > abs(end) and end !=0:
        current = end
    elif abs(start) > end and end ==0 and abs(start) < speed:
        current = end

    return current

def getNormals(polygon)->list:
    result = []
    for i,vertice in enumerate(polygon):
        if i == len(polygon)-1:
            edge = polygon[0] - vertice
            result.append(edge.perpendicular().normalize())
            break

        nextv = polygon[i+1]
        edge = nextv - vertice
        result.append(edge.perpendicular().normalize())
    return result;

def project(polygon, axis)->minmax:
    min = polygon[0].dot(axis)
    max = min
    for vertice in polygon:
        proj = vertice.dot(axis)
        min = proj if proj < min else min
        max = proj if proj > max else max
    return minmax(min,max)

def overlap(a:minmax ,b:minmax)->float:
    if a.max < b.min or b.max < a.min:
        return 0
    overlap_depth = min(a.max, b.max) - max(a.min, b.min)
    return overlap_depth if overlap_depth > 0 else 0


def SATCollision(A,B):
    minoverlap = float("inf")
    smallest_axis = Vec2()
    mtv = Vec2()

    Axis = getNormals(A)
    Bxis = getNormals(B)

    for axis in Axis:
        aproj = project(A,axis)
        bproj = project(B,axis)

        o = overlap(aproj,bproj)
        if not o:
            return (False,mtv)
        if o<minoverlap:
            minoverlap = o
            smallest_axis = axis
    for axis in Bxis:
        aproj = project(A,axis)
        bproj = project(B,axis)

        o = overlap(aproj,bproj)
        if not o:
            return (False,mtv)
        if o<minoverlap:
            minoverlap = o
            smallest_axis = axis

    centerA = Vec2()
    centerB = Vec2()
    for v in A:
        centerA = centerA + v
    for v in B:
        centerB = centerB + v
    centerA = centerA * (1/len(A))
    centerB = centerB * (1/len(B))

    direction = centerB - centerA
    if direction.dot(smallest_axis) < 0:
        smallest_axis = -smallest_axis

    mtv = smallest_axis*minoverlap
    return (True,mtv)

def getVerticesFromRect(rect:pygame.Rect)->list:
    return [Vec2(rect.left,rect.top),Vec2(rect.right,rect.top),
            Vec2(rect.right,rect.bottom),Vec2(rect.left,rect.bottom)]
