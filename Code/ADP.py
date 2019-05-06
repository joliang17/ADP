import numpy as np
import pandas as pd

class ADP_Algorithm:
    # 针对所有车辆和未被分配的订单
    # 通过学习优化算法，循环迭代更新参数

    # 提供参数
    # 车辆列表和属性
    # 订单列表和属性
    # 未被配送的订单列表和属性
    # 配送记录



    def __init__(self, VehicleID):
        # 初始化车辆集中站点为0
        self.ID = VehicleID
        self.Con_Weight = 20
        self.Cur_Location = [0,0]
        self.Nex_Location = -1
        self.Apr_Time = 0