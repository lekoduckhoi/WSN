import pha1
import math 
import matplotlib.pyplot as plt
from collections import defaultdict
import time
class Graph:
	def __init__(self,vertices):
		self.V= vertices #No. of vertices
		self.graph = defaultdict(list) # default dictionary to store graph
		self.Time = 0

	# function to add an edge to graph
	def addEdge(self,u,v):
		self.graph[u].append(v)
		self.graph[v].append(u)

	def isBCUtil(self,u, visited, parent, low, disc):

		#Count of children in current node
		children =0

		# Mark the current node as visited and print it
		visited[u]= True

		# Initialize discovery time and low value
		disc[u] = self.Time
		low[u] = self.Time
		self.Time += 1

		#Recur for all the vertices adjacent to this vertex
		for v in self.graph[u]:
			# If v is not visited yet, then make it a child of u
			# in DFS tree and recur for it
			if visited[v] == False :
				parent[v] = u
				children += 1
				if self.isBCUtil(v, visited, parent, low, disc):
					return True

				# Check if the subtree rooted with v has a connection to
				# one of the ancestors of u
				low[u] = min(low[u], low[v])

				# u is an articulation point in following cases
				# (1) u is root of DFS tree and has two or more children.
				if parent[u] == -1 and children > 1:
					return True

				#(2) If u is not root and low value of one of its child is more
				# than discovery value of u.
				if parent[u] != -1 and low[v] >= disc[u]:
					return True
					
			elif v != parent[u]: # Update low value of u for parent function calls.
				low[u] = min(low[u], disc[v])

		return False


	# The main function that returns true if graph is Biconnected,
	# otherwise false. It uses recursive function isBCUtil()
	def isBC(self):

		# Mark all the vertices as not visited and Initialize parent and visited,
		# and ap(articulation point) arrays
		visited = [False] * (self.V)
		disc = [float("Inf")] * (self.V)
		low = [float("Inf")] * (self.V)
		parent = [-1] * (self.V)
	

		# Call the recursive helper function to find if there is an
		# articulation points in given graph. We do DFS traversal starting
		# from vertex 0
		if self.isBCUtil(0, visited, parent, low, disc):
			return False

		if any(i == False for i in visited):
			return False
		
		return True
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
def runPha2(_rc): 
    start = time.time()
    SSCAT = pha1.SSCAT.copy()
    rc = _rc #communication radius
    V1 = SSCAT.copy()
    V1.append([5,5]) #add base station 
    G1 = []
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
            print(result)
            return result


    G2 = GraphWeight(len(conn_comp))
    for i in range(len(conn_comp)-1):
        for j in range(i+1, len(conn_comp)):
            G2.add_edge(i,j, matrixEXY[i][j][2])

    MST = G2.kruskal_algo()

    relayNodes = []
    def fillRelayNodes(i,j): #add relay nodes to line V1[i] V1[j]
        #vector V1[i] to V[j] = (a,b)
        a = V1[j][0] - V1[i][0]
        b = V1[j][1] - V1[i][1]
        c = math.sqrt(a**2 + b**2)
        a = a/c
        b = b/c
        startPoint = [V1[i][0], V1[i][1]]
        while math.dist(startPoint, V1[j]) > rc:
            relayNodes.append([startPoint[0] + a*0.9*_rc, startPoint[1] + b*0.9*_rc])
            startPoint = [startPoint[0] + a*0.9*_rc, startPoint[1] + b*0.9*_rc]
    for mst in MST:
        #2 components mst[0], mst[1]
        #matrixEXY[mst[0]][mst[1]][0]
        fillRelayNodes(matrixEXY[mst[0]][mst[1]][0], matrixEXY[mst[0]][mst[1]][1])

    #phan 2 Ensuring fault-tolerance:

    V2 = V1.copy()
    for i in range(len(relayNodes)):
        V2.append(relayNodes[i])

    def isCutVertex(index):
        V2_temp = V2.copy()
        del V2_temp[index]
        GG = Graph_struct(len(V2_temp))
        for i in range(len(V2_temp)-1):
            for j in range(i+1, len(V2_temp)):
                if math.dist(V2_temp[i], V2_temp[j]) <= rc:
                    GG.add_edge(i,j)
        conn_comp1 = GG.connected_components()
        if len(conn_comp1) == 1:
            return False
        else:
            return True
    V3 = []
    for i in range(len(V2)):
        if isCutVertex(i) == False:
            V3.append(V2[i])
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
            relayNodes2.append([startPoint[0] + a*0.9*_rc, startPoint[1] + b*0.9*_rc])
            startPoint = [startPoint[0] + a*0.9*_rc, startPoint[1] + b*0.9*_rc]
    for mst in MST2:
        #2 components mst[0], mst[1]
        #matrixEXY[mst[0]][mst[1]][0]
        fillRelayNodes2(matrixEXY2[mst[0]][mst[1]][0], matrixEXY2[mst[0]][mst[1]][1])

    #improvement step
    remainRel = relayNodes.copy()
    remainRel2 = relayNodes2.copy()
    def isRemoveNodes(n):
        Gn = Graph(len(V1)+len(remainRel)+len(remainRel2)-1)
        removen = remainRel.copy()
        del removen[n]
        Vn = V1 + remainRel2 + removen
        for i in range(len(Vn)-1):
            for j in range(len(Vn)):
                if math.dist(Vn[i], Vn[j]) <= rc:
                    Gn.addEdge(i, j)
        if Gn.isBC():
            return True
        else:
            return False
    def isRemoveNodes2(n):
        Gn = Graph(len(V1)+len(remainRel)+len(remainRel2)-1)
        removen = remainRel2.copy()
        del removen[n]
        Vn = V1 + remainRel + removen
        for i in range(len(Vn)-1):
            for j in range(len(Vn)):
                if math.dist(Vn[i], Vn[j]) <= rc:
                    Gn.addEdge(i, j)
        if Gn.isBC():
            return True
        else:
            return False
    ie = 0
    while ie < len(remainRel):
        if isRemoveNodes(ie):
            del remainRel[ie]
        else:
            ie += 1
    ie2 = 0
    while ie2 < len(remainRel2):
        if isRemoveNodes2(ie2):
            del remainRel2[ie2]
        else:
            ie2 += 1   
    print("Number of Sensor Nodes: ", len(SSCAT))
    print("Number of Relay Nodes: ", len(remainRel)+len(remainRel2))
    #ve hinh
    V3x = []
    V3y = []

    for i in range(len(V3)):
        V3x.append(V3[i][0])
        V3y.append(V3[i][1])

    relX = []
    relY = []
    for i in range(len(relayNodes)):
        relX.append(relayNodes[i][0])
        relY.append(relayNodes[i][1])

    remrelX = []
    remrelY = []
    for i in range(len(remainRel)):
        remrelX.append(remainRel[i][0])
        remrelY.append(remainRel[i][1])
    remrelX2 = []
    remrelY2 = []
    for i in range(len(remainRel2)):
        remrelX2.append(remainRel2[i][0])
        remrelY2.append(remainRel2[i][1])

    relX2 = []
    relY2 = []
    for i in range(len(relayNodes2)):
        relX2.append(relayNodes2[i][0])
        relY2.append(relayNodes2[i][1])

    Sx = []
    Sy = []
    for i in range(len(SSCAT)):
        Sx.append(SSCAT[i][0])
        Sy.append(SSCAT[i][1])

    end = time.time()

    # total time taken
    print(f"Runtime of Pha2 is {end - start}")
    fig, axs = plt.subplots(3,3)
    #axs[2,2].plot(tarX, tarY, '*', color = 'red', markersize=7)
    axs[0,0].set_xlim(0,10), axs[0,1].set_xlim(0,10), axs[1,0].set_xlim(0,10), axs[1,1].set_xlim(0,10),axs[0,2].set_xlim(0,10),axs[1,2].set_xlim(0,10),axs[2,0].set_xlim(0,10),axs[2,1].set_xlim(0,10),axs[2,2].set_xlim(0,10)
    axs[0,0].set_ylim(0,10), axs[0,1].set_ylim(0,10), axs[1,0].set_ylim(0,10), axs[1,1].set_ylim(0,10),axs[0,2].set_ylim(0,10),axs[1,2].set_ylim(0,10),axs[2,0].set_ylim(0,10),axs[2,1].set_ylim(0,10),axs[2,2].set_ylim(0,10)
    axs[0,0].set_box_aspect(1), axs[0,1].set_box_aspect(1), axs[1,0].set_box_aspect(1), axs[1,1].set_box_aspect(1),axs[0,2].set_box_aspect(1),axs[1,2].set_box_aspect(1),axs[2,0].set_box_aspect(1),axs[2,1].set_box_aspect(1),axs[2,2].set_box_aspect(1)
    axs[0,0].plot([5],[5], '^', color = 'red', markersize = 8), axs[0,1].plot([5],[5], '^', color = 'red', markersize = 8), axs[1,0].plot([5],[5], '^', color = 'red', markersize = 8),axs[1,1].plot([5],[5], '^', color = 'red', markersize = 8),axs[0,2].plot([5],[5], '^', color = 'red', markersize = 8),axs[1,2].plot([5],[5], '^', color = 'red', markersize = 8),axs[2,0].plot([5],[5], '^', color = 'red', markersize = 8),axs[2,1].plot([5],[5], '^', color = 'red', markersize = 8),axs[2,2].plot([5],[5], '^', color = 'red', markersize = 8)
    axs[0,0].plot(Sx, Sy, 'o', color = 'black', markersize=rc/2),axs[1,0].plot(Sx, Sy, 'o', color = 'black', markersize=rc/2), axs[2,1].plot(Sx, Sy, 'o', color = 'black', markersize=rc/2)
    axs[0,0].add_patch(plt.Circle((5, 5), rc/2, color='orange', alpha = 0.5)),axs[1,0].add_patch(plt.Circle((5, 5), rc/2, color='orange', alpha = 0.5)),axs[2,1].add_patch(plt.Circle((5, 5), rc/2, color='orange', alpha = 0.5)),axs[2,2].add_patch(plt.Circle((5, 5), rc/2, color='orange', alpha = 0.5))

    axs[1,1].plot(V3x, V3y, 'o', color = 'orange', markersize=6, alpha = 0.4),axs[1,2].plot(V3x, V3y, 'o', color = 'orange', markersize=6, alpha = 0.4)
    axs[2,0].plot(V3x, V3y, 'o', color = 'black', markersize=1)
    axs[2,0].plot(relX2, relY2, 'o', color = 'blue', markersize=1),axs[2,1].plot(relX2, relY2, 'o', color = 'blue', markersize=rc/2)
    axs[1,0].plot(relX, relY, 'o', color = 'green', markersize=1),axs[2,1].plot(relX, relY, 'o', color = 'green', markersize=rc/2)
    axs[0,1].plot(Sx, Sy, 'o', color = 'orange', markersize=6, alpha = 0.4),axs[0,2].plot(Sx, Sy, 'o', color = 'orange', markersize=6, alpha = 0.4)

    for i in range(len(SSCAT)):
        axs[0,0].add_patch(plt.Circle((Sx[i], Sy[i]), rc/2, color='orange', alpha = 0.5))
        axs[1,0].add_patch(plt.Circle((Sx[i], Sy[i]), rc/2, color='orange', alpha = 0.5))
        axs[2,1].add_patch(plt.Circle((Sx[i], Sy[i]), rc/2, color='orange', alpha = 0.5))
        axs[2,2].add_patch(plt.Circle((Sx[i], Sy[i]), rc/2, color='orange', alpha = 0.5))
    for i in range(len(V3)):
        axs[2,0].add_patch(plt.Circle((V3x[i], V3y[i]), rc/2, color='orange', alpha = 0.5))
    for i in range(len(V1)-1):
        for j in range(i+1, len(V1)):
            if G1[i][j] == 1:
                axs[0,1].plot([V1[i][0], V1[j][0],], [V1[i][1], V1[j][1]], color='purple')
                axs[0,2].plot([V1[i][0], V1[j][0],], [V1[i][1], V1[j][1]], color='purple')
    for i in range(len(V3)-1):
        for j in range(i+1, len(V3)):
            if G3[i][j] == 1:
                axs[1,1].plot([V3[i][0], V3[j][0],], [V3[i][1], V3[j][1]], color='purple')
                axs[1,2].plot([V3[i][0], V3[j][0],], [V3[i][1], V3[j][1]], color='purple')    
    for i in range(len(MST)):
        axs[0,2].plot([V1[matrixEXY[MST[i][0]][MST[i][1]][0]][0], V1[matrixEXY[MST[i][0]][MST[i][1]][1]][0],], [V1[matrixEXY[MST[i][0]][MST[i][1]][0]][1], V1[matrixEXY[MST[i][0]][MST[i][1]][1]][1]], color='green')
    for i in range(len(relayNodes)):
        axs[1,0].add_patch(plt.Circle((relX[i], relY[i]), rc/2, color='green', alpha = 0.3))
        axs[2,1].add_patch(plt.Circle((relX[i], relY[i]), rc/2, color='green', alpha = 0.3))
    for i in range(len(remainRel)):
        axs[2,2].add_patch(plt.Circle((remrelX[i], remrelY[i]), rc/2, color='green', alpha = 0.3))
    for i in range(len(remainRel2)):
        axs[2,2].add_patch(plt.Circle((remrelX2[i], remrelY2[i]), rc/2, color='blue', alpha = 0.3))
    for i in range(len(relayNodes2)):
        axs[2,0].add_patch(plt.Circle((relX2[i], relY2[i]), rc/2, color='blue', alpha = 0.3))
        axs[2,1].add_patch(plt.Circle((relX2[i], relY2[i]), rc/2, color='blue', alpha = 0.3))
    for i in range(len(MST2)):
        matrixEXY2[MST2[i][0]][MST2[i][1]][0]
        matrixEXY2[MST2[i][0]][MST2[i][1]][1]
        axs[1,2].plot([V3[matrixEXY2[MST2[i][0]][MST2[i][1]][0]][0], V3[matrixEXY2[MST2[i][0]][MST2[i][1]][1]][0],], [V3[matrixEXY2[MST2[i][0]][MST2[i][1]][0]][1], V3[matrixEXY2[MST2[i][0]][MST2[i][1]][1]][1]], color='blue')

    plt.show()


runPha2(1)