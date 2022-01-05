import random
import math 
import matplotlib.pyplot as plt
import time
def runNewAlgo(_rs, n0targets):
    start = time.time()
    rs = _rs #sensing radius
    _rc = rs
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
            while math.dist(startPoint, V1[j]) > _rc:
                relayNodes.append([startPoint[0] + a*0.9*_rc, startPoint[1] + b*0.9*_rc])
                startPoint = [startPoint[0] + a*0.9*_rc, startPoint[1] + b*0.9*_rc]
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

    V3 = V2.copy()
    V3.append([5,5])
    matrixConnect = []
    for i in range(len(V3)):
        listConnect = []
        for j in range(len(V3)):
            if math.dist(V3[i], V3[j]) <= rs:
                listConnect.append(1)
            else:
                listConnect.append(0)
        matrixConnect.append(listCovered)

    # for dinh in V3:
    #     deg = 0
    #     for dinh2 in V3:
    #         if math.dist(dinh, dinh2) <= rs*2:







    end = time.time()
    #vehinh
    remrelX = []
    remrelY = []
    for i in range(len(remainRel)):
        remrelX.append(remainRel[i][0])
        remrelY.append(remainRel[i][1])
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
    axs[0,0].plot(targetsX, targetsY, '*', color = 'red', markersize=rs*7),axs[0,1].plot(targetsX, targetsY, '*', color = 'red', markersize=rs*7),axs[1,0].plot(targetsX, targetsY, '*', color = 'red', markersize=rs*7),axs[2,0].plot(targetsX, targetsY, '*', color = 'red', markersize=rs*7),axs[2,1].plot(targetsX, targetsY, '*', color = 'red', markersize=rs*7),axs[0,2].plot(targetsX, targetsY, '*', color = 'red', markersize=rs*7),axs[1,2].plot(targetsX, targetsY, '*', color = 'red', markersize=rs*7),axs[2,2].plot(targetsX, targetsY, '*', color = 'red', markersize=rs*7)
    axs[0,0].plot([5],[5], '^', color = 'red', markersize = 8), axs[0,1].plot([5],[5], '^', color = 'red', markersize = 8), axs[1,0].plot([5],[5], '^', color = 'red', markersize = 8),axs[1,1].plot([5],[5], '^', color = 'red', markersize = 8),axs[0,2].plot([5],[5], '^', color = 'red', markersize = 8),axs[1,2].plot([5],[5], '^', color = 'red', markersize = 8),axs[2,0].plot([5],[5], '^', color = 'red', markersize = 8),axs[2,1].plot([5],[5], '^', color = 'red', markersize = 8),axs[2,2].plot([5],[5], '^', color = 'red', markersize = 8)
    axs[1,1].plot(V3x, V3y, 'o', color = 'orange', markersize=6, alpha = 0.4),axs[1,2].plot(V3x, V3y, 'o', color = 'orange', markersize=6, alpha = 0.4)
    for mst in MST:
        axs[0,1].plot([V1[mst[0]][0], V1[mst[1]][0]],[V1[mst[0]][1], V1[mst[1]][1]], color='green')
    for i in range(len(relayNodes)):
        axs[0,2].add_patch(plt.Circle((relX[i], relY[i]), _rc, color='green', alpha = 0.3))
    for i in range(len(remainRel)):
        axs[1,0].add_patch(plt.Circle((remrelX[i], remrelY[i]), _rc, color='green', alpha = 0.3))
    for i in range(len(SSCAT)):
        axs[1,0].add_patch(plt.Circle((Sx[i], Sy[i]), _rc, color='orange', alpha = 0.5))
    plt.show()
    
    print(f"Runtime of Pha1 is {end - start}")
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