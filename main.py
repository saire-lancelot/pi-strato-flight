#!/usr/bin/env python3

# PI STRATO FLIGHT
# IDPA (at) WKS
# Contributor: Alex Streit, Lars Wolf
# Licence: MIT License

# Module importieren
from sense_hat import SenseHat
import time    
import csv
import datetime

# Variablen editieren
sense = SenseHat()
sense.clear()
sense.set_imu_config(True, True, True)
sense.low_light = True

# CSV-Daten erstellen, bzw. öffnen und Zeilenüberschriften schreiben
with open('data.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Zeit','Temperatur1', 'Temperatur2', 'Temperatur3', 'Luftdruck', 'Luftfeuchtigkeit', 'Yaw', 'Pitch', 'Roll', 'Compass X', 'Compass Y', 'Compass Z', 'Gyro X', 'Gyro Y', 'Gyro Z'])

with open('acc.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Zeit','Acc_X','Acc_Y','Acc_Z'])

with open('log.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Zeit','Fehler'])

# Farben definieren
red = (255, 0, 0)
green = (0, 255, 0)
black = (0,0,0)

# Ermittelte Werte der Sensoren in die CSV-Datei schreiben
def writeDataToCsv(temperature, temperature2, temperature3, pressure, humidty, yaw, pitch, roll, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z):
    with open('data.csv', mode='a') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([datetime.datetime.now(),temperature, temperature2, temperature3, pressure, humidty, yaw, pitch, roll, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z])
        
def writeAccelerationToCsv(x,y,z):
    with open('acc.csv', mode='a') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([datetime.datetime.now(),x,y,z])
        sense.set_pixel(0, 0, green)
        time.sleep(.05)
        sense.set_pixel(0, 0, black)
    
def main():  
    sense.set_pixel(0, 0, black)
    counter = 0
    try:
        while True:
            # Beschleunigungswerte ermitteln
            acceleration = sense.get_accelerometer_raw()
            acc_x = acceleration['x']
            acc_y = acceleration['y']
            acc_z = acceleration['z']
            writeAccelerationToCsv(acc_x,acc_y,acc_z)
            time.sleep(.250)
            counter+=1
            
            
            if(counter == 4):                
                # Temperaturwerte ermitteln
                temperature = sense.get_temperature()
                temperature2 = sense.get_temperature_from_humidity()
                temperature3 = sense.get_temperature_from_pressure()
                
                # Luftdruck ermitteln 
                pressure = sense.get_pressure()
                humidty = sense.get_humidity()
                
                # Lagewerte ermitteln
                orientation = sense.get_orientation()
                yaw = orientation["yaw"]
                pitch = orientation["pitch"]
                roll = orientation["roll"]
                
                # Magnetometer auslesen
                mag = sense.get_compass_raw()
                mag_x = mag["x"]
                mag_y = mag["y"]
                mag_z = mag["z"]
                
                # Gyroskopsensor auslesen
                gyro = sense.get_gyroscope_raw()
                gyro_x = gyro["x"]
                gyro_y = gyro["y"]
                gyro_z = gyro["z"]
                
                # Variablen an die CSV-Datei übergeben
                writeDataToCsv(temperature, temperature2, temperature3, pressure, humidty, yaw, pitch, roll, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z)
                
                # Fehlerbehandlung definieren
                counter = 0;
    except Exception as e:
        with open('log.csv', mode='a') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([datetime.datetime.now(),str(e)])
            sense.set_pixel(1, 0, red)
    finally:
        pass
        main()
    
if __name__ == '__main__':
    main()
