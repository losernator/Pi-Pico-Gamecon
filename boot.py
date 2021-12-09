import usb_hid
import usb_midi
import storage
import board
import digitalio

GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,  # Usage (Game Pad)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x04,  #   Report ID (4)
    0x05, 0x09,  #   Usage Page (Button)
    0x19, 0x01,  #   Usage Minimum (Button 1)
    0x29, 0x10,  #   Usage Maximum (Button 16)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x75, 0x01,  #   Report Size (1)
    0x95, 0x10,  #   Report Count (16)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x01,  #   Usage Page (Generic Desktop Ctrls)
    0x15, 0x81,  #   Logical Minimum (-127)
    0x25, 0x7F,  #   Logical Maximum (127)
    0x09, 0x30,  #   Usage (X)
    0x09, 0x31,  #   Usage (Y)
    0x09, 0x32,  #   Usage (Z)
    0x09, 0x35,  #   Usage (Rz)
    0x75, 0x08,  #   Report Size (8)
    0x95, 0x04,  #   Report Count (4)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x09, 0x39,  #   USAGE (Hat switch)
    0x15, 0x01,  #   LOGICAL_MINIMUM (0)
    0x25, 0x08,  #   LOGICAL_MAXIMUM (7)
    0x35, 0x00,  #   PHYSICAL_MINIMUM (0)
    0x46, 0x0e,  #   PHYSICAL_MAXIMUM (270)
    0x75, 0x04,  #   REPORT_SIZE (4)
    0x95, 0x01,  #   REPORT_COUNT (1)
    0x81, 0x02,  #   INPUT (Data,Var,Abs)
    0xC0,        # End Collection
))

gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(4,),           # Descriptor uses report ID 4.
    in_report_lengths=(7,),    # This gamepad sends 6 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable((gamepad,))
usb_midi.disable()

button = digitalio.DigitalInOut(board.GP2)
button.switch_to_input(pull=digitalio.Pull.UP)

if not button.value:
    storage.disable_usb_drive()    # Hide drive
    usb_cdc.disable()              # REPL off
'''
if not button.value:
    storage.remount("/", False)
'''
