from scipy.optimize import minimize
import numpy as np

class Minimize:
    def __init__(self, c, p, Stop_Number, Vehicle_Number, Shortest_Matrix, Cur_Loc_Veh, Cur_Loc_Pac, Dest_Pak, Rat_Load, Weight_Pac, Latest_Time, Records, UnRellocated_Order, Transport_Order, System_T):
        self.c = c
        self.p = p
        self.Stop_Number = Stop_Number
        self.Vehicle_Number = Vehicle_Number
        self.Shortest_Matrix = Shortest_Matrix
        self.Cur_Loc_Veh = Cur_Loc_Veh
        self.Cur_Loc_Pac = Cur_Loc_Pac
        self.Dest_Pak = Dest_Pak
        self.Rat_Load = Rat_Load
        self.Weight_Pac = Weight_Pac
        self.Latest_Time = Latest_Time
        self.Records = Records
        self.UnRellocated_Order = UnRellocated_Order
        self.Transport_Order = Transport_Order
        self.System_T = System_T

def Prepare_Variables_Cost(self):

    # 生成车辆当前位置与包裹当前位置的距离矩阵: i*j
    # SH[i][j]: 车辆i与包裹j之间的距离【Cur_Loc_Veh[i], Cur_Loc_Pac[j]】
    Veh_Pack_Distance = np.zeros(
        (len(self.UnRellocated_Order), self.Vehicle_Number), dtype=float)
    for i in range(self.Vehicle_Number):
        for j in range(len(self.UnRellocated_Order)):
            Veh_Pack_Distance[i][j] == self.Shortest_Matrix[self.Cur_Loc_Veh[i]
                                                       ][self.Cur_Loc_Pac[j]]
    Veh_Pack_Distance = np.mat(Veh_Pack_Distance, dtype=float)

    # 待分配包裹重量集合: 1*j
    Weight_UnRellocated = [self.Weight_Pac[i] for i in self.UnRellocated_Order]
    Weight_UnRellocated = np.mat(Weight_UnRellocated, dtype=float)

    # 运输中包裹重量集合: 1*j
    Weight_Rellocated = [self.Weight_Pac[i]
                         for i in self.Transport_Order if i not in self.UnRellocated_Order]
    Weight_Rellocated = np.mat(Weight_Rellocated, dtype=float)

    # 配送记录: i*j
    Records_Matrix = np.mat(self.Records, dtype=np.int)

    # 配送记录: 1*i
    Rat_Load = np.mat(self.Rat_Load, dtype=float)

    return Weight_UnRellocated, Weight_Rellocated, Rat_Load, Records_Matrix, Veh_Pack_Distance

def CostF(self, x, y):

    p1 = self.p[0]
    p2 = self.p[1]
    Weight_UnRellocated, Weight_Rellocated, Rat_Load, Records_Matrix, Veh_Pack_Distance = Prepare_Variables_Cost(self)

    Cost_Distance = p1*sum(np.multiply(x, Veh_Pack_Distance))

    # 车辆当前剩余载重： i*1
    # wl[i]: 车辆i剩余载重
    # wl[i]=l[i]-非分配包裹重量-运输中包裹重量
    # 非分配包裹重量【np.dot(x, Weight_UnRellocated)】
    # 运输中包裹重量【np.dot(Records_Matrix, Weight_Rellocated)】
    # i*1
    Available_Weight = np.zeros((self.Vehicle_Number, 1))
    Available_Weight = Rat_Load - \
        np.dot(x, Weight_UnRellocated.T) - \
        np.dot(Records_Matrix, Weight_Rellocated.T)

    # x: i*j, Available_Weight: i*1
    Weight_Veh_Pac = np.dot(x.T, Available_Weight)

    Cost_Weight = p2*sum(np.divide(Weight_Veh_Pac,
                                   Weight_UnRellocated.T))

    CostValue = Cost_Distance + Cost_Weight

    return CostValue

