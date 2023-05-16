import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import os
import glob
import time
 
class Temperature:
    def __init__(self, peltier_pin) -> None:
        # Read de file one-wire microcontroller
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'
        self.temp_max = 30
        self.peltier_pin = peltier_pin
        GPIO.setup(self.peltier_pin, GPIO.OUT, initial = GPIO.LOW)
        self.peltier_pwm = GPIO.PWM(self.peltier_pin,1)
        self.peltier_ison = False

    def read_temp_raw(self):
        file = open(self.device_file, 'r')
        lines = file.readlines()
        file.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
        return temp_c

    def change_temp_max(self, cantidad):
        self.temp_max += cantidad

    def peltier_enable(self):
        self.peltier_pwm.start(100)
        self.peltier_ison = True
        print("Enable")
        
    def peltier_disable(self):
        self.peltier_pwm.stop()
        self.peltier_ison = False
        print("Disable")
    
# test = Temperature()
# 
# while True:
#      print(test.read_temp())
#      print(type(test.read_temp())
#      time.sleep(0.3)
