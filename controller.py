import time
import vgamepad as vg

class XboxController:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()
        self.last_press = 0.0

    def tap_button(self, button, duration=0.1):
        self.gamepad.press_button(button=button)
        self.gamepad.update()
        time.sleep(duration)
        self.gamepad.release_button(button=button)
        self.gamepad.update()
        