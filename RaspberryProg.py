from lidar.MyLidarClass import MyLidar
from wifi_com.ServeurClass import Server

class Robot(Server):
    def __init__(self, LidarPort = '/dev/ttyUSB0'):
        super().__init__()
        self.lidar = MyLidar(LidarPort)
        self.run()
        
    def take_Lidar(self):
        data = self.lidar.getScanData(360, format=1)
        return data
    