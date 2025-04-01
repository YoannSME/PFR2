import serial
import time

try:
    bluetooth = serial.Serial(port="COM6", baudrate=9600, timeout=1)
    print(f"Port {bluetooth.port} ouvert avec succès.")
except serial.SerialException as e:
    print(f"Erreur lors de l'ouverture du port série : {e}")
    exit()

time.sleep(2)  # Attendre l'initialisation

bluetooth.write(b'TaDar')
time.sleep(1)

response = bluetooth.read_all()
print("Réponse du module HC-06 :")
print(response.decode())

bluetooth.close()
