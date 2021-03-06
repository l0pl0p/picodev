# This example takes the temperature from the Pico's onboard temperature sensor, and displays it on Pico Explorer, along with a little pixelly graph.
# It's based on the thermometer example in the "Getting Started with MicroPython on the Raspberry Pi Pico" book, which is a great read if you're a beginner!

import machine
import utime
import json
from dht import DHT11 # import DHT lib to allow sensor addressing

# Pico Explorer boilerplate
import picoexplorer as display
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)

# add pin reference for temp and humidity sensor
DHTPin = machine.Pin(2)
sensor = DHT11(DHTPin)

# reads from Pico's temp sensor and converts it into a more manageable number
#sensor_temp = machine.ADC(4)
#conversion_factor = 3.3 / (65535)

i = 0

while True:
    # the following two lines do some maths to convert the number from the temp sensor into fahrenheit
    #reading = sensor_temp.read_u16() * conversion_factor
    #temperature = round(((27 - (reading - 0.706) / 0.001721) * 9/5) + 32)
    sensor.measure()
    temperature = round((sensor.temperature() * 9/5) + 32)
    humidity = round(sensor.humidity())

    # test temp for display tuning
    # temperature = 100
    
    # this if statement clears the display once the graph reaches the right hand side of the display
    if i >= (width + 1):
        i = 0
        display.set_pen(0, 0, 0)
        display.clear()

    # chooses a pen colour based on the temperature
    display.set_pen(0, 255, 0)
    if temperature > 68:
        display.set_pen(255, 0, 0)
    if temperature < 55:
        display.set_pen(0, 0, 255)

    # draws the reading as a tall, thin rectangle
    display.rectangle(i, height - (temperature * 2), 6, height)

    # draws a white background for the text
    display.set_pen(255, 255, 255)
    display.rectangle(1, 1, 65, 33)

    # writes the reading as text in the white rectangle
    display.set_pen(0, 0, 0)
    display.text("{:.0f}".format(temperature) + "f", 3, 3, 0, 4)

    #writes humidity reading
    display.set_pen(255, 0, 0)
    display.text("{:.0f}".format(humidity) + "%", 75, 3, 0, 4)
    
    # time to update the display
    display.update()
    
    #write the data to the json datalog
    #with open('datalog.json') as f:
    #    f.write(json.dumps(str(utime.localtime()) + "," + str(temperature) + "," + str(humidity) + "\n"))

    datalog = open("datalog.csv", "a")
    datalog.write(str(utime.localtime()) + "," + str(temperature) + "," + str(humidity) + "\n")
    datalog.close()

    # waits for 30 seconds
    utime.sleep(30)

    # the next tall thin rectangle needs to be drawn 6 pixels to the right of the last one
    i += 6