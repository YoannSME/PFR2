from CartographieClass import Cartographie

import matplotlib.pyplot as plt

#Use of Mylidar

carte = Cartographie(500, LidarPort = '/dev/ttyUSB0')

for i in range(10000):
    # input("Appuyez sur Entrée pour continuer...")  # Attend un appui sur Entrée
    carte.update_carte(ploting=False)

plt.scatter(carte.carte[:, 0], carte.carte[:, 1], color='black')
plt.show()
