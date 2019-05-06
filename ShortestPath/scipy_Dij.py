from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra, shortest_path
import numpy as np

Graph = [[0,6,2],[6,0,3],[2,3,0]]
Cgraph = np.array(Graph)
print(Cgraph)

dist_matrix, predecessor = shortest_path(Cgraph,method='auto',directed=False, return_predecessors=True)
print(dist_matrix)
print(predecessor)
ShortestPath_Set = {}
for i in range(3):
    for j in range(i+1,3):
        ShortestPath_Set[(i,j)] = [] 
        ShortestPath_Set[(j,i)] = [] 
        pre_Node = predecessor[i][j]
        while pre_Node != i:
            # i到j: 比如1-->3-->5-->7
            # [i,j]: [3, 5]
            # [j,i]: [5,3]
            ShortestPath_Set[(i,j)].insert(0,pre_Node)
            ShortestPath_Set[(j,i)].append(pre_Node)
            pre_Node = predecessor[i][pre_Node]

print(ShortestPath_Set)