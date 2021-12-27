import pha1
import math 
import matplotlib.pyplot as plt
SSCAT = pha1.SSCAT.copy()
rc = 2 #communication radius
V1 = SSCAT.copy()
V1.append([5,5]) #add base station 
G1 = []

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
DFSG1 = Graph_struct(len(V1))
for i in range(len(V1)):
    hangi = []
    for j in range(len(V1)):
        if math.dist(V1[i], V1[j]) <= rc: 
            DFSG1.add_edge(i, j)
            hangi.append(1)
        else:
            hangi.append(0)
    G1.append(hangi)    


conn_comp = DFSG1.connected_components()
print("The connected components are :")
print(V1)
print(conn_comp)

#matrixEXY[i][j] = [a,b, d] => distant between 2 connected component index i and j
# is d = distant of point index a in i and b in j
matrixEXY = [] 
for i in range(len(conn_comp)):
    hangi = []
    for j in range(len(conn_comp)):
        hangicotj = []
        pointOfi = 0
        pointOfj = 0
        min_distance = 100
        for a in range(len(conn_comp[i])):
            for b in range(len(conn_comp[j])):
                if math.dist(V1[conn_comp[i][a]], V1[conn_comp[j][b]]) <= min_distance:
                    pointOfi = conn_comp[i][a]
                    pointOfj = conn_comp[j][b]
                    min_distance = math.dist(V1[conn_comp[i][a]], V1[conn_comp[j][b]])
        hangicotj.append(pointOfi)
        hangicotj.append(pointOfj)
        hangicotj.append(min_distance)
        hangi.append(hangicotj)
    matrixEXY.append(hangi)
print(matrixEXY)

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
        

G2 = GraphWeight(len(conn_comp))
for i in range(len(conn_comp)-1):
    for j in range(i+1, len(conn_comp)):
        G2.add_edge(i,j, matrixEXY[i][j][2])

MST = G2.kruskal_algo()
print(MST)


Sx = []
Sy = []
for i in range(len(SSCAT)):
    Sx.append(SSCAT[i][0])
    Sy.append(SSCAT[i][1])

fig, axs = plt.subplots(2,2)
axs[0,0].set_xlim(0,10), axs[0,1].set_xlim(0,10), axs[1,0].set_xlim(0,10), axs[1,1].set_xlim(0,10)
axs[0,0].set_ylim(0,10), axs[0,1].set_ylim(0,10), axs[1,0].set_ylim(0,10), axs[1,1].set_ylim(0,10)
axs[0,0].set_box_aspect(1), axs[0,1].set_box_aspect(1), axs[1,0].set_box_aspect(1), axs[1,1].set_box_aspect(1)
axs[0,0].plot([5],[5], '^', color = 'red', markersize = 8), axs[0,1].plot([5],[5], '^', color = 'red', markersize = 8), axs[1,0].plot([5],[5], '^', color = 'red', markersize = 8),axs[1,1].plot([5],[5], '^', color = 'red', markersize = 8)
axs[0,0].plot(Sx, Sy, 'o', color = 'black', markersize=1)
axs[0,1].plot(Sx, Sy, 'o', color = 'black', markersize=6, alpha = 0.4),axs[1,0].plot(Sx, Sy, 'o', color = 'black', markersize=6, alpha = 0.4)
for i in range(len(SSCAT)):
    axs[0,0].add_patch(plt.Circle((Sx[i], Sy[i]), 2, color='orange', alpha = 0.5))
for i in range(len(V1)-1):
    for j in range(i+1, len(V1)):
        if G1[i][j] == 1:
            axs[0,1].plot([V1[i][0], V1[j][0],], [V1[i][1], V1[j][1]], color='grey')
            axs[1,0].plot([V1[i][0], V1[j][0],], [V1[i][1], V1[j][1]], color='grey')
for i in range(len(MST)):
    matrixEXY[MST[i][0]][MST[i][1]][0]
    matrixEXY[MST[i][0]][MST[i][1]][1]
    axs[1,0].plot([V1[matrixEXY[MST[i][0]][MST[i][1]][0]][0], V1[matrixEXY[MST[i][0]][MST[i][1]][1]][0],], [V1[matrixEXY[MST[i][0]][MST[i][1]][0]][1], V1[matrixEXY[MST[i][0]][MST[i][1]][1]][1]], color='green')


plt.show()
