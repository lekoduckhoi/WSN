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
axs[0,1].plot(Sx, Sy, 'o', color = 'black', markersize=6, alpha = 0.4)
for i in range(len(SSCAT)):
    axs[0,0].add_patch(plt.Circle((Sx[i], Sy[i]), 2, color='orange', alpha = 0.5))
for i in range(len(V1)-1):
    for j in range(i+1, len(V1)):
        if G1[i][j] == 1:
            axs[0,1].plot([V1[i][0], V1[j][0],], [V1[i][1], V1[j][1]], color='grey')



plt.show()
