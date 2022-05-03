# losernator
# License-Identifier: MIT
# 2022/05/03
import time
import board
import digitalio
import analogio
import usb_hid
import neopixel
from hid_gamepad import Gamepad
from rainbowio import colorwheel
from configs import config

gp = Gamepad(usb_hid.devices)

# Buttons
turbo_speed = config.get('turbo_speed')
turbo_status = []
button_pins = []
gamepad_buttons = []
button_leds = []
# 1:A, 2:B, 3:RB, 4:X, 5:Y, 6:LB, 7:LT, 8:RT, 9:L2, 10:R2, 11:SELECT, 12:START, 13:EX1, 14:THUMBL, 15:THUMBR, 16:EX2
# button_keys = ['A', 'B', 'RB', 'X', 'Y', 'LB', 'LT', 'RT', 'L3', 'R3', 'SELECT', 'START', 'PS', 'TP', 'EX1', 'EX2']
# D-Input layout for tekknen
button_keys = ['X', 'A', 'B', 'Y', 'LB', 'RB', 'LT', 'RT', 'SELECT', 'START', 'L3', 'R3', 'PS', 'TP', 'EX1', 'EX2']
for i, button in enumerate(button_keys):
    if config.get(button):
        button_pins.append(config.get(button))
        gamepad_buttons.append(i+1)
        turbo_status.append(0)
        button_leds.append(config.get(button+'_led', -1))

isMode = False
isTurbo = False
if config.get('MODE'):
    mode = digitalio.DigitalInOut(config.get('MODE'))
    mode.direction = digitalio.Direction.INPUT
    mode.pull = digitalio.Pull.UP
    isMode = True
if config.get('TURBO'):
    turbo = digitalio.DigitalInOut(config.get('TURBO'))
    turbo.direction = digitalio.Direction.INPUT
    turbo.pull = digitalio.Pull.UP
    isTurbo = True

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

# Joystick lever
dpad_mode = config.get('dpad_mode')
dpad_axis = [ 0, 254, 0, 254 ]
hatposition = {
    "":8,
    "UP":0,
    "DOWN":4,
    "LEFT":6,
    "RIGHT":2,
    "UPLEFT":7,
    "UPRIGHT":1,
    "DOWNLEFT":5,
    "DOWNRIGHT":3,
    "UPDOWN":8,
    "UPDOWNLEFT":6,
    "UPDOWNRIGHT":2,
    "UPDOWNLEFTRIGHT":2,
    "LEFTRIGHT":8,
    "DOWNLEFTRIGHT":4,
    "UPLEFTRIGHT":0,
}
dpad_pins = []
dpad_leds = []
dpad_all = []
dpad_keys = ['UP', 'DOWN', 'LEFT', 'RIGHT']
for i, dpad in enumerate(dpad_keys):
    if config.get(dpad):
        dpad_pins.append(config.get(dpad))
        dpad_all.append(dpad)
        dpad_leds.append(config.get(dpad+'_led', -1))
dpads = [digitalio.DigitalInOut(pin) for pin in dpad_pins]
for dpad in dpads:
    dpad.direction = digitalio.Direction.INPUT
    dpad.pull = digitalio.Pull.UP
#Analog axis
if config.get('AnalogX'):
    ax = analogio.AnalogIn(config.get('AnalogX'))
    ay = analogio.AnalogIn(config.get('AnalogY'))
    isAnalog = True
else:
    isAnalog = False

#NeoPixel
if config.get('neopixel_pin'):
    default_color = config.get('default_color')
    led_color = config.get('led_color')
    num_pixels = max([max(button_leds),max(dpad_leds)])+1
    if len(led_color) < num_pixels:
        for i in range (num_pixels - len(led_color)):
            led_color.append(default_color)
    pixels = neopixel.NeoPixel(config.get('neopixel_pin'), num_pixels, auto_write=False)
    pixels.brightness = config.get('led_brightness')
    fadingstep = config.get('fadingstep')
    activetime = config.get('activetime')
    Neopixel = True
else :
    Neopixel = False

def rainbow(speed):
    ebreak = False
    while True:
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = colorwheel(pixel_index & 255)
            for i, button in enumerate(buttons):
                if not button.value:
                    ebreak = True
                    break
            for i, hat in enumerate(dpads):
                if not hat.value:
                    ebreak = True
                    break
            if isAnalog:
                if not analog_check(ax.value) == 127 or not analog_check(ay.value) == 127 :
                    ebreak = True
                    break
            if (ebreak):
                break
            pixels.show()
            time.sleep(speed)
        if (ebreak):
            break

