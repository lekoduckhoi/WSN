def isCutVertex(index):
        V3_temp = V3.copy()
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
    V4 = []
    for i in range(len(V3)):
        if isCutVertex(i) == False:
            V4.append(V3[i])
    print(len(V3))
    print(len(V4))