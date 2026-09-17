import board
import keypad
import rotaryio
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

rows = (board.D0, board.D1, board.D2)
cols = (board.D3, board.D4, board.D5)

keys = keypad.KeyMatrix(rows, cols, columns_to_anodes=False)

keyboard = Keyboard(usb_hid.devices)
volume = ConsumerControl(usb_hid.devices)

keycodes = (
    Keycode.ONE, Keycode.TWO, Keycode.THREE,
    Keycode.FOUR, Keycode.FIVE, Keycode.SIX,
    Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE
)

encoder = rotaryio.IncrementalEncoder(board.D6, board.D7)
last_position = encoder.position

button = digitalio.DigitalInOut(board.D8)
button.switch_to_input(pull=digitalio.Pull.UP)

while True:
    event = keys.events.get()

    if event:
        if event.pressed:
            keyboard.press(keycodes[event.key_number])
        elif event.released:
            keyboard.release(keycodes[event.key_number])

    position = encoder.position

    if position > last_position:
        volume.send(ConsumerControlCode.VOLUME_INCREMENT)
    elif position < last_position:
        volume.send(ConsumerControlCode.VOLUME_DECREMENT)

    last_position = position

    if not button.value:
        volume.send(ConsumerControlCode.MUTE)