from scipy.optimize import minimize
import numpy as np


def Prepare_Variables(x, y, Vehicle_Number, Shortest_Matrix, Cur_Loc_Veh, Cur_Loc_Pac, Rat_Load, Weight_Pac, Records, UnRellocated_Order, Transport_Order):
    # 决策变量
    x = np.mat(x)
    y = np.mat(y)

    # 生成车辆当前位置与包裹当前位置的距离矩阵
    # SH[i][j]: 车辆i与包裹j之间的距离【Cur_Loc_Veh[i], Cur_Loc_Pac[j]】
    Veh_Pack_Distance = np.zeros((len(UnRellocated_Order), Vehicle_Number))
    for i in range(Vehicle_Number):
        for j in range(len(UnRellocated_Order)):
            Veh_Pack_Distance[i][j] == Shortest_Matrix[Cur_Loc_Veh[i]
                                                       ][Cur_Loc_Pac[j]]
    Veh_Pack_Distance = np.mat(Veh_Pack_Distance)

    # l[i]: 车辆i额定载重【Rat_Load】
    Rat_Load = np.mat(Rat_Load)

    # 待分配包裹重量集合: j*1
    Weight_UnRellocated = [Weight_Pac[i] for i in UnRellocated_Order]
    Weight_UnRellocated_Mines = [1/i for i in Weight_UnRellocated]
    Weight_UnRellocated = np.mat(Weight_UnRellocated)
    Weight_UnRellocated_Mines = np.mat(Weight_UnRellocated_Mines)

    # 运输中包裹重量集合
    Weight_Rellocated = [Weight_Pac[i]
                         for i in Transport_Order if i not in UnRellocated_Order]
    Weight_Rellocated = np.mat(Weight_Rellocated)

    # 配送记录
    Records_Matrix = np.mat(Records)

    return x, y, Weight_UnRellocated, Weight_Rellocated, Weight_UnRellocated_Mines, Rat_Load, Records_Matrix, Veh_Pack_Distance


def CostF(x, y, Vehicle_Number, Shortest_Matrix, Cur_Loc_Veh, Cur_Loc_Pac, Rat_Load, Weight_Pac, Records, UnRellocated_Order, Transport_Order):

    p1 = 3
    p2 = 5

    x, y, Weight_UnRellocated, Weight_Rellocated, Weight_UnRellocated_Mines, Rat_Load, Records_Matrix, Veh_Pack_Distance = Prepare_Variables(
        x, y, Vehicle_Number, Shortest_Matrix, Cur_Loc_Veh, Cur_Loc_Pac, Rat_Load, Weight_Pac, Records, UnRellocated_Order, Transport_Order)

    Cost_Distance = p1*sum(np.multiply(x, Veh_Pack_Distance))

    # 车辆当前剩余载重： i*1
    # wl[i]: 车辆i剩余载重
    # wl[i]=l[i]-非分配包裹重量-运输中包裹重量
    # 非分配包裹重量【np.dot(x, Weight_UnRellocated)】
    # 运输中包裹重量【np.dot(Records_Matrix, Weight_Rellocated)】
    # i*1
    Available_Weight = np.zeros((Vehicle_Number, 1))
    Available_Weight = Rat_Load - \
        np.dot(x, Weight_UnRellocated) - \
        np.dot(Records_Matrix, Weight_Rellocated)

    # x: i*j, Available_Weight: i*1
    Weight_Veh_Pac = np.dot(x.T, Available_Weight)

    Cost_Weight = p2*sum(np.multiply(Weight_Veh_Pac,
                                     Weight_UnRellocated_Mines))

    CostValue = Cost_Distance + Cost_Weight

    return CostValue

def ValueF(x, y, Vehicle_Number, Shortest_Matrix, Cur_Loc_Veh, Cur_Loc_Pac, Rat_Load, Weight_Pac, Records, UnRellocated_Order, Transport_Order):
    


    return ApproximateValue