import board
# color preset
RED = (255,  0,  0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 250, 250)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
GREY = (30, 30, 30)
WHITE = (125, 125, 125) # better not to use

config = {
    # 4way Joystick pins
    # [up, down ,left , right]
   "dpad_pins": [board.GP2, board.GP3, board.GP4, board.GP5],
   # index of NeoPixel LED for DPAD (1~ ) 0 = none
   "dpad_leds": [0, 0, 0, 0],
   # Buttons - up to 16
   # 1:X, 2:A, 3:B, 4:Y, 5:LB, 6:RB, 7:LT, 8:RT, 9:SELECT, 10:START
   # You can set NeoPixel LED index number with "~_led" parameter : (1~ )
   #   6-5-4-
   #   1-2-3-
   # comment out anything if you don't need
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
   "SELECT":board.GP12,
   "START":board.GP13,
   #"L3":board.GP16,
   #"R3":board.GP17,
   #"HOME":board.GP16,
   #"TOUCH":board.GP17,
   #"L4":board.GP17,
   #"R4":board.GP17,

   # NeoPixel - WS2812
   "neopixel_pin": board.GP0,
   # RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, GREY, WHITE
   # RGB LED Color, must set as many as LED lights you have
   "led_color": [GREEN, RED, CYAN, CYAN, YELLOW, BLUE ],
   "led_brightness": 1, # 1 is maximum value
   "fadingstep" : 12, # Dimming speed - higher, faster
   "activetime" : 5, # Standby mode entry time(sec)

   # Basic setup
   # joystick mode - 'axis' or 'hat'
   "dpad_mode": "hat",

}
