# raspigamer
# License-Identifier: MIT
# 2022/01/19
import time
import board
import digitalio
import usb_hid
import neopixel
from hid_gamepad import Gamepad
from adafruit_pypixelbuf import colorwheel
from configs import config

gp = Gamepad(usb_hid.devices)

#NeoPixel
button_leds = []
if config.get('neopixel_pin'):
    led_color = config.get('led_color')
    num_pixels = len(led_color)
    pixels = neopixel.NeoPixel(config.get('neopixel_pin'), num_pixels, auto_write=False)
    pixels.brightness = config.get('led_brightness')
    fadingstep = config.get('fadingstep')
    activetime = config.get('activetime')
    Neopixel = True
else :
    Neopixel = False

# Buttons
turbo_speed = config.get('turbo_speed')
turbo_status = []
button_pins = []
gamepad_buttons = []
# 1:A, 2:B, 3:RB, 4:X, 5:Y, 6:LB, 7:LT, 8:RT, 9:L2, 10:R2, 11:SELECT, 12:START, 13:MODEB, 14:THUMBL, 15:THUMBR, 16:EX
button_keys = ['A', 'B', 'RB', 'X', 'Y', 'LB', 'LT', 'RT', 'L2', 'R2', 'SELECT', 'START', 'MODEB', 'THUMBL', 'THUMBR', 'EX']
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
dpad_axis = [ -127, 127, -127, 127 ]
hatposition = {
    "":0,
    "UP":1,
    "DOWN":5,
    "LEFT":7,
    "RIGHT":3,
    "UPLEFT":8,
    "UPRIGHT":2,
    "DOWNLEFT":6,
    "DOWNRIGHT":4,
    "UPDOWN":0,
    "UPDOWNLEFT":7,
    "UPDOWNRIGHT":3,
    "UPDOWNLEFTRIGHT":3,
    "LEFTRIGHT":0,
    "DOWNLEFTRIGHT":5,
    "UPLEFTRIGHT":1,
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
                    print (lastshot_time)
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
                print ("pressed:",button_num)
                if not button_leds[i] == -1 and Neopixel:
                    print ("LED",button_leds[i])
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
    x = y = 0
    hatstring = ''
    for i, dpad in enumerate(dpads):
        if not dpad.value:
            current_time = time.monotonic()
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
    if dpad_mode == "axis":
        gp.move_joysticks(x, y)
    else:
        gp.hat_pos(hatposition[hatstring])
    if Neopixel:
        pixels.show()
    #time.sleep(0.01)

