from numba import jit

import numpy as np

from Code.Vehicle import Vehicle
from Code.Order import Package
from Code.Network import Network

# 先生成部分订单，根据现有订单进行规划
# 在下一个时间点，在不同集中站点随机生成部分订单
@jit(nopython=True)
def Main_Func(Stop_Number, Graph, T_System, T_Event, Vehicle_Number, Vehicle_Set, Package_Set):
    Event_T = 0
    OrderID_Last = -1
    UnRellocated_Order = []
    Arrival_List = []
    NewOrder_Status = 0
    NewVehicle_Status = 0
    for System_T in range(T_System):

        # 依据某一随机分布，在各集中站点生成订单
        OrderID_New, UnRellocated_Order = Generate_Order_Step(System_T, OrderID_Last, Package_Set, UnRellocated_Order, Stop_Number, T_System)

        if(OrderID_New == OrderID_Last):
            # 无新订单出现
            NewOrder_Status = 0
        else:
            NewOrder_Status = 1
            # 更新状态矩阵
            Record_new = np.zeros([Stop_Number, OrderID_Last-OrderID_New])
            Records = np.hstack((Records, Record_new))
            OrderID_Last = OrderID_New

        # 判定是否有车辆到达站点
        Arrival_List = Check_Vehicle_Status(System_T, Arrival_List, Vehicle_Number, Vehicle_Set)

        if(len(Arrival_List) == 0):
            # 无车辆到站
            NewVehicle_Status = 0
        else:
            NewVehicle_Status = 1
            # 对于已到站点的车，搭载的包裹全部卸下（包裹当前起始点发生变化、当前状态由1换为0）、配送记录发生变化
            UnRellocated_Order = Find_Package_Vehicle(System_T, Arrival_List, UnRellocated_Order, Records, Vehicle_Set, Package_Set)

        # 问题：有新包裹出现，但是没有车辆出现？
        # 等待车辆出现（保持unRellocated状态不变）

        if(NewVehicle_Status == 1):
            # 有车靠站

            # 针对未分配包裹list（UnRellocated_Order）和已到站点车辆（Arrival_List），进行ADP规划
            # 获取x[i][j], y[i][N]

            # ADP算法


            # 根据获取的决策变量，更新Vehicle, Order, Records
            # x[i][j]: 更新R, f
            # y[i][N]: 更新v

            x = [[]]
            y = [[]]
            Update_State(x, y, Arrival_List, Vehicle_Set, UnRellocated_Order, Package_Set, Records, Stop_Number, Graph, System_T)

            # 推进事件时间点
            Event_T += 1
        else:
            pass

        # 推进时间System_T
        System_T += 1

        if(Event_T >= T_Event):
            break
    return

# 根据决策向量更新状态(更新当前记录R, 订单状态f, 下一站点，预计到达时间，当前位置)
# 如果是车辆从其他集中站点过来接包裹呢?
@jit(nopython=True)
def Update_State(x, y, Arrival_List, Vehicle_Set, UnRellocated_Order, Package_Set, Records, Stop_Number, Graph, System_T):
    # 更新剩余载重

    for i in Arrival_List:
        for j in UnRellocated_Order:
            if(x[i][j]==1):
                # 因为只能分配同站点包裹与车辆，因此如果x变量为分配，则这一时间点，包裹必上车
                # 将包裹分配给车辆
                Records[i][j]=1

                # 包裹正在进行配送
                Package_Set[str(j)].Update_Package_AfterD(1)
                # 包裹从未分配中删除
                UnRellocated_Order.remove(j)

        for stop in range(Stop_Number):
            if(y[i][stop]==1):
                # 车辆状态改变
                # 车辆当前位置
                Cur_Location = Vehicle_Set[str(i)].Cur_Location[0]
                Cur_Location = [Cur_Location, stop]
                # 预计抵达时间
                Apr_Time = Graph.Graph[Cur_Location[0]][Cur_Location[1]]
                Vehicle_Set[str(i)].Update_Vehicle(Cur_Location, stop, System_T + Apr_Time)

                # 车辆从已到站点的list中删除
                Arrival_List.remove(i)
        
    return

