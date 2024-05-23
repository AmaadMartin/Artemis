from pynput import keyboard
import pyautogui as gui
import tkinter as tk
from tkinter.simpledialog import askstring
from GUIAgent import GUIAgent
agent = GUIAgent()

# Variables to track if Ctrl and Command keys are held down
ctrl_pressed = False
command_pressed = False

def on_press(key):
    global ctrl_pressed, command_pressed

    if key == keyboard.Key.ctrl:
        ctrl_pressed = True
    elif key == keyboard.Key.cmd:
        command_pressed = True

def on_release(key):
    global ctrl_pressed, command_pressed

    # Update the status of Ctrl and Command keys
    if key == keyboard.Key.ctrl:
        ctrl_pressed = False
    elif key == keyboard.Key.cmd:
        command_pressed = False

    if hasattr(key, 'char') and ctrl_pressed and command_pressed and key.char == 'u':
        print("Processing")
        return False
    
def main():
    # Collect events until released
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()
    try:
        task = "add EAA's to my cart on amazon"
        agent.complete_task(task)
    except (KeyboardInterrupt, SystemExit):
        agent.print_trace()
        raise


if __name__ == "__main__":
    main()
