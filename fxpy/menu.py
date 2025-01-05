import sys
import keyboard as kboard
# Controller from Pynput required to initiate a false input
from pynput.keyboard import Key, Controller

# Displays the menu with the options passed and selects the selected index
def display_menu(options, selected):
    for i, option in enumerate(options):
        prefix = "->  " if i == selected else "    "
        print(f"{prefix}{option.name}")
    print("\nEsc Exit")

# Moves the cursor up 'lines_count' lines and clears them
def clear_menu_lines(lines_count):
    sys.stdout.write(f"\033[{lines_count}A")  # Move up the cursor
    sys.stdout.write("\033[J")  # Clear everything from the cursor down
    sys.stdout.flush()

def start_menu(options):
    selected = 0

    # Only passing first 5 matches, as there are over 100 matches a few times and most of them are not useful
    if len(options) > 5:
        options = options[:5]

    menu_lines = len(options)+2 # Adding 2 to adjust for a blank line and the exit line at the end

    while True:
        display_menu(options, selected)

        key = kboard.read_event()
        if (key.name == "up" or key.name == "k") and key.event_type == "down":
            selected = (selected - 1) % len(options)
        elif (key.name == "down" or key.name == "j") and key.event_type == "down":
            selected = (selected + 1) % len(options)
        elif key.name == "enter" and key.event_type == "down":
            clear_menu_lines(menu_lines + 2)
            return selected
        elif key.name == "esc" and key.event_type == "down":
            # When user presses escape the input leaks to the receiver country input. To tackle this, a 'Enter' key is initiated when esc is pressed
            # This is not required when the user selects a country, as it is done by pressing enter.
            enter_keyboard = Controller()
            enter_keyboard.press(Key.enter)
            enter_keyboard.release(Key.enter)
            clear_menu_lines(menu_lines + 3)
            return None

        clear_menu_lines(menu_lines)  # Clear menu for redraw
