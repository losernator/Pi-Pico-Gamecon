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
   # You can set NeoPixel LED index number with "~_led" parameter / comment out anything if you don't need LED
   # 방향키 핀 및 LED 지정 [위, 아래, 좌, 우]
   "UP":board.GP2,
   #"UP_led": 0,
   "DOWN":board.GP3,
   #"DOWN_led": 0,
   "LEFT":board.GP4,
   #"LEFT_led": 0,
   "RIGHT":board.GP5,
   #"RIGHT_led": 0,
   # Buttons - up to 16
   # 1:X, 2:A, 3:B, 4:Y, 5:LB, 6:RB, 7:LT, 8:RT, 9:SELECT, 10:START, 11:L3, 12:R3, 13:HOME, 14:TOUCH,
   # You can set NeoPixel LED index number with "~_led" parameter :
   #   5-4-3-
   #   0-1-2-
   # comment out anything if you don't need
   # 버튼 설정 - 최대 16개까지 가능
   # 사용할 버튼 항목만 주석 삭제 후 설정
   # LED가 있을시 "버튼_led"값으로 번호 설정, 없을시 주석처리하거나 생략
   "A":board.GP6,
   "A_led": 0,
   "B":board.GP7,
   "B_led": 1,
   "X":board.GP8,
   "X_led": 5,
   "Y":board.GP9,
   "Y_led": 4,
   "LB":board.GP10,
   "LB_led": 3,
   "RB":board.GP11,
   "RB_led": 2,
   "START":board.GP12,
   #"START_led": 7,
   "SELECT":board.GP13,
   #"SELECT_led": 8,
   #"LT":board.GP16,
   #"RT":board.GP17,
   #"L3":board.GP18,
   #"R3":board.GP19,
   #"HOME":board.GP20,
   #"TOUCH":board.GP21,
   #"L4":board.GP20,
   #"R4":board.GP21,
   "MODE":board.GP20,
   "TURBO":board.GP21,

   # NeoPixel - WS2812
   # 네오픽셀 ws2812b 핀 설정
   # LED가 없을 경우 주석처리
   "neopixel_pin": board.GP0,
   # RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, GREY, WHITE
   # RGB LED Color, must set as many as LED lights you have
   # 버튼 별 기본 색상 설정 *LED 개수 만큼 지정할 것
   "dpad_led_color": [GREEN, CYAN, YELLOW, BLUE ],
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
   "turbo_speed": 0.03,

}
