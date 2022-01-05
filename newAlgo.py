import random
import math 
import matplotlib.pyplot as plt
import time
def runNewAlgo(_rs, n0targets):
    start = time.time()
    rs = _rs #sensing radius
    rc = 2*rs
    targetsX = [] #list of targets in X coordinate
    targetsY = [] #list of targets in X coordinate
    targets = [] #list of targets 
    tar = [] #list of targets whose disks do not intersect, denote T' in paper
    for i in range(0,n0targets): #randomly generate 12 targets
        targetsX.append(random.uniform(1,9))
        targetsY.append(random.uniform(1,9))
        targets.append([targetsX[i], targetsY[i]])
    
    V1 = targets.copy()
    V1.append([5,5])
    G = GraphWeight(len(V1))
    for i in range(len(V1)-1):
        for j in range(i+1,len(V1)):
            G.add_edge(i, j, math.dist(V1[i], V1[j]))
    MST = G.kruskal_algo()
    relayNodes = []
    def fillRelayNodes(i,j): #add relay nodes to line V1[i] V1[j]
        #vector V1[i] to V[j] = (a,b)
        if math.dist(V1[i], V1[j]) < rs*2:
            relayNodes.append([(V1[j][0] + V1[i][0])/2, (V1[j][1] + V1[i][1])/2])
        else:
            a = V1[j][0] - V1[i][0]
            b = V1[j][1] - V1[i][1]
            c = math.sqrt(a**2 + b**2)
            a = a/c
            b = b/c
            startPoint = [V1[i][0], V1[i][1]]
            while math.dist(startPoint, V1[j]) > rs:
                relayNodes.append([startPoint[0] + a*0.9*rs, startPoint[1] + b*0.9*rs])
                startPoint = [startPoint[0] + a*0.9*rs, startPoint[1] + b*0.9*rs]
    for mst in MST:
        #2 components mst[0], mst[1]
        #matrixEXY[mst[0]][mst[1]][0]
        fillRelayNodes(mst[0], mst[1])
    
    V2 = relayNodes.copy()
    #finding SSCAT from F
    matrixCover = []
    SSCAT = []
    for i in range(len(V2)):
        listCovered = []
        for j in range(len(targets)):
            if math.dist(V2[i], targets[j]) <= rs +0.0001:
                listCovered.append(1)
            else:
                listCovered.append(0)
        matrixCover.append(listCovered)
    def findMaxLfIndex():
        Lflist = [0]*len(V2)
        for i in range(len(V2)):
            Lflist[i] = sum(matrixCover[i])
        return(Lflist.index(max(Lflist)))

    while sum(sum(matrixCover,[])) != 0:
        maxLfIndex = findMaxLfIndex()
        SSCAT.append(V2[maxLfIndex])
        for i in range(len(targets)):
            if math.dist(V2[maxLfIndex], targets[i]) <= rs +0.0001:
                for j in range(len(V2)):
                    matrixCover[j][i] = 0
    remainRel = V2.copy()
    for sscat in SSCAT:
        remainRel.remove(sscat)

    # V2 là tập các relaynodes và sensor nodes
    remainRel2 = remainRel.copy()
    print(len(V2))
    def isRemove(n):
        _V = remainRel2 + SSCAT
        _V.append([5,5])
        _V.remove(remainRel2[n])
        G3 = Graph_struct(len(_V))
        for i in range(len(_V)-1):
            for j in range(i+1, len(_V)):
                if math.dist(_V[i],_V[j]) <= rc:
                    G3.add_edge(i, j)
        cc = len(G3.connected_components())
        if cc == 1:
            return True
        else:
            return False
    
    ie = 0
    while ie < len(remainRel2):
        if isRemove(ie):
            del remainRel2[ie]
        else:
            ie += 1
        
    VV = SSCAT + remainRel2 + [[5,5]]
    def isCutVertex(index):
        V3_temp = VV.copy()
        del V3_temp[index]
        GG = Graph_struct(len(V3_temp))
        for i in range(len(V3_temp)-1):
            for j in range(i+1, len(V3_temp)):
                if math.dist(V3_temp[i], V3_temp[j]) <= rc:
                    GG.add_edge(i,j)
        cc1 = GG.connected_components()
        if len(cc1) == 1:
            return False
        else:
            return True
    V3 = []
    for i in range(len(VV)):
        if isCutVertex(i) == False:
            V3.append(VV[i])
    
    G3=[]
    DFSG3 = Graph_struct(len(V3))
    for i in range(len(V3)):
        hangi = []
        for j in range(len(V3)):
            if math.dist(V3[i], V3[j]) <= rc:
                DFSG3.add_edge(i, j)
                hangi.append(1)
            else:
                hangi.append(0)
        G3.append(hangi)

    conn_comp3 = DFSG3.connected_components()

    matrixEXY2 = [] 
    for i in range(len(conn_comp3)):
        hangi = []
        for j in range(len(conn_comp3)):
            hangicotj = []
            pointOfi = 0
            pointOfj = 0
            min_distance = 100
            for a in range(len(conn_comp3[i])):
                for b in range(len(conn_comp3[j])):
                    if math.dist(V3[conn_comp3[i][a]], V3[conn_comp3[j][b]]) <= min_distance:
                        pointOfi = conn_comp3[i][a]
                        pointOfj = conn_comp3[j][b]
                        min_distance = math.dist(V3[conn_comp3[i][a]], V3[conn_comp3[j][b]])
            hangicotj.append(pointOfi)
            hangicotj.append(pointOfj)
            hangicotj.append(min_distance)
            hangi.append(hangicotj)
        matrixEXY2.append(hangi)

    G4 = GraphWeight(len(conn_comp3))
    for i in range(len(conn_comp3)-1):
        for j in range(i+1, len(conn_comp3)):
            G4.add_edge(i,j, matrixEXY2[i][j][2])

    MST2 = G4.kruskal_algo()

    relayNodes2 = []
    def fillRelayNodes2(i,j): #add relay nodes to line V1[i] V1[j]
        #vector V1[i] to V[j] = (a,b)
        a = V3[j][0] - V3[i][0]
        b = V3[j][1] - V3[i][1]
        c = math.sqrt(a**2 + b**2)
        a = a/c
        b = b/c
        startPoint = [V3[i][0], V3[i][1]]
        while math.dist(startPoint, V3[j]) > rc:
            relayNodes2.append([startPoint[0] + a*0.9*rc, startPoint[1] + b*0.9*rc])
            startPoint = [startPoint[0] + a*0.9*rc, startPoint[1] + b*0.9*rc]
    for mst in MST2:
        #2 components mst[0], mst[1]
        #matrixEXY[mst[0]][mst[1]][0]
        fillRelayNodes2(matrixEXY2[mst[0]][mst[1]][0], matrixEXY2[mst[0]][mst[1]][1])


    end = time.time()
    #vehinh
    relX2 = []
    relY2 = []
    for i in range(len(relayNodes2)):
        relX2.append(relayNodes2[i][0])
        relY2.append(relayNodes2[i][1])
    remrelX = []
    remrelY = []
    for i in range(len(remainRel)):
        remrelX.append(remainRel[i][0])
        remrelY.append(remainRel[i][1])
    remrel2X = []
    remrel2Y = []
    for i in range(len(remainRel2)):
        remrel2X.append(remainRel2[i][0])
        remrel2Y.append(remainRel2[i][1])
    Sx = []
    Sy = []
    for i in range(len(SSCAT)):
        Sx.append(SSCAT[i][0])
        Sy.append(SSCAT[i][1])
    relX = []
    relY = []
    for i in range(len(relayNodes)):
        relX.append(relayNodes[i][0])
        relY.append(relayNodes[i][1])
    V3x = []
    V3y = []
    for i in range(len(V3)):
        V3x.append(V3[i][0])
        V3y.append(V3[i][1])
    
    fig, axs = plt.subplots(3,3)
    axs[0,0].set_xlim(0,10), axs[0,1].set_xlim(0,10), axs[1,0].set_xlim(0,10), axs[1,1].set_xlim(0,10),axs[0,2].set_xlim(0,10),axs[1,2].set_xlim(0,10),axs[2,0].set_xlim(0,10),axs[2,1].set_xlim(0,10),axs[2,2].set_xlim(0,10)
    axs[0,0].set_ylim(0,10), axs[0,1].set_ylim(0,10), axs[1,0].set_ylim(0,10), axs[1,1].set_ylim(0,10),axs[0,2].set_ylim(0,10),axs[1,2].set_ylim(0,10),axs[2,0].set_ylim(0,10),axs[2,1].set_ylim(0,10),axs[2,2].set_ylim(0,10)
    axs[0,0].set_box_aspect(1), axs[0,1].set_box_aspect(1), axs[1,0].set_box_aspect(1), axs[1,1].set_box_aspect(1),axs[0,2].set_box_aspect(1),axs[1,2].set_box_aspect(1),axs[2,0].set_box_aspect(1),axs[2,1].set_box_aspect(1),axs[2,2].set_box_aspect(1)
    axs[0,0].plot(targetsX, targetsY, '*', color = 'red', markersize=rs*7),axs[0,1].plot(targetsX, targetsY, '*', color = 'red', markersize=rs*7),axs[1,0].plot(targetsX, targetsY, '*', color = 'red', markersize=rs*7)
    axs[0,0].plot([5],[5], '^', color = 'red', markersize = 8), axs[0,1].plot([5],[5], '^', color = 'red', markersize = 8), axs[1,0].plot([5],[5], '^', color = 'red', markersize = 8),axs[1,1].plot([5],[5], '^', color = 'red', markersize = 8),axs[0,2].plot([5],[5], '^', color = 'red', markersize = 8),axs[1,2].plot([5],[5], '^', color = 'red', markersize = 8),axs[2,0].plot([5],[5], '^', color = 'red', markersize = 8),axs[2,1].plot([5],[5], '^', color = 'red', markersize = 8),axs[2,2].plot([5],[5], '^', color = 'red', markersize = 8)
    axs[1,2].plot(V3x, V3y, 'o', color = 'orange', markersize=6, alpha = 0.4)
    axs[1,0].add_patch(plt.Circle((5, 5), rc/2, color='green', alpha = 0.3)),axs[1,1].add_patch(plt.Circle((5, 5), rc/2, color='green', alpha = 0.3)),axs[2,1].add_patch(plt.Circle((5, 5), rc/2, color='green', alpha = 0.3)),axs[2,2].add_patch(plt.Circle((5, 5), rc/2, color='green', alpha = 0.3))
    for mst in MST:
        axs[0,1].plot([V1[mst[0]][0], V1[mst[1]][0]],[V1[mst[0]][1], V1[mst[1]][1]], color='green')
    for i in range(len(relayNodes)):
        axs[0,2].add_patch(plt.Circle((relX[i], relY[i]), rs, color='green', alpha = 0.3))
    for i in range(len(remainRel)):
        axs[1,0].add_patch(plt.Circle((remrelX[i], remrelY[i]), rs, color='green', alpha = 0.3))
    for i in range(len(remainRel2)):
        axs[1,1].add_patch(plt.Circle((remrel2X[i], remrel2Y[i]), rs, color='green', alpha = 0.3))
        axs[2,1].add_patch(plt.Circle((remrel2X[i], remrel2Y[i]), rs, color='green', alpha = 0.3))
    for i in range(len(SSCAT)):
        axs[1,0].add_patch(plt.Circle((Sx[i], Sy[i]), rs, color='orange', alpha = 0.5))
        axs[1,1].add_patch(plt.Circle((Sx[i], Sy[i]), rs, color='orange', alpha = 0.5))
        axs[2,0].add_patch(plt.Circle((Sx[i], Sy[i]), rs, color='orange', alpha = 0.5))
        axs[2,1].add_patch(plt.Circle((Sx[i], Sy[i]), rs, color='orange', alpha = 0.5))
        axs[2,2].add_patch(plt.Circle((Sx[i], Sy[i]), rs, color='orange', alpha = 0.5))
    for i in range(len(MST2)):
        matrixEXY2[MST2[i][0]][MST2[i][1]][0]
        matrixEXY2[MST2[i][0]][MST2[i][1]][1]
        axs[1,2].plot([V3[matrixEXY2[MST2[i][0]][MST2[i][1]][0]][0], V3[matrixEXY2[MST2[i][0]][MST2[i][1]][1]][0],], [V3[matrixEXY2[MST2[i][0]][MST2[i][1]][0]][1], V3[matrixEXY2[MST2[i][0]][MST2[i][1]][1]][1]], color='blue')
    for i in range(len(V3)-1):
        for j in range(i+1, len(V3)):
            if G3[i][j] == 1:
                axs[1,2].plot([V3[i][0], V3[j][0],], [V3[i][1], V3[j][1]], color='purple')    
    for i in range(len(relayNodes2)):
        axs[2,0].add_patch(plt.Circle((relX2[i], relY2[i]), rc/2, color='blue', alpha = 0.3))
        axs[2,1].add_patch(plt.Circle((relX2[i], relY2[i]), rc/2, color='blue', alpha = 0.3))
    plt.show()
    
    print(f"Runtime is {end - start}")
    print(f"Total Sensing Nodes is {len(SSCAT)}")
    return SSCAT