# 依据当前系统时间生成各站点订单
@jit(nopython=True)
def Generate_Order_Step(System_T, OrderID_Last, Package_Set, UnRellocated_Order, Stop_Number, T_System):
    Stop_Basic = np.random.rand(Stop_Number)
    # 定义各站点出现包裹的随机分布（当前是否有包裹、包裹数量、包裹目的地、包裹要求到达时间）
    # 假设都为均匀分布
    # 一次至多出现5个包裹
    Max_Appear = 5
    for i in range(Stop_Number):
        if(Stop_Basic[i]>=0.8):
            # 有包裹出现
            Order_Num = np.random.randint(1, Max_Appear)
            for j in range(Order_Num):
                # 生成包裹目的地
                Destination = np.random.randint(Stop_Number)
                while Destination==i:
                    Destination = np.random.randint(Stop_Number)
                
                # 生成要求到达时间
                Last_Time = np.random.randint(System_T+1, T_System)

                # 创建包裹
                OrderID_Last = OrderID_Last + 1
                Package_Set[str(OrderID_Last)]=Package(OrderID_Last)
                Package_Set[str(OrderID_Last)].Generate_Package(i, Destination, Last_Time)

                # 将未分配包裹加入list
                UnRellocated_Order.append(OrderID_Last)
    return OrderID_Last, UnRellocated_Order

# 判断是否有车辆到达站点
@jit(nopython=True)
def Check_Vehicle_Status(System_T, Arrival_List, Vehicle_Number, Vehicle_Set):
    for i in range(Vehicle_Number):
        Arrival_Time = Vehicle_Set[str(i)].Apr_Time
        # 如果抵达站点的时间为当前系统时间(新到达车辆)
        if(Arrival_Time == System_T):
            # 记录到站点的车
            Arrival_List.append(i)
            # 更改车的属性（当前位置、下一抵达站点、下一抵达站点的时间）
            Cur_Location = Vehicle_Set[str(i)].Cur_Location[1]
            Cur_Location = np.ones(2)*Cur_Location
            Nex_Location = -1
            Apr_Time = 0
            Vehicle_Set[str(i)].Update_Vehicle(Cur_Location, Nex_Location, Apr_Time)

    return Arrival_List

# 找到每辆已到站点的车搭载的包裹
@jit(nopython=True)
def Find_Package_Vehicle(System_T, Arrival_List, UnRellocated_Order, Records, Vehicle_Set, Package_Set):
    # 需要找到车辆i搭载的全部包裹j
    for i in Arrival_List:
        # 取出第i辆车的行数据
        Records_I = Records[[i]]
        OrderList_I = np.flatnonzero(Records_I)
        for j in OrderList_I:
            # 包裹当前起始点发生变化、当前状态由1换为0、配送记录发生变化

            # 包裹当前起始点更新
            # 判断是否已到配送终点
            Cur_Origins = Vehicle_Set[str(i)].Cur_Location[0]
            # 包裹未到终点
            if(Package_Set[str(j)].Destination != Cur_Origins):
                # 当前状态发生变化
                Cur_State = 0
                Package_Set[str(j)].Update_Package_BeforeD(Cur_Origins, Cur_State)
                # 更新未分配list
                UnRellocated_Order.append(j)
            # 包裹已到终点
            else:
                # 当前状态发生变化
                Cur_State = 2
                Package_Set[str(j)].Update_Package_BeforeD(Cur_Origins, Cur_State)

            # 配送记录发生变化
            Records[i][j] = 0

    return UnRellocated_Order

if __name__ == "__main__":
    
    # 定义站点数量
    Stop_Number = 6
    Density = 0.5
    # 生成物流网络
    Graph = Network(Stop_Number)
    Graph.Generate_Graph(Density)
    Shortest_Path = Graph.Gain_Shortest_Path(Stop_Number)

    # 定义车辆数量
    Vehicle_Number = 15
    Vehicle_Set = locals()
    for i in range(Vehicle_Number):
        Vehicle_Set[str(i)] = Vehicle(i)

    # 定义订单
    Package_Set = locals()

    # 定义配送状态记录
    Records = np.zeros([Stop_Number, 0])

    # 定义系统时间点
    T_System = 50
    # 定义事件时间点
    T_Event = 30

    Main_Func(Stop_Number, Graph, T_System, T_Event, Vehicle_Number, Vehicle_Set, Package_Set)
    