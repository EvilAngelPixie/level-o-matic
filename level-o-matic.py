import RPi.GPIO as GPIO
from time import sleep
import os
import serial

# Dev settings
sensor_on = False
verbose = True

# Button pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)

# Initialise values
value_zero = 0.00
value_init = 0.00
change_percent = 0.00
level = 0.00
level_reached = 0
ready = False

# Initialise button states
button_zero = 0
button_perc = 0
button_init = 0
button_read = 0

# Initialise alerts
alerting = False
alert_min = 5 #mm
alert_high = 0.00
alert_low = 0

# Connect bluetooth
if(sensor_on):
  bluetooth = serial.Serial( "/dev/rfcomm0", baudrate=9600 )

while True:
  
  try:
    # Read sensor data
    if(sensor_on):
      if(bluetooth.inWaiting() > 0):
        sensor_data = bluetooth.readline()
        sensor_data = float(sensor_data) / 100
        if(verbose):
          print "Received: " + str(sensor_data)
        # set level
        level = sensor_data
                         
    if ((not button_zero) and GPIO.input(14)):
      #Verify 0
      value_init = 0
      value_alert = 0
      alerting = False
      os.system('flite -voice awb -t "Zeroing level. Ready to cook"')
      if(verbose):
        print("Zeroing level & alerts")

    # Set initial liquid level
    if ((not button_init) and GPIO.input(23)):
      if(not ready):
        #Read value and store
        ready = True
        value_init = level
        os.system('flite -voice awb -t "Initial liquid level is %.0f millimeters"' % value_init)
        if(verbose):
          print("Initial liquid level is %.0f millimeters" % value_init)
      else:
        ready = False
        alerting = True
        value_alert = value_init/100 * change_percent
        os.system('flite -voice awb -t "Alert set for %.0f millimeter change"' % alert_value)
        if(verbose):
          print("Alert set for %.0f millimeter change" % value_alert)

    # Set percentage change 
    if ((not button_perc) and GPIO.input(24)):
      #Store % change and speak %
      if(change_percent < 100):
        change_percent += 5
      else:
        change_percent = 0

      if(verbose):
        print("Value change set: %.0f percent" % change_percent)
    
      os.system('flite -voice awb -t "%.0f percent change"' % change_percent)
      
    # Button read
    if ((not button_read) and GPIO.input(15)):
      #Read out 
      os.system('flite -voice awb -t "Current level is %.0f millimeters"' % level)
      if(verbose):
        print("Current level: %.0f millimeters" % level)

    # Test level condition
    if(alerting):
      #print("Alert value is: %" (value_alert))
      alert_high = value_alert + value_init
      alert_low = value_init - value_alert
      
      if((level >= alert_high) or (level <= alert_low)):
          if(level_reached < 5):
            level_reached += 1
          else:
            level_reached = 0
            os.system('flite -voice awb -t "Level reached %.0f percent change"' % level)
            if(verbose):
                print("Level reached %.0f percent change" % level)
                
    if((level <= alert_min) and (level > 0)):
      if(level_reached < 5):
        level_reached += 1
      else:
        level_reached = 0
        os.system('flite -voice awb -t "WARNING Minimum level reached %.0f remaining"' % level)
        if(verbose):
          print("WARNING Minimum level reached %.0f mm remaining" % level)        
    
    sleep(0.3);
    #0.1

  except KeyboardInterrupt:
    GPIO.cleanup()
    exit()
  
