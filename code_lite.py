# raspigamer
# License-Identifier: MIT
# 2021/12/09
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
button_pins = []
gamepad_buttons = []
# 1:A, 2:B, 3:RB, 4:X, 5:Y, 6:LB, 7:LT, 8:RT, 9:L2, 10:R2, 11:SELECT, 12:START, 13:MODEB, 14:LS, 15:RS, 16:EX
# alternative config for tekknen
#button_keys = ['X', 'A', 'B', 'Y', 'LB', 'RB', 'LT', 'RT', 'SELECT', 'START', 'L2', 'R2', 'MODEB', 'LS', 'RS', 'EX']
button_keys = ['A', 'B', 'RB', 'X', 'Y', 'LB', 'LT', 'RT', 'L2', 'R2', 'SELECT', 'START', 'MODEB', 'LS', 'RS', 'EX']
for i, button in enumerate(button_keys):
for i, button in enumerate(button_keys):
    if config.get(button):
        button_pins.append(config.get(button))
        gamepad_buttons.append(i+1)
        button_leds.append(config.get(button+'_led', -1))

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

# Joystick lever
dpad_mode = config.get('dpad_mode')
dpad_axis = [ 0, 254, 0, 254 ]
hatposition = {
    "":-1,
    "UP":0,
    "DOWN":4,
    "LEFT":6,
    "RIGHT":2,
    "UPLEFT":7,
    "UPRIGHT":1,
    "DOWNLEFT":5,
    "DOWNRIGHT":3,
    "UPDOWN":-1,
    "UPDOWNLEFT":6,
    "UPDOWNRIGHT":2,
    "UPDOWNLEFTRIGHT":2,
    "LEFTRIGHT":-1,
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
while True:
    if Neopixel:
        if time.monotonic() - current_time > activetime:
            rainbow(0.003)
    # Button pressed value = False
    for i, button in enumerate(buttons):
        button_num = gamepad_buttons[i]
        if not button.value:
            current_time = time.monotonic()
            gp.press_buttons(button_num)
            if not button_leds[i] == -1 and Neopixel:
                pixels[button_leds[i]] = led_color[button_leds[i]]
        else:
            gp.release_buttons(button_num)
            if not button_leds[i] == -1 and Neopixel:
                pixelfading(button_leds[i])
    # Joystick
    x = y = 128
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