def Prepare_Variables_Value(self, x, y):

    # 各集中站点之间的最短路: k*k
    Shortest_Matrix = np.mat(self.Shortest_Matrix, dtype=float)

    # 配送记录: i*j 
    Records_Matrix = np.mat(self.Records, dtype=np.int)

    # 待分配包裹终点集合: 1*j 
    Dest_UnRellocated = [self.Dest_Pak[i] for i in self.UnRellocated_Order]

    # 运输中包裹终点集合: 1*j 
    Dest_Rellocated = [self.Dest_Pak[i]
                       for i in self.Transport_Order if i not in self.UnRellocated_Order]

    # 显示未分配包裹和运输中包裹是否驶到集中站点k的0-1矩阵: j*k
    Dest_UnRellocated_Matrix = np.zeros(
        (len(Dest_UnRellocated), self.Stop_Number), dtype=np.int)
    Dest_Rellocated_Matrix = np.zeros(
        (len(Dest_Rellocated), self.Stop_Number), dtype=np.int)

    for j in range(len(Dest_UnRellocated)):
        Dest_UnRellocated_Matrix[j][Dest_UnRellocated[j]] = 1

    for j in range(len(Dest_Rellocated)):
        Dest_Rellocated_Matrix[j][Dest_Rellocated[j]] = 1

    # j*k 
    Dest_UnRellocated_Matrix = np.mat(Dest_UnRellocated_Matrix, dtype=np.int)
    Dest_Rellocated_Matrix = np.mat(Dest_Rellocated_Matrix, dtype=np.int)

    # 待分配包裹最晚到达时间列表: 1*j 
    Latest_Time_UnRellocated = [self.Latest_Time[i] -
                                self.System_T for i in self.UnRellocated_Order]
    Latest_Time_UnRellocated = np.mat(Latest_Time_UnRellocated, dtype=float)

    return Shortest_Matrix, Records_Matrix, Dest_UnRellocated_Matrix, Dest_Rellocated_Matrix, Latest_Time_UnRellocated

def ValueF(self, x, y):

    c1 = self.c[0]
    c2 = self.c[1]

    Shortest_Matrix, Records_Matrix, Dest_UnRellocated_Matrix, Dest_Rellocated_Matrix, Latest_Time_UnRellocated = Prepare_Variables_Value(self, x, y)

    # 显示车辆i上搭载几个前往终点k的未分配包裹数量矩阵: i*k 
    Veh_UnRellocated_Number = np.dot(x, Dest_UnRellocated_Matrix)

    # 显示车辆i上搭载几个前往终点k的运输中包裹数量矩阵: i*k 
    Veh_Rellocated_Number = np.dot(Records_Matrix, Dest_Rellocated_Matrix)

    # 显示车辆i上搭载几个前往终点k的全部包裹数量: i*k 
    Veh_All_Number = Veh_Rellocated_Number + Veh_UnRellocated_Number

    # 显示与未分配包裹j同车的不同终点的包裹件数: j*k 
    Same_Veh_Dest = np.dot(x.T, Veh_All_Number)

    # 显示与j同车的全部件数； j*1
    Col_Pack_Dest_All = map(sum, Same_Veh_Dest)

    # 显示与未分配包裹j同车的同终点的包裹件数: j*k
    Same_Veh_Dest_Pack = np.multiply(Dest_UnRellocated_Matrix, Same_Veh_Dest)

    # 显示与j同车同终点的全部件数: j*1 
    Col_Pack_Dest_Same = map(sum, Same_Veh_Dest_Pack)

    # 显示同终点的占比
    Value_Dest = c1*sum(np.divide(Col_Pack_Dest_Same, Col_Pack_Dest_All))

    # 待分配包裹与下一步被分配站点的0-1矩阵关系: j*k
    Next_Stop = np.dot(x.T, y)

    # 待分配包裹j下一站站点与各终点之间的距离: j*k
    Next_Final_Dis = np.dot(Next_Stop, Shortest_Matrix)

    # 待分配包裹j下一站点与其终点之间的距离: j*k 
    Next_Final_Dis_Spe = np.multiply(Next_Final_Dis, Dest_UnRellocated_Matrix)
    Col_Next_Final_Dis = map(sum, Next_Final_Dis_Spe)

    Value_Time = c2 * \
        sum(np.subtract(Latest_Time_UnRellocated, Col_Next_Final_Dis))

    ApproximateValue = Value_Dest + Value_Time

    return ApproximateValue

def Objective_Function(AllDecision, args):
    self = args[0]

    # 决策变量: i*j 
    x = AllDecision[0:self.Vehicle_Number*len(self.UnRellocated_Order)]
    x = x.reshapre((self.Vehicle_Number, len(self.UnRellocated_Order)))
    x = np.mat(x, dtype=np.int)

    y = AllDecision[self.Vehicle_Number*len(self.UnRellocated_Order):]
    y = y.reshapre((self.Vehicle_Number, self.Stop_Number))
    y = np.mat(y, dtype=np.int)

    CostValue = CostF(self, x, y)

    ApprValue = ValueF(self, x, y)

    objectiveValue = CostValue + ApprValue
    return objectiveValue

