from numba import jit
import numpy as np

class Network:

    def __init__(self, Stop_Number):
        self.Stop_Number = Stop_Number
        self.Graph = np.zeros([Stop_Number, Stop_Number])

    @jit(nopython=True)
    def Generate_Graph(self, Density):
        for i in range(self.Stop_Number):
            for j in range(i+1, self.Stop_Number):
                Temp1 = np.random.rand()
                if(Temp1 <= Density):
                    Length = int(np.random.rand()*10)
                    self.Graph[i][j] = Length
        return