def colorchase(color, speed):
    ebreak = False
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(speed)
        pixels.show()
        for i, button in enumerate(buttons):
            if not button.value:
                ebreak = True
                break
        for i, hat in enumerate(dpads):
            if not hat.value:
                ebreak = True
                break
        if (ebreak):
            break
    time.sleep(0.5)

def pixelfading(index):
    if pixels[index][0]+pixels[index][1]+pixels[index][2] > 0:
        pixels[index]=(max([pixels[index][0] - pixels[index][0]/255 * fadingstep,0]), max([pixels[index][1] - pixels[index][1]/255 * fadingstep,0]), max([pixels[index][2] - pixels[index][2]/255 * fadingstep,0]))

def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
def analog_dz(x, dz):
    if abs(x-127) < dz:
        x = 127
    return x
def analog_check(x):
    x = analog_dz(range_map(x, 0, 65535, 0, 254),10)
    return x
def analog_hat(x,y):
    x = analog_dz(range_map(x, 0, 65535, 0, 254),10)
    y = analog_dz(range_map(y, 0, 65535, 0, 254),10)
    hatx = ""
    haty = ""
    if x < 127:
        hatx = "LEFT"
    elif x > 127:
        hatx = "RIGHT"
    if y < 127:
        haty = "UP"
    elif y > 127:
        haty = "DOWN"
    return haty+hatx

current_time = time.monotonic()
lastshot_time = time.monotonic()
button_toggle = True
last_turbo = None
last_mode = None
while True:
    if Neopixel:
        if time.monotonic() - current_time > activetime:
            rainbow(0.003)
    #mode setting
    if isMode and mode.value != last_mode:
        last_mode = mode.value
        if not last_mode:
            dpad_mode = "hat" if dpad_mode == "axis" else "axis"

    # Button pressed value = False
    for i, button in enumerate(buttons):
        button_num = gamepad_buttons[i]
        if not button.value:
            #check turbo status
            if isTurbo and turbo_status[i] == 1:
                if current_time - lastshot_time > turbo_speed:
                    button_toggle = True if button_toggle == False else False
                    lastshot_time = time.monotonic()
                if button_toggle:
                    gp.release_buttons(button_num)
                    if not button_leds[i] == -1 and Neopixel:
                        pixels[button_leds[i]] = (0,0,0)
                else:
                    gp.press_buttons(button_num)
                    if not button_leds[i] == -1 and Neopixel:
                        pixels[button_leds[i]] = led_color[button_leds[i]]
            else:
                gp.press_buttons(button_num)
                # print ("pressed:",button_num)
                if not button_leds[i] == -1 and Neopixel:
                    # print ("LED",button_leds[i])
                    pixels[button_leds[i]] = led_color[button_leds[i]]
            current_time = time.monotonic()
            #turbo setting
            if isTurbo and turbo.value != last_turbo:
                last_turbo = turbo.value
                if not last_turbo:
                    turbo_status[i] = 1 if turbo_status[i] == 0 else 0
        else:
            gp.release_buttons(button_num)
            if not button_leds[i] == -1 and Neopixel:
                pixelfading(button_leds[i])
    # Joystick
    x = y = 127
    hatstring = ''
    for i, dpad in enumerate(dpads):
        if not dpad.value:
            if dpad_mode == "axis":
                if dpad_all[i] == "UP" or dpad_all[i] == "DOWN":
                    y =  dpad_axis[i]
                else:
                    x =  dpad_axis[i]
            else:
                hatstring += dpad_all[i]
            if not dpad_leds[i] == -1 and Neopixel:
                pixels[dpad_leds[i]] = led_color[dpad_leds[i]]
        else:
            if not dpad_leds[i] == -1 and Neopixel:
                pixelfading(dpad_leds[i])
    if isAnalog :
        if dpad_mode == "axis":
            hatstring = analog_hat(ax.value, ay.value)
            print (hatstring)
        else:
            x = analog_check(ax.value)
            y = analog_check(ay.value)
    if not x == 127 or not y == 127 or not hatstring == "":
        current_time = time.monotonic()

    gp.move_joysticks(x, y)
    gp.hat_pos(hatposition[hatstring])
    if Neopixel:
        pixels.show()
    #time.sleep(0.01)

