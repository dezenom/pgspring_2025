#hyp - get displacement from the origin
#change - get vector from one point to another
#normalizeVector - return a vector of same direction but with a range of -1<=v<=1

hyp = lambda pos: (pos[0]**2+pos[1]**2)**0.5
change = lambda start,end: (end[0]-start[0],end[1]-start[1])
normalizeVector = lambda pos,hyp: (pos[0]/hyp,pos[1]/hyp)

#getOffset - get position in view space
def getOffset(pos,scroll,type = "TD"):
    x = pos[0]-scroll[0]
    y = pos[1]-scroll[1]
    return x,y

#moveTowards - move one value to another incremently over time
def moveTowards(start,speed,end):
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
