import random
import math 
import matplotlib.pyplot as plt
import time
from collections import defaultdict
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
def runNewAlgo(_rs,_rc, n0targets):
    start = time.time()
    rs = _rs #sensing radius
    rc = _rc
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
    rrl = V2.copy()
    for sscat in SSCAT:
        rrl.remove(sscat)

    # V2 l?? t???p c??c relaynodes v?? sensor nodes
    rrl2 = rrl.copy()
    def isRemove(n):
        _V = rrl2 + SSCAT
        _V.append([5,5])
        _V.remove(rrl2[n])
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
    
    iee = 0
    while iee < len(rrl2):
        if isRemove(iee):
            del rrl2[iee]
        else:
            iee += 1
        
    VV = SSCAT + rrl2 + [[5,5]]
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

    VT = SSCAT + [[5,5]]
    remainRel = relayNodes.copy()
    remainRel2 = relayNodes2.copy()
    def isRemoveNodes(n):
        Gn = Graph(len(VT)+len(remainRel)+len(remainRel2)-1)
        removen = remainRel.copy()
        del removen[n]
        Vn = VT + remainRel2 + removen
        for i in range(len(Vn)-1):
            for j in range(len(Vn)):
                if math.dist(Vn[i], Vn[j]) <= rc:
                    Gn.addEdge(i, j)
        if Gn.isBC():
            return True
        else:
            return False
    def isRemoveNodes2(n):
        Gn = Graph(len(VT)+len(remainRel)+len(remainRel2)-1)
        removen = remainRel2.copy()
        del removen[n]
        Vn = VT + remainRel + removen
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

    end = time.time()
    
    
    # print(f"Runtime is {end - start}")
    # print(f"Total Sensing Nodes is {len(SSCAT)}")
    return [SSCAT, remainRel, remainRel2, end - start]
#runNewAlgo(sensing radius, communication range, number of targets)
runNewAlgo(0.5,1.5, 17)
def runTestNewAlgo(_rs, _rc,_n0targets, _n0test):
    print(f"With new Algorithm, after {_n0test} tests with {_n0targets} targets, sensing range {_rs} and communication range {_rc} in a 10x10 field, We have: ")
    totalTime = 0
    n0s = 0
    n0r = 0
    for i in range(_n0test):
        res = runNewAlgo(_rs, _rc, _n0targets)
        totalTime += res[3]
        n0s += len(res[0])
        n0r += (len(res[1])+len(res[2]))
    print("1. Average runtime: ", totalTime/_n0test)
    print("2. Average number of Sensors Nodes: ", n0s/_n0test)
    print("3. Average number of Relay Nodes: ", n0r/_n0test)

#runTest(Sensing Radius, Communication Range, Number of Targets, Number of Tests)
runTestNewAlgo(1,2,100,100)