import time
from eeg import EmotivBCIClient
from controller import XboxController
from config import ACTION_TO_BUTTON, POWER_THRESHOLD, DEBOUNCE_SECONDS

def main():
    bci = EmotivBCIClient()
    pad = XboxController() 
    last_action_time = 0.0

    print('listening for mental commands...')
    while True:
        act, power = bci.get_command()

        if act is None:
            continue
        
        now = time.time()
        if power >= POWER_THRESHOLD and (now - last_action_time) > DEBOUNCE_SECONDS:
            button = ACTION_TO_BUTTON.get(act)
            if button:
                print(f'{act} ({power:0.2f}) -> {button}')
                pad.tap_button(button)
                last_action_time = now

if __name__ == '__main__':
    main()