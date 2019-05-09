from scipy.optimize import minimize
import numpy as np


def Prepare_Variables(x, y, Vehicle_Number, Shortest_Matrix, Cur_Loc_Veh, Cur_Loc_Pac, Rat_Load, Weight_Pac, Records, UnRellocated_Order, Transport_Order):
    # 决策变量
    x = np.mat(x, dtype=np.int)
    y = np.mat(y, dtype=np.int)

    # 生成车辆当前位置与包裹当前位置的距离矩阵
    # SH[i][j]: 车辆i与包裹j之间的距离【Cur_Loc_Veh[i], Cur_Loc_Pac[j]】
    Veh_Pack_Distance = np.zeros((len(UnRellocated_Order), Vehicle_Number), dtype=float)
    for i in range(Vehicle_Number):
        for j in range(len(UnRellocated_Order)):
            Veh_Pack_Distance[i][j] == Shortest_Matrix[Cur_Loc_Veh[i]
                                                       ][Cur_Loc_Pac[j]]
    Veh_Pack_Distance = np.mat(Veh_Pack_Distance, dtype=float)

    # l[i]: 车辆i额定载重【Rat_Load】
    Rat_Load = np.mat(Rat_Load, dtype=float)

    # 待分配包裹重量集合: j*1
    Weight_UnRellocated = [Weight_Pac[i] for i in UnRellocated_Order]
    Weight_UnRellocated = np.mat(Weight_UnRellocated, dtype=float)

    # 运输中包裹重量集合
    Weight_Rellocated = [Weight_Pac[i]
                         for i in Transport_Order if i not in UnRellocated_Order]
    Weight_Rellocated = np.mat(Weight_Rellocated, dtype=float)

    # 配送记录
    Records_Matrix = np.mat(Records, dtype=np.int)

    return x, y, Weight_UnRellocated, Weight_Rellocated, Rat_Load, Records_Matrix, Veh_Pack_Distance


def CostF(x, y, Vehicle_Number, Shortest_Matrix, Cur_Loc_Veh, Cur_Loc_Pac, Rat_Load, Weight_Pac, Records, UnRellocated_Order, Transport_Order):

    p1 = 3
    p2 = 5

    x, y, Weight_UnRellocated, Weight_Rellocated, Rat_Load, Records_Matrix, Veh_Pack_Distance = Prepare_Variables(
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

    Cost_Weight = p2*sum(np.divide(Weight_Veh_Pac,
                                     Weight_UnRellocated))

    CostValue = Cost_Distance + Cost_Weight

    return CostValue

def ValueF(x, y, Stop_Number, Vehicle_Number, Shortest_Matrix, Cur_Loc_Veh, Cur_Loc_Pac, Dest_Pak, Rat_Load, Weight_Pac, Records, UnRellocated_Order, Transport_Order):

    c1 = 1
    c2 = 2


    x = np.mat(x, dtype=np.int)
    y = np.mat(y, dtype=np.int)
    # 配送记录
    Records_Matrix = np.mat(Records, dtype=np.int)

    # 待分配包裹终点集合: j*1
    Dest_UnRellocated = [Dest_Pak[i] for i in UnRellocated_Order]

    # 运输中包裹终点集合
    Dest_Rellocated = [Dest_Pak[i]
                         for i in Transport_Order if i not in UnRellocated_Order]
    
    # 显示未分配包裹和运输中包裹是否驶到集中站点k的0-1矩阵
    Dest_UnRellocated_Matrix = np.zeros((len(Dest_UnRellocated), Stop_Number), dtype=np.int)
    Dest_Rellocated_Matrix = np.zeros((len(Dest_Rellocated), Stop_Number), dtype=np.int)

    for j in range(len(Dest_UnRellocated)):
        Dest_UnRellocated_Matrix[j][Dest_UnRellocated[j]] = 1
        
    for j in range(len(Dest_Rellocated)):
        Dest_Rellocated_Matrix[j][Dest_Rellocated[j]] = 1
    
    Dest_UnRellocated_Matrix = np.mat(Dest_UnRellocated_Matrix, dtype=np.int)
    Dest_Rellocated_Matrix = np.mat(Dest_Rellocated_Matrix, dtype=np.int)

    # 显示车辆i上搭载几个前往终点k的未分配包裹数量矩阵
    Veh_UnRellocated_Number = np.dot(x, Dest_UnRellocated_Matrix)
    
    # 显示车辆i上搭载几个前往终点k的运输中包裹数量矩阵
    Veh_Rellocated_Number = np.dot(Records_Matrix, Dest_Rellocated_Matrix)

    # 显示车辆i上搭载几个前往终点k的全部包裹数量
    Veh_All_Number = Veh_Rellocated_Number + Veh_UnRellocated_Number

    # 显示与未分配包裹j同车的不同终点的包裹件数
    Same_Veh_Dest = np.dot(x.T, Veh_All_Number)

    # 显示与j同车的全部件数
    Col_Pack_Dest_All = map(sum, Same_Veh_Dest)

    # 显示与未分配包裹j同车的同终点的包裹件数
    Same_Veh_Dest_Pack = np.multiply(x.T, Same_Veh_Dest)

    # 显示与j同车同终点的全部件数
    Col_Pack_Dest_Same = map(sum, Same_Veh_Dest_Pack)

    # 显示同终点的占比
    Value_Dest = c1*sum(np.divide(Same_Veh_Dest_Pack,Same_Veh_Dest))




    return ApproximateValue