def Weight_Cons(AllDecision, args):
    self = args[0]
    # 决策变量: i*j 
    x = AllDecision[0:self.Vehicle_Number*len(self.UnRellocated_Order)]
    x = x.reshapre((self.Vehicle_Number, len(self.UnRellocated_Order)))
    x = np.mat(x, dtype=np.int)

    # 配送记录: i*j 
    Records_Matrix = np.mat(self.Records, dtype=np.int)

    # l[i]: 车辆i额定载重【Rat_Load】: 1*i 
    Rat_Load = np.mat(self.Rat_Load, dtype=float)

    # 待分配包裹重量集合: 1*j 
    Weight_UnRellocated = [self.Weight_Pac[i] for i in self.UnRellocated_Order]
    Weight_UnRellocated = np.mat(Weight_UnRellocated, dtype=float)

    # 运输中包裹重量集合: 1*j 
    Weight_Rellocated = [self.Weight_Pac[i]
                         for i in self.Transport_Order if i not in self.UnRellocated_Order]
    Weight_Rellocated = np.mat(Weight_Rellocated, dtype=float)

    # 未分配包裹在各车辆上的重量: i*1 
    UnRellocated_Veh_Weight = np.dot(x, Weight_UnRellocated.T)

    # 运输中包裹在各车辆上的重量: i*1 
    Rellocated_Veh_Weight = np.dot(Records_Matrix, Weight_Rellocated.T)

    # 车辆上剩余空余重量: i*1 
    Remain_Weight = Rat_Load - UnRellocated_Veh_Weight - Rellocated_Veh_Weight

    # 找出超重车辆
    Remain_Weight = Remain_Weight[Remain_Weight<0]
    
    # 找出超重重量
    Remain_Weight = sum(abs(Remain_Weight))

    return Remain_Weight

def Pack_Cons(AllDecision, args):
    self = args[0]
    # 决策变量
    x = AllDecision[:self.Vehicle_Number*len(self.UnRellocated_Order)]
    x = x.reshapre((self.Vehicle_Number, len(self.UnRellocated_Order)))
    x = np.mat(x, dtype=np.int)

    # 按列求和
    X_Sum = map(sum, zip(*x))
    
    Ones = np.ones((1, self.Vehicle_Number), dtype=np.int)

    # 1*j
    PackAllocation = Ones - X_Sum

    # 找出不等于1的包裹（未分配包裹）
    PackAllocation = PackAllocation[PackAllocation != 1]
    PackAllocation = sum(abs(PackAllocation))
    return PackAllocation

def Veh_Cons(AllDecision, args):
    self = args[0]
    # 决策变量
    y = AllDecision[self.Vehicle_Number*len(self.UnRellocated_Order):]
    y = y.reshapre((self.Vehicle_Number, self.Stop_Number))
    y = np.mat(y, dtype=np.int)

    # 按行求和
    Y_Sum = map(sum, y)

    Ones = np.ones((self.Vehicle_Number, 1), dtype=np.int)

    # i*1
    VehAllocation = Ones-Y_Sum

    # 找出不等于1的车辆（未分配下一站点或多分配了）
    VehAllocation = VehAllocation[VehAllocation != 1]
    VehAllocation = sum(abs(VehAllocation))

    return VehAllocation

def Generate_DecisionVar(self):
    # Decision
    totalNum = self.Vehicle_Number*len(self.UnRellocated_Order) + self.Vehicle_Number*self.Stop_Number
    x0 = np.ones((totalNum, 1))
    AllDecision = np.array((np.zeros(totalNum),np.ones(totalNum))).T
    return x0, AllDecision

def Minimize_Main(self):
    x0, bnds = Generate_DecisionVar(self)
    WeighCons = {'type': 'ineq', 'fun': Weight_Cons, 'args': (self,)}
    PackAllCons = {'type': 'eq', 'fun': Pack_Cons, 'args': (self,)}
    VehAllCons = {'type': 'eq', 'fun': Veh_Cons, 'args': (self,)}
    cons = (WeighCons, PackAllCons, VehAllCons)

    sol = minimize(Objective_Function, x0, args=(self,), method='SLSQP', bounds=bnds, constraints=cons)
    return sol.x, sol.fun