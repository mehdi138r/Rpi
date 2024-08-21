import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
def ssm(a, b, c, d, e, f, g, number, digit1 = None, digit2 = None, digit3 = None, digit4 = None):
    segments = [a,b,c,d,e,f,g]
    digits = {0:[a, b, c, d, e, f],
            1:[b, c] ,
            2:[a, b, g, e, d] ,
            3:[a, b, c, g, d] ,
            4:[f, g, b, c] ,
            5:[a, f, g, c, d] ,
            6:[a, f, e, d, c, g] ,
            7:[a, b, c] ,
            8:[a, b, c, d, e, f, g] ,
            9:[g, f, a, b, c, d]}
    val = len(number)
    if digit1 != None:
        gpio.setup(digit1, gpio.OUT)
    if digit1 != None:    
        gpio.setup(digit2, gpio.OUT)
    if digit1 != None:
        gpio.setup(digit3, gpio.OUT)
    if digit1 != None:      
        gpio.setup(digit4, gpio.OUT)
    gpio.setup(a, gpio.OUT)
    gpio.setup(b, gpio.OUT)
    gpio.setup(c, gpio.OUT)
    gpio.setup(d, gpio.OUT)
    gpio.setup(e, gpio.OUT)
    gpio.setup(f, gpio.OUT)
    gpio.setup(g, gpio.OUT)
    def convert_to_number(digit, number):
        gpio.output(digit, 1)
        for j in segments:
            if j in digits[number]:
                gpio.output(j, 0)
            else:
                gpio.output(j, 1)
        time.sleep(0.01)
        gpio.output(digit, 0)
    if val == 4 :
        convert_to_number(digit1, number[0])
        convert_to_number(digit2, number[1])
        convert_to_number(digit3, number[2])
        convert_to_number(digit4, number[3])
    if val == 3 :
        convert_to_number(digit1, 0)
        convert_to_number(digit2, number[0])
        convert_to_number(digit3, number[1])
        convert_to_number(digit4, number[2])
    if val == 2 :
        convert_to_number(digit1, 0)
        convert_to_number(digit2, 0)
        convert_to_number(digit3, number[0])
        convert_to_number(digit4, number[1])   
    if val == 1 :
        convert_to_number(digit1, 0)
        convert_to_number(digit2, 0)
        convert_to_number(digit3, 0)
        convert_to_number(digit4, number[0])       
    
