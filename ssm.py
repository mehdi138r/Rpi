# SEVEN SEGMENT MODULE . PYTHON
# SSM . PY
class ssm():
    def __init__(
                self, 
                pins: dict = 
                    {
                        "a" : None,
                        "b" : None,
                        "c" : None,
                        "d" : None,
                        "e" : None,
                        "f" : None,
                        "g" : None,
                        "pn" : None
                    },
                digit_pins: dict = 
                    {
                        "digit 1" : None,
                        "digit 2" : None,
                        "digit 3" : None,
                        "digit 4" : None
                    },
                common_cathod: bool = True,
                has_registor: bool = False,
                ):
        # import library
        import RPi.GPIO as gpio
        from time import sleep
        # create values
        self.sp = sleep
        self.gpio = gpio
        self.pins = pins
        self.digit_pins = digit_pins
        self.has_registor = has_registor
        self.digit_on = 0 if common_cathod else 1
        self.digit_off = 1 if common_cathod else 0
        self.float_sign = 65
        a, b, c, d, e, f, g, self.pn = self.pins[0], self.pins[1], self.pins[2], self.pins[3], self.pins[4], self.pins[5], self.pins[6], self.pins[7]
        self.digits = {
                0 : [a, b, c, d, e, f], 
                1 : [b, c], 
                2 : [a, b, g, e, d], 
                3 : [a, b, c, g, d], 
                4 : [f, g, b, c], 
                5 : [a, f, g, c, d], 
                6 : [a, f, e, d, c, g], 
                7 : [a, b, c], 
                8 : [a, b, c, d, e, f, g], 
                9 : [g, f, a, b, c, d]
            }
        # setup pins
        for pin in zip(self.pins, self.digit_pins): 
            try: self.gpio.setup(pin, gpio.OUT)
            except: pass
    def convert_to_number(
                            self, 
                            digit: int, 
                            number: str,
                        ):
        if digit == None:
            return False
        else:
            # turn on number digit
            self.gpio.output(digit, self.digit_on)
            # turn pn led on
            if number == self.float_sign and self.float_sign != 65: self.gpio.output(self.pn, self.digit_on)
            # turn on number leds (turn off more)
            for i in self.pins:
                if i in self.digits[int(number)]: self.gpio.output(i, self.digit_on)
                else: self.gpio.output(i, self.digit_off)
            self.sp(0.001)
            # turn off number digit
            self.gpio.output(digit, self.digit_off)
            # turn off all digit leds
            for i in self.pins: self.gpio.output(i, self.digit_off)
    def show_number(
                        self, 
                        number: str,
                        float: bool
                    ):
        if float:
            self.float_sign = number[number.find(".") - 1]
            number = number.replace(".", "")     # TODO TODO: CHECK THIS WHILE TESTING
        number_len = len(number) 
        if number_len == 4:
            self.convert_to_number(self.digit_pins["digit 4"], number[0])
            self.convert_to_number(self.digit_pins["digit 3"], number[1])
            self.convert_to_number(self.digit_pins["digit 2"], number[2])
            self.convert_to_number(self.digit_pins["digit 1"], number[3])
        elif number_len == 3:
            self.convert_to_number(self.digit_pins["digit 4"], 0)
            self.convert_to_number(self.digit_pins["digit 3"], number[0])
            self.convert_to_number(self.digit_pins["digit 2"], number[1])
            self.convert_to_number(self.digit_pins["digit 1"], number[2])
        elif number_len == 2:
            self.convert_to_number(self.digit_pins["digit 4"], 0)
            self.convert_to_number(self.digit_pins["digit 3"], 0)
            self.convert_to_number(self.digit_pins["digit 2"], number[0])
            self.convert_to_number(self.digit_pins["digit 1"], number[1])
        elif number_len == 1:
            self.convert_to_number(self.digit_pins["digit 4"], 0)
            self.convert_to_number(self.digit_pins["digit 3"], 0)
            self.convert_to_number(self.digit_pins["digit 2"], 0)
            self.convert_to_number(self.digit_pins["digit 1"], number[0])
