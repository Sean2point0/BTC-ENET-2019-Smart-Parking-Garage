from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time

entranceLCD = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)

exitLCD = CharLCD(i2c_expander='PCF8574', address=0x26, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)
GPIO.setwarnings(False)

def exit():
    GPIO.setmode(GPIO.BOARD)

    MATRIX = [ ['1','2','3'],
               ['4','5','6'],
               ['7','8','9'],
               ['*','0','#'] ]

    ROW = [35,33,31,29]
    COL = [15,13,11]
    Number = ""
    exitLCD.clear()
    exitLCD.write_string('Confirmation #:')
    exitLCD.crlf()
    exitLCD.cursor_mode = "blink"

    for j in range(len(COL)):
        GPIO.setup(COL[j], GPIO.OUT)
        GPIO.output(COL[j], 1)

    for i in range(len(ROW)):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    try:
        while len(Number) < 8:
            for j in range(len(COL)):
                GPIO.output(COL[j], 0)

                for i in range(len(ROW)):
                    char = MATRIX[i][j]
                    if GPIO.input(ROW[i]) == 0 and char.isnumeric():
                        Number += char
                        exitLCD.write_string(char)
                        while GPIO.input(ROW[i]) == 0:
                            time.sleep(0.2)
                            pass

                GPIO.output(COL[j], 1)
        time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()
    return Number

def exitWrite(lineOne="", lineTwo=""):
    exitLCD.cursor_mode = "hide"
    exitLCD.clear()
    if lineOne or lineTwo:
        exitLCD.write_string(lineOne)
        exitLCD.crlf()
        exitLCD.write_string(lineTwo)

def entranceWrite(lineOne="", lineTwo=""):
    entranceLCD.clear()
    if lineOne or lineTwo:
        entranceLCD.write_string(lineOne)
        entranceLCD.crlf()
        entranceLCD.write_string(lineTwo)
