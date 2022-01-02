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
dpad_leds = [0, 0, 0, 0]
if config.get('neopixel_pin'):
    dpad_leds = config.get('dpad_leds')
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
# 1:X, 2:A, 3:B, 4:Y, 5:LB, 6:RB, 7:LT, 8:RT, 9:SELECT, 10:START, 11:L3, 12:R3, 13:HOME, 14:TOUCH, 15:L4, 16:R4
button_keys = ['X', 'A', 'B', 'Y', 'LB', 'RB', 'LT', 'RT', 'SELECT', 'START', 'L3', 'R3', 'HOME', 'TOUCH', 'L4', 'R4']
for i, button in enumerate(button_keys):
    if config.get(button):
        button_pins.append(config.get(button))
        gamepad_buttons.append(i+1)
        if config.get(button+'_led'):
            button_leds.append(config.get(button+'_led'))
        else:
            button_leds.append(0)

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

# Joystick lever
dpad_mode = config.get('dpad_mode')
dpad_pins = config.get('dpad_pins')
dpad_hats = ['up', 'down', 'left', 'right']
dpad_axis = [ -127, 127, -127, 127 ]
hatposition = {
    "":0,
    "up":1,
    "down":5,
    "left":7,
    "right":3,
    "upleft":8,
    "upright":2,
    "downleft":6,
    "downright":4,
    "updown":0,
    "updownleft":7,
    "updownright":3,
    "updownleftright":3,
    "leftright":0,
    "downleftright":5,
    "upleftright":1,
}
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

def singlerainbow(speed,pixel_index):
    for j in range(255):
        pixels[pixel_index]=colorwheel(256+j&255)
        pixels.show()
        time.sleep(speed)

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
            if not button_leds[i] == 0 and Neopixel:
                pixels[button_leds[i]-1] = led_color[button_leds[i]-1]
        else:
            gp.release_buttons(button_num)
            if not button_leds[i] == 0 and Neopixel:
                pixelfading(button_leds[i]-1)
    # Joystick
    x = y = 0
    hatstring = ''
    for i, dpad in enumerate(dpads):
        if not dpad.value:
            current_time = time.monotonic()
            if dpad_mode == "hat":
                hatstring += dpad_hats[i]
            else:
                if i < 2 :
                    y =  dpad_axis[i]
                else:
                    x =  dpad_axis[i]
            if not dpad_leds[i] == 0 and Neopixel:
                pixels[dpad_leds[i]-1] = led_color[dpad_leds[i]-1]
        else:
            if not dpad_leds[i] == 0 and Neopixel:
                pixelfading(dpad_leds[i]-1)
    if dpad_mode == "hat":
        gp.hat_pos(hatposition[hatstring])
    else:
        gp.move_joysticks(x, y)
    if Neopixel:
        pixels.show()
    #time.sleep(0.01)

