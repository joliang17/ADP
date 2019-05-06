from numba import jit
import numpy as np
from scipy.sparse.csgraph import dijkstra, shortest_path

class Network:

    def __init__(self, Stop_Number):
        self.Stop_Number = Stop_Number
        self.Graph = np.zeros([Stop_Number, Stop_Number])
        self.Graph_Shortest = np.zeros([Stop_Number, Stop_Number])

    @jit(nopython=True)
    def Generate_Graph(self, Density):
        for i in range(self.Stop_Number):
            for j in range(i+1, self.Stop_Number):
                Temp1 = np.random.rand()
                if(Temp1 <= Density):
                    Length = int(np.random.rand()*10)
                    self.Graph[i][j] = Length
        return

    @jit(nopython=True)
    def Gain_Shortest_Path(self, Stop_Number):
        # 获得每个点到另外一个点的最短路
        # 如果有直接连接(Graph[i][j]>0)
        # 最短路直接就是这个那条路
        # 如果无直接连接(Graph[i][j]=0)
        # 运用最短路算法，获得最短路径
        # 注意：转乘一定大于直达

        # 需要记录内容：
        # 1. 最短距离(数字)
        # 2. 最短距离对应的路线
        # 字典形式存储！
        # ShortestPath_Set={(1,2):[2,3,4]...}

        # find the shortest path
        Cgraph = np.array(self.Graph)
        self.Graph_Shortest, predecessor = shortest_path(Cgraph, method='auto', directed=False, return_predecessors=True)
        # dist_matrix, predecessor = shortest_path(Cgraph,method='auto',directed=False, return_predecessors=True)

        # modify the result
        ShortestPath_Set = {}
        for i in range(Stop_Number):
            for j in range(i+1, Stop_Number):
                ShortestPath_Set[(i,j)] = [] 
                ShortestPath_Set[(j,i)] = [] 
                pre_Node = predecessor[i][j]
                # 当i到j不为直达：
                while pre_Node != i:
                    # i到j: 比如1-->3-->5-->7
                    # [i,j]: [3, 5]
                    # [j,i]: [5, 3]
                    ShortestPath_Set[(i,j)].insert(0,pre_Node)
                    ShortestPath_Set[(j,i)].append(pre_Node)
                    pre_Node = predecessor[i][pre_Node]
                
        return ShortestPath_Set
