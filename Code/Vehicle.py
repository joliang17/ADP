from numba import jit

class Vehicle:

    def __init__(self, VehicleID):
        # 初始化车辆集中站点为0
        self.ID = VehicleID
        self.Con_Weight = 20
        self.Cur_Location = [0,0]
        self.Nex_Location = -1
        self.Apr_Time = 0

    def Update_Vehicle(self, Cur_Location, Nex_Location, Apr_Time):
        self.Cur_Location = Cur_Location
        self.Nex_Location = Nex_Location
        self.Apr_Time = Apr_Time

