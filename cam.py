#!/usr/bin/env python3

# Module importieren
from picamera import PiCamera
from sense_hat import SenseHat
from time import sleep
import time
import datetime
import csv

# Farben definieren
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class VideoLogger(object):
    
    # Kameraparameter definieren
    def __init__(self):
        delimiter=';'
        quotechar='"'
        quoting=csv.QUOTE_MINIMAL
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)
        self.camera.framerate = 30        
        self.sense = SenseHat()
        log_headings = ['Zeit','Fehler']
        with open('video_log.csv', 'w') as file:
            writer = csv.writer(file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
            writer.writerow(log_headings)
        self.sense.set_pixel(6, 7, BLACK)
        self.sense.set_pixel(7, 7, BLACK)
        
    # Aufnahme als Datei schreiben
    def write_data_to_file(self, data, file_name, mode='a', delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL):
        with open(file_name, mode=mode) as file:
            writer = csv.writer(file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
            for row in data:
                writer.writerow(row)
        
    # Filmvorgang starten
    def start_filming(self):
        while True:
            self.camera.start_recording('/home/pi/pi-strato-flight/videos/video' + str(datetime.datetime.now()) + '.h264')
            self.sense.set_pixel(7, 7, GREEN)
            print('starting')
            self.camera.wait_recording(600)
            self.camera.stop_recording()
            self.sense.set_pixel(7, 7, BLACK)
            
    # Fehlerbehandlung definieren
    def log_exception(self, exception):
        print(str(exception))
        self.sense.set_pixel(6, 7, RED)
        row = []
        row.append([str(datetime.datetime.now()), str(exception)])
        self.write_data_to_file(row, 'video_log.csv')
            
        
if __name__ == '__main__':
    logger = VideoLogger()
    try:
        logger.start_filming()
    except Exception as e:
        logger.log_exception(e)
