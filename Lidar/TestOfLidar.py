from CartographieClass import Cartographie
from MyLidarClass import MyLidar

import matplotlib.pyplot as plt

#Use of Mylidar

cartographie = Cartographie()
myLidar = MyLidar("COM6")
for i in range(10000):
    # input("Appuyez sur Entrée pour continuer...")  # Attend un appui sur Entrée
    cartographie.update_carte(myLidar.getScanData(200, format=1),ploting=True)
