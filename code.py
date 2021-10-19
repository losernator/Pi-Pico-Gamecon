# raspigamer
# License-Identifier: MIT
# 2021/10/18
import time
import board
import digitalio
import analogio
import usb_hid
from hid_gamepad import Gamepad
#import adafruit_fancyled.adafruit_fancyled as fancy
import neopixel
try:
    from rainbowio import colorwheel
except ImportError:
    try:
        from _pixelbuf import colorwheel
    except ImportError:
        from adafruit_pypixelbuf import colorwheel
gp = Gamepad(usb_hid.devices)
# 컬러프리셋
RED = (255,  0,  0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 250, 250)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
GREY = (30, 30, 30)
WHITE = (128, 128, 128) #고급 네오픽셀에서만 사용
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
# 사용자 설정
ledcolor = (GREEN,RED,CYAN,CYAN,YELLOW,BLUE) #LED별 색상, LED개수 만큼 지정*중요
num_pixels = len(ledcolor) # led개수
led_brightness = 1 # led 밝기
fadingstep = -15 # 디밍 밝기 감소 단위
activetime = 5 # 대기모드 진입시간(초)
# 버튼 설정, 최대16개
button_pins = (board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP13, board.GP12)
# 핀별 LED번호 지정, LED 없음 = 0
#   6-5-4-
#   1-2-3-
button_leds = (1, 2, 6, 5, 4, 3, 0, 0)
# 1:X, 2:A, 3:B, 4:Y, 5:LB, 6:RB, 7:LT, 8:RT, 9:SELECT, 10:START
gamepad_buttons = (2, 3, 1, 4, 5, 6, 9, 10) # 버튼 번호
hat_pins = (board.GP2, board.GP3, board.GP4, board.GP5) # 방향키HAT핀(디지털)
hat_leds = (0, 0, 0, 0) # 방향키용 LED번호 지정, LED 없음 = 0
gamepad_hats = ('up', 'down', 'left', 'right')
# 사용자 설정 끝
'''
# 아날로그 핀할당
#ax = analogio.AnalogIn(board.GP26)
#ay = analogio.AnalogIn(board.GP27)
'''
pixels = neopixel.NeoPixel(board.GP0, num_pixels, auto_write=False)
pixels.brightness = led_brightness
buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
hats = [digitalio.DigitalInOut(pin) for pin in hat_pins]
for hat in hats:
    hat.direction = digitalio.Direction.INPUT
    hat.pull = digitalio.Pull.UP
# 아날로그 범위
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# 레인보우 효과
def rainbow(speed):
    ebreak = False
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(speed)
        for i, button in enumerate(buttons):
            if not button.value:
                ebreak = True
                break
        for i, hat in enumerate(hats):
            if not hat.value:
                ebreak = True
                break
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
        for i, hat in enumerate(hats):
            if not hat.value:
                ebreak = True
                break
        if (ebreak):
            break
    time.sleep(0.5)

def pixelfading(index):
    if pixels[index][0]+pixels[index][1]+pixels[index][2] > 0:
        pixels[index]=(max([pixels[index][0]+ fadingstep,0]), max([pixels[index][1]+ fadingstep,0]), max([pixels[index][2]+ fadingstep,0]))
    pixels.show()

current_time = time.monotonic()
while True:
    if time.monotonic() - current_time > activetime:
        rainbow(0.003)
    # 버튼 눌림 value = False
    for i, button in enumerate(buttons):
        button_num = gamepad_buttons[i]
        if not button.value:
            current_time = time.monotonic()
            gp.press_buttons(button_num)
            if not button_leds[i] == 0:
                pixels[button_leds[i]-1] = ledcolor[button_leds[i]-1]
                pixels.show()
        else:
            gp.release_buttons(button_num)
            if not button_leds[i] == 0:
                pixelfading(button_leds[i]-1)
    # 8방향 HAT
    hatstring = ''
    for i, hat in enumerate(hats):
        if not hat.value:
            current_time = time.monotonic()
            hatstring += gamepad_hats[i]
            if not hat_leds[i] == 0:
                pixels[hat_leds[i]-1] = ledcolor[hat_leds[i]-1]
        else:
            if not hat_leds[i] == 0:
                pixelfading(hat_leds[i]-1)
    gp.hat_pos(hatposition[hatstring])

    #데이터 변환 [0, 65535] to -127 to 127
    #gp.move_joysticks(
    #    x=range_map(ax.value, 0, 65535, -127, 127),
    #    y=range_map(ay.value, 0, 65535, -127, 127),
    #)
    time.sleep(0.001)

