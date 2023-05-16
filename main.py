import RPi.GPIO as GPIO
from stepper import Stepper
from gui import Gui
from temperature import Temperature
import time
from concurrent import futures

# Object initialization
stepper1 = Stepper(en=10, dr=9, pul=11)
stepper2 = Stepper(en=17, dr=27, pul=22)
interface = Gui()
temp = Temperature(peltier_pin = 26)


# Motor enabling
stepper1.disable_motor()
stepper2.disable_motor()

# An array that will store lambda functions for the butons.
sum_def = []
sub_def = []

# Changes the frequency of the PWM applied to the corresponding motor.
def sum_or_sub_frequency(stepper, meter, amount):
    if stepper == 0:
        stepper = stepper1
    if stepper == 1:
        stepper = stepper2
        
    stepper.change_frequency_by(amount)
    interface.meters[meter].configure(amountused=stepper.current_frequency)

def sum_or_sub_temp_max(a):
    temp.change_temp_max(a)
    interface.meters[2].configure(amountused=temp.temp_max)
    
        
def button_enable_motors():
    stepper1.enable_motor()
    stepper2.enable_motor()
    interface.switch()
    start_loop()
    #my_thread.submit(start_loop)

time_per_rev = 0
stepper2_one_rev_after = 0
def stepper2_one_rev():
#     stepper2.dir.start(100)
    global stepper2_one_rev_after
    global time_per_rev
    stepper2.start_motor()
    time_per_rev = int(stepper2.time_per_rev) * 1000
    stepper2_one_rev_after = interface.root.after(time_per_rev, stepper1_movement)


strides_done = 0
time_per_stride = 0
def stepper1_movement():
    global time_per_stride
    global strides_done
    steps_to_do = 1 # CHANGE THIS ACCORDING TO THE DIAMATER OF THE FILAMENT
    strides_before_back = 5 # CHANGE THIS ACCORDING TO THE WIDTH OF THE WHEEL
    stepper2.pwm.stop
    time_per_stride = int(steps_to_do * stepper1.time_per_step) * 1000
    
    
    
    if strides_done >= 0 and strides_before_back - 1:
        stepper1.do_step(steps_to_do)
        strides_done += 1
        
    elif strides_done >= 3 and strides_done <= stides_before_back*2 - 1:
        stepper1.do_step(-steps_to_do)
        strides_done += 1
    
    
    if strides_done > 5:
        strides_done = 0
    
  #  print(strides_done, stepper1.direction_state )    
    
    
    
    
    

     
start_loop_after = 0
peltier_activate = False

def start_loop():
    global peltier_activate
    global start_loop_after
    stepper2_one_rev()
    if isinstance(temp.read_temp(), float):
        sensor_read = temp.read_temp()
        if sensor_read > temp.temp_max and not peltier_activate:
            temp.peltier_enable()
            print("en ", sensor_read)
            peltier_activate = True
        elif sensor_read < temp.temp_max - 3 and peltier_activate:
            temp.peltier_disable()
            print("dn ", sensor_read)
            peltier_activate = False
           
        #print(sensor_read)
    interface.meters[3].configure(amountused = round(sensor_read,1))
        
    start_loop_after = interface.root.after(time_per_rev + time_per_stride, start_loop)
    # REMEMBER THAT THE TIME PER REVOLUTION CHANGES ACCORDING TO THE WHEEL'S RELATION
    
    
def button_disable_motors():
    interface.switch()
    stepper1.pwm.stop()
    stepper2.pwm.stop()
    interface.root.after_cancel(stepper2_one_rev_after)
    interface.root.after_cancel(start_loop_after)
    stepper1.disable_motor()
    stepper2.disable_motor()
    
    
# Assigns the command functions to each button.
for i in range(0, 2):
    interface.sum_buttons[i].configure(command = lambda stepper=i, meter=i, amount=1: sum_or_sub_frequency(stepper, meter, amount))
    interface.sub_buttons[i].configure(command = lambda stepper=i, meter=i, amount=-1: sum_or_sub_frequency(stepper, meter, amount))

interface.sum_buttons[2].configure(command = lambda a = 1 : sum_or_sub_temp_max(a))
interface.sub_buttons[2].configure(command = lambda a = -1 : sum_or_sub_temp_max(a))


interface.start_button.configure(command = button_enable_motors)
interface.stop_button.configure(command = button_disable_motors)

interface.root.mainloop()
GPIO.cleanup()