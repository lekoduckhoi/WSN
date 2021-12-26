import random
import math 
import matplotlib.pyplot as plt

rs = 1 #sensing radius
targetsX = [] #list of targets in X coordinate
targetsY = [] #list of targets in X coordinate
targets = [] #list of targets 
tar = [] #list of targets whose disks do not intersect, denote T' in paper
ists = [] #list of intersections between disks
F = [] #sensors set
for i in range(0,18): #randomly generate 12 targets
    targetsX.append(random.randint(1,9))
    targetsY.append(random.randint(1,9))
    targets.append([targetsX[i], targetsY[i]])

def get_intersections(x0, y0, x1, y1): # get 2 intersections of disks
    
    d=math.dist([x0, y0], [x1, y1])
    a=(rs**2-rs**2+d**2)/(2*d)
    h=math.sqrt(rs**2-a**2)
    x2=x0+a*(x1-x0)/d   
    y2=y0+a*(y1-y0)/d   
    x3=x2+h*(y1-y0)/d     
    y3=y2-h*(x1-x0)/d 
    x4=x2-h*(y1-y0)/d
    y4=y2+h*(x1-x0)/d
    
    return ([x3, y3], [x4, y4])
hasIntersected = [0]*len(targets)

for i in range(0,17): 
    for j in range(i+1,18):
        if math.dist(targets[i], targets[j]) == 2:
            ists.append([(targetsX[i] + targetsX[j])/2, (targetsY[i] + targetsY[j])/2])
            hasIntersected[i] = 1
            hasIntersected[j] = 1
        if 0 < math.dist(targets[i], targets[j]) < 2:
            ists.append(get_intersections(targetsX[i], targetsY[i], targetsX[j], targetsY[j])[0])
            ists.append(get_intersections(targetsX[i], targetsY[i], targetsX[j], targetsY[j])[1])
            hasIntersected[i] = 1
            hasIntersected[j] = 1
print(hasIntersected)
istsX = []
istsY = []
for i in range(len(ists)):
    istsX.append(ists[i][0])
    istsY.append(ists[i][1])
F = ists.copy()
Fx = []
Fy = []
for i in range(len(targets)):
    if hasIntersected[i] == 0:
        F.append([targetsX[i], targetsY[i]])
for i in range(len(F)):
    Fx.append(F[i][0])
    Fy.append(F[i][1])





fig1, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_box_aspect(1)
plt.plot(targetsX, targetsY, '*', color = 'red', markersize=12)
plt.plot(Fx, Fy, 'o', color = 'blue', markersize=4)
for i in range(0,18):
    ax.add_patch(plt.Circle((targetsX[i], targetsY[i]), 1, color='blue', alpha = 0.2))
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()

