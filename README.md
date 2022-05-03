# Pico Gamecon 
Pico Gamecon\
Raspberry Pi Pico Gamepad using CircuitPython 7.x

Supports 16 buttons, 4-way Joystick, 1 analog stick and NeoPixel WS2812B strip
 
## Changelog
- v 1.5
  * Add analog input (disabled default, should change config.py)

- v 1.4
  * Add Mode change button (axis - hat)
  * Add Turbo function (useage: hold button to use and press TURBO button simultaneously )

- v 1.3
  * Improved Neopixel dimming method
  * Fix HID recognition error on boot (Raspberry pi, android and some windows pc)
- v 1.2 - add config.py
- v 1.0

## How to use
### install circuitpython on your Pico
https://circuitpython.org/board/raspberry_pi_pico/

### PINOUT
![Pico Gamecon pinout](picocon_pinout.png)

### Options (configs.py):
- Pin number
- Buttons to use
- Turbo speed
- Neopixel Color, index num., fading speed

## Compatibility
D-INPUT
PC, Android, SBC like Rasberry Pi

## License
MIT

## Screenshots

## Videos
