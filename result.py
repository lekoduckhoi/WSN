import random
import math 
import matplotlib.pyplot as plt
import time
def runPha1(_rs, n0targets):
    start = time.time()
    rs = _rs #sensing radius
    targetsX = [] #list of targets in X coordinate
    targetsY = [] #list of targets in X coordinate
    targets = [] #list of targets 
    tar = [] #list of targets whose disks do not intersect, denote T' in paper
    ists = [] #list of intersections between disks
    F = [] #sensors set
    for i in range(0,n0targets): #randomly generate 12 targets
        targetsX.append(random.uniform(1,9))
        targetsY.append(random.uniform(1,9))
        targets.append([targetsX[i], targetsY[i]])

    def get_intersections(x0, y0, x1, y1): # get 2 intersections of disks
        d=math.dist([x0, y0], [x1, y1])
        a= d/2
        h=math.sqrt(rs**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 
        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d

        return ([x3, y3], [x4, y4])
    hasIntersected = [0]*len(targets)

    for i in range(len(targets)): 
        for j in range(i+1,len(targets)):
            if math.dist(targets[i], targets[j]) == 2*rs:
                ists.append([(targetsX[i] + targetsX[j])/2, (targetsY[i] + targetsY[j])/2])
                hasIntersected[i] = 1
                hasIntersected[j] = 1
            if 0 < math.dist(targets[i], targets[j]) < 2*rs:
                ists.append(get_intersections(targetsX[i], targetsY[i], targetsX[j], targetsY[j])[0])
                ists.append(get_intersections(targetsX[i], targetsY[i], targetsX[j], targetsY[j])[1])
                hasIntersected[i] = 1
                hasIntersected[j] = 1
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

    #finding SSCAT from F
    matrix = []
    SSCAT = []
    for i in range(len(F)):
        listCovered = []
        for j in range(len(targets)):
            if math.dist(F[i], targets[j]) <= rs +0.0001:
                listCovered.append(1)
            else:
                listCovered.append(0)
        matrix.append(listCovered)
    def findMaxLfIndex():
        Lflist = [0]*len(F)
        for i in range(len(F)):
            Lflist[i] = sum(matrix[i])
        return(Lflist.index(max(Lflist)))

    while sum(sum(matrix,[])) != 0:
        maxLfIndex = findMaxLfIndex()
        SSCAT.append(F[maxLfIndex])
        for i in range(len(targets)):
            if math.dist(F[maxLfIndex], targets[i]) <= rs +0.0001:
                for j in range(len(F)):
                    matrix[j][i] = 0
    end = time.time()

# total time taken
    print(f"Runtime of the program is {end - start}")
    print(f"Total Sensing Nodes is {len(SSCAT)}")
    return SSCAT

for i in range(20):
    runPha1(1,17)