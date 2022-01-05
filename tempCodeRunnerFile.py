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