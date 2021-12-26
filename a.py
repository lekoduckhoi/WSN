import math
rs = 1
def get_intersections(x0, y0, x1, y1):
    # circle 1: (x0, y0)
    # circle 2: (x1, y1)
    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    # non intersecting
    if d > 2:
        return None
    # coincident circles
    if d == 0:
        return None
    else:
        a=(rs**2-rs**2+d**2)/(2*d)
        h=math.sqrt(rs**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        
        return (x3, y3, x4, y4)
print(get_intersections(1,1,1,2))