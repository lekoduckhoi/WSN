import random
import math 
import matplotlib.pyplot as plt
from collections import defaultdict
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
    # print(f"Runtime of the program is {end - start}")
    # print(f"Total Sensing Nodes is {len(SSCAT)}")
    return [SSCAT, end - start]

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
def runPha2(_rc, SSCAT): 
    start = time.time()
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
    end = time.time()
    return [len(remainRel)+ len(remainRel2), end - start]

def runTest(_rs, _rc,_n0targets, _n0test):
    print(f"After {_n0test} tests with {_n0targets} targets, sensing range {_rs} and communication range {_rc} in a 10x10 field, We have: ")
    totalTime1 = 0
    totalTime2 = 0
    n0s = 0
    n0r = 0
    for i in range(_n0test):
        res1 = runPha1(_rs, _n0targets)
        res2 = runPha2(_rc, res1[0])
        totalTime1 += res1[1]
        totalTime2 += res2[1]
        n0s += len(res1[0])
        n0r += res2[0]
    print("1. Average runtime of Pha1: ", totalTime1/_n0test)
    print("2. Average runtime of Pha2: ", totalTime2/_n0test)
    print("3. Average number of Sensors Nodes: ", n0s/_n0test)
    print("4. Average number of Relay Nodes: ", n0r/_n0test)

#runTest(Sensing Radius, Communication Range, Number of Targets, Number of Tests)
runTest(1,2,17,100)