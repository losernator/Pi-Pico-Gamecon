import board
# color preset
RED = (255,  0,  0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 250, 250)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
GREY = (30, 30, 30)
WHITE = (250, 250, 250) # better not to use

config = {
   # 4way Joystick pins
   # [up, down ,left , right]
   # 방향키 핀 지정 [위, 아래, 좌, 우]
   "dpad_pins": [board.GP2, board.GP3, board.GP4, board.GP5],

   # index of NeoPixel LED for DPAD (1~ ) 0 = none
   # 방향키 네오픽셀 LED 번호, LED 사용 안할 시 0으로 설정
   "dpad_leds": [0, 0, 0, 0],

   # Buttons - up to 16
   # 1:X, 2:A, 3:B, 4:Y, 5:LB, 6:RB, 7:LT, 8:RT, 9:SELECT, 10:START
   # You can set NeoPixel LED index number with "~_led" parameter : (1~ )
   #   6-5-4-
   #   1-2-3-
   # comment out anything if you don't need
   # 버튼 설정 - 최대 16개까지 가능
   # 사용할 버튼 항목만 주석 삭제 후 설정
   # LED가 있을시 "버튼_led"값으로 번호 설정, 없을시 주석처리하거나 생략
   "A":board.GP6,
   "A_led": 1,
   "B":board.GP7,
   "B_led": 2,
   "X":board.GP8,
   "X_led": 6,
   "Y":board.GP9,
   "Y_led": 5,
   #"LB":board.GP14,
   #"LB_led": 0,
   #"RB":board.GP15,
   #"LB_led": 0,
   "LT":board.GP10,
   "LT_led": 4,
   "RT":board.GP11,
   "RT_led": 3,
   "SELECT":board.GP13,
   "START":board.GP12,
   #"L3":board.GP16,
   #"R3":board.GP17,
   "HOME":board.GP16,
   #"TOUCH":board.GP19,
   #"L4":board.GP20,
   #"R4":board.GP21,
   "MODE":board.GP14,
   "TURBO":board.GP15,

   # NeoPixel - WS2812
   # 네오픽셀 ws2812b 핀 설정
   # LED가 없을 경우 주석처리
   "neopixel_pin": board.GP0,
   # RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, GREY, WHITE
   # RGB LED Color, must set as many as LED lights you have
   # 버튼 별 기본 색상 설정 *LED 개수 만큼 지정할 것
   "led_color": [GREEN, RED, CYAN, CYAN, YELLOW, BLUE ],
   # LED 밝기 1이 최대
   "led_brightness": 1, # 1 is maximum value
   # 버튼 디밍 단계 (0~255), 높을수록 빨리 꺼짐
   "fadingstep" : 10, # Dimming speed - higher, faster
   # 대기모드 진입 시간 (초)
   "activetime" : 5, # Standby mode entry time(sec)

   # joystick mode - 'axis' or 'hat'
   # 조이스틱 모드 설정 'axis' 또는 'hat'
   "dpad_mode": "axis",
   "turbo_speed": 0.05,

}
