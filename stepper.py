import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import time

class Stepper:
    def __init__(self, en, dr, pul, step_count=200):
        # Pin Variables
        self.step_count = step_count
        self.enable_pin = en
        self.direction_pin = dr
        self.pulse_pin = pul

        # GPIO setup
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.pulse_pin, GPIO.OUT)
            
        # PWM Setup    
        self.pwm = GPIO.PWM(self.pulse_pin, 1)
        self.dir = GPIO.PWM(self.direction_pin, 1)
        self.dir.start(100)
        self.en = GPIO.PWM(self.enable_pin, 1)
        self.en.start(100)
        
        
        # Status variables
        self.direction_state = True
        self.current_frequency = 100 # Hz
        self.time_per_rev = self.step_count / self.current_frequency # Seconds   
        self.time_per_step = self.time_per_rev / self.step_count # Seconds
        self.step_position = 0 # Not implemented yet
        self.is_enabled = False
        
        
    def change_frequency_by(self, amount):
        # Frequency can't be negative.
        if amount <= 0 and self.current_frequency <= 0:
            return
        
        # Changes the frequency
        self.pwm.ChangeFrequency(self.current_frequency + amount)
        
        # Update status values
        self.current_frequency += amount
        self.time_per_rev = self.step_count / self.current_frequency
        self.time_per_step = self.time_per_rev / self.step_count
        
    def change_frequency(self, hz):
        if hz <= 0:
            return
        
        self.pwm.ChangeFrequency(hz)
        
        # Updates
        self.current_frequency = hz
        self.time_per_rev = self.step_count / self.current_frequency
        self.time_per_step = self.time_per_rev / self.step_count        
    
    def disable_motor(self):
        self.en.start(100)
        self.is_enabled = False
        time.sleep(0.2)
    
    
    def enable_motor(self):
        self.en.stop()
        self.is_enabled = True
        time.sleep(0.2)
          
 
    def change_dir(self, dr):
        if dr:
            self.dir.ChangeDutyCycle(100)
            self.direction_state = True
        else:
            self.dir.ChangeDutyCycle(0)
            self.direction_state = False
            
    def invert_dir(self):
        if self.direction_state:
            self.dir.stop()
            self.direction_state = False
        if self.direction_state == False:
            self.dir.start(100)
            self.direction_state = True
    def start_motor(self):
        self.pwm.start(50)
        self.change_frequency(self.current_frequency)
        
        
    # DO THIS    
    def do_step(self, steps):
        if steps < 0:
            reverse = True
        else:
            reverse = False
        self.change_frequency(self.current_frequency)
        
        if self.step_position + steps > self.step_count:
            self.step_position = self.step_position + steps - self.step_count
        else:
            self.step_position += steps
            
#         print(self.step_position)
        
        self.pwm.start(50)
        
        start_time = time.time()
        
        if reverse:
            end_time = start_time + (self.time_per_step * steps * -1)
        else:    
            end_time = start_time + ( self.time_per_step * steps )
#         print(start_time, end_time)
        self.change_dir(reverse)
        while True:
                
            current_time = time.time()
            if current_time >= end_time:
                self.pwm.stop()
                return
            

# test = Stepper(en=17, dr=27, pul=22)
# test.enable_motor()
# test.change_frequency(100)
# while True:
#     test.do_step(-50)
#     time.sleep(.5)
#     test.do_step(50)
#     time.sleep(0.5)
# # test.pwm.start(50)


        