from numba import jit

class Package:

    def __init__(self, PackageID): 
        self.Latest_Time = -1
        self.Destination = -1
        self.Pack_Weight = 1
        self.Cur_Origins = -1
        self.Cur_State = 0

    def Generate_Package(self, Origins, Destination, Latest_Time):
        self.Latest_Time = Latest_Time
        self.Destination = Destination
        self.Cur_Origins = Origins
        return

    # 车辆到站，卸货
    def Update_Package_BeforeD(self, Cur_Origins, Cur_State):
        self.Cur_Origins = Cur_Origins
        self.Cur_State = Cur_State
        return

    # 上车
    def Update_Package_AfterD(self, Cur_State):
        self.Cur_State = Cur_State
        return

