import numpy as np
import pandas as pd

class ADP_Algorithm:
    # 针对所有车辆和未被分配的订单
    # 通过学习优化算法，循环迭代更新参数

    # 提供参数
    # 车辆当前位置（下一站点位置e[1]）、距离下一站点距离、额定载重
    # 所有正在运输中的订单最晚要求到达时间、终点、包裹重量
    # 未被配送的订单编号
    # 配送记录

    def __init__(self, Vehicle_Set, Package_Set, Vehicle_Number, UnRellocated_Order, Transport_Order, Records):
        self.Vehicle_Set = Vehicle_Set
        self.Package_Set = Package_Set
        self.Vehicle_Number = Vehicle_Number
        self.UnRellocated_Order = UnRellocated_Order
        self.Transport_Order = Transport_Order
        self.Records = Records

    def Decision_Prepare(self):
        Vehicle_Weight=[]
        for i in range(self.Vehicle_Number):
            Vehicle_Weight.append(self.Vehicle_Set[str(i)].Con_Weight)
        
        Package_Weight=[]
        Package_Destination = []
        Package_LastTime = []
        for i in range(len(self.Transport_Order)):
            Order_Index = self.Transport_Order[i]
            Package_Weight.append(self.Package_Set[str(Order_Index)].Pack_Weight)
            Package_Destination.append(self.Package_Set[str(Order_Index)].Destination)
            Package_LastTime.append(self.Package_Set[str(Order_Index)].Latest_Time)
        
        Records_Transport = np.array(self.Records)
        

        return Vehicle_Weight