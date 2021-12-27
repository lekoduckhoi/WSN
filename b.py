def findMaxLf():
    Lflist = [0]*len(matrix)
    for i in range(len(matrix)):
        Lflist[i] = sum(matrix[i])
    return(Lflist.index(max(Lflist)))

matrix = [[2,3,4], [3,4,5], [1,2,1], [4,5,6]]

a = findMaxLf()
print(a)
print(sum(sum(matrix,[])))