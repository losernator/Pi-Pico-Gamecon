import board
# color preset
RED = (255,  0,  0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 40, 0)
CYAN = (0, 250, 250)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
GREY = (30, 30, 30)
WHITE = (250, 250, 250) # better not to use
TEAL = (0, 255, 120)
PURPLE = (180, 0, 255)
MAGENTA = (255, 0, 20)
BLACK = (0, 0, 0) # black or off
GOLD = (255, 222, 30)
PINK = (242, 90, 255)
AQUA = (50, 255, 255)
JADE = (0, 255, 40)
AMBER = (255, 100, 0)

config = {
   # 4way Joystick pins
   # You can set NeoPixel LED index number with "~_led" parameter / comment out anything if you don't need LED
   # 방향키 핀 및 LED 지정
   "UP":board.GP2,
   #"UP_led": 0,
   "DOWN":board.GP3,
   #"DOWN_led": 0,
   "LEFT":board.GP4,
   #"LEFT_led": 0,
   "RIGHT":board.GP5,
   #"RIGHT_led": 0,
   # Buttons - up to 16
   # 1:A, 2:B, 3:RB, 4:X, 5:Y, 6:RB, 7:LT, 8:RT, 9:L2, 10:R2, 11:SELECT, 12:START, 13:EX1, 14:LS, 15:RS, 16:EX2
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
   #"START_led": 6,
   "SELECT":board.GP13,
   #"SELECT_led": 7,
   "LT":board.GP16,
   #"LT_led": 8,
   "RT":board.GP17,
   #"RT_led": 9,
   #"L3":board.GP18,
   #"R3":board.GP19,
   #"PS":board.GP18,
   #"TP":board.GP19,
   #"EX1":board.GP20,
   #"EX2":board.GP21,
   "TURBO":board.GP20,
   "MODE":board.GP21,
   # Pins for anlog input - should be ADC pin
   #"AnalogX":board.GP27,
   #"AnalogY":board.GP26,

   # NeoPixel - WS2812
   # 네오픽셀 ws2812b 핀 설정
   # LED가 없을 경우 주석처리
   "neopixel_pin": board.GP0,
   # RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, GREY, WHITE
   # RGB LED Color, must set as many as LED lights you have
   # 버튼 별 기본 색상 설정 *LED 개수 만큼 지정할 것
   "led_color": [GREEN, RED, CYAN, CYAN, YELLOW, BLUE ],
   # Default color for buttons with no assigned color
   "default_color":GREY,
   # LED 밝기 1이 최대
   "led_brightness": 1, # 1 is maximum value
   # 버튼 디밍 단계 (0~255), 높을수록 빨리 꺼짐
   "fadingstep" : 10, # Dimming speed - higher, faster
   # 대기모드 진입 시간 (초)
   "activetime" : 5, # Standby mode entry time(sec)

   # Defult DPAD mode - 'axis' or 'hat'
   # 조이스틱 모드 설정 'axis' 또는 'hat'
   "dpad_mode": "hat",
   # Turbo button speed (sec)
   "turbo_speed": 0.04,

}
