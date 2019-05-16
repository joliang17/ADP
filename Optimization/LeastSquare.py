import padasip as pa
import numpy as np

class LeastSquare:
    def __init__(self, p, ValuePart1, ValuePart2, TotalValue):
        self.p = p
        self.ValuePart1 = ValuePart1
        self.ValuePart2 = ValuePart2
        self.TotalValue = TotalValue
        self.d = np.array([TotalValue], dtype=float)
        self.x = np.array([ValuePart1, ValuePart2], dtype=float)

    def MainPart(self):
        filt = pa.filters.FilterRLS(2, mu=0.99)
        y, e, w = filt.run(self.d, self.x)
        
        return





