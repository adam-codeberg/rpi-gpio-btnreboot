"""
Script that defects button press and duration.
Initiates reset or shutdown accordingly.

Requires 
pip install python-daemon

"""
import RPi.GPIO as GPIO
import time
from subprocess import call
from threading import Thread

class ButtonApp():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    def run(self):
        print('Listening for button_down')
        GPIO.add_event_detect(4, GPIO.RISING, callback=self.button_down, bouncetime=300)
        while True:
            time.sleep(0.1)

    def button_down(self, channel):
        buttonDown = time.time()

        while GPIO.input(channel) == True: 
            time.sleep(1)

        
        if GPIO.input(channel) == False:
            buttonUp = time.time() - buttonDown
            print('button up {}').format(buttonUp)
            self.button_up(buttonUp)

    def button_up(self, buttonUp):
        # buttonUp = time.time() - buttonDown

        if buttonUp < 3:
            print('System reboot initiated')
            call('reboot', shell=False)

        if buttonUp > 3:
            print('System shutdown initiated')
            call(['sudo', 'halt'], shell= False)

        GPIO.cleanup()

if __name__ == "__main__":
    print('Starting Script')
    app = ButtonApp()
    thread = Thread( target = app.run() )
    thread.start()
    thread.join()