class GraphWeight:
        def __init__(self, vertices):
            self.V = vertices
            self.graph = []

        def add_edge(self, u, v, w):
            self.graph.append([u, v, w])

        # Search function

        def find(self, parent, i):
            if parent[i] == i:
                return i
            return self.find(parent, parent[i])

        def apply_union(self, parent, rank, x, y):
            xroot = self.find(parent, x)
            yroot = self.find(parent, y)
            if rank[xroot] < rank[yroot]:
                parent[xroot] = yroot
            elif rank[xroot] > rank[yroot]:
                parent[yroot] = xroot
            else:
                parent[yroot] = xroot
                rank[xroot] += 1

        #  Applying Kruskal algorithm
        def kruskal_algo(self):
            result = []
            i, e = 0, 0
            self.graph = sorted(self.graph, key=lambda item: item[2])
            parent = []
            rank = []
            for node in range(self.V):
                parent.append(node)
                rank.append(0)
            while e < self.V - 1:
                u, v, w = self.graph[i]
                i = i + 1
                x = self.find(parent, u)
                y = self.find(parent, v)
                if x != y:
                    e = e + 1
                    result.append([u, v])
                    self.apply_union(parent, rank, x, y)
            return result
class Graph_struct:
   def __init__(self, V):
      self.V = V
      self.adj = [[] for i in range(V)]

   def DFS_Utililty(self, temp, v, visited):

      visited[v] = True

      temp.append(v)

      for i in self.adj[v]:
         if visited[i] == False:
            temp = self.DFS_Utililty(temp, i, visited)
      return temp

   def add_edge(self, v, w):
      self.adj[v].append(w)
      self.adj[w].append(v)

   def connected_components(self):
      visited = []
      conn_compnent = []
      for i in range(self.V):
         visited.append(False)
      for v in range(self.V):
         if visited[v] == False:
            temp = []
            conn_compnent.append(self.DFS_Utililty(temp, v, visited))
      return conn_compnent
SSCAT = runNewAlgo(1, 17)