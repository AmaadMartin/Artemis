from GUIAgent.tools.GroundingAgent import get_coordinates
import pyautogui as gui

def click(self, args):
    button = args["button"]
    if button == "left":
        gui.click()
    elif button == "right":
        gui.click(button="right")
    return "clicked"

def scroll(self, args):
    direction = args["direction"]
    if direction == "up":
        gui.scroll(1)
    elif direction == "down":
        gui.scroll(-1)
    return "scrolled"

def move_mouse_to_element(self, args):
    task = args['element'] if "element" in args else args["task"]
    print(task)

    normalized_coordinates = get_coordinates(self.image, task)
    print(normalized_coordinates)

    # Get the screen resolution
    screen_width, screen_height = gui.size()
    
    try:
        unnormalized_coordinates = float(normalized_coordinates['x']) * screen_width, float(normalized_coordinates['y']) * screen_height
        gui.moveTo(unnormalized_coordinates[0], unnormalized_coordinates[1], 0.5, gui.easeOutQuad)
    except Exception as e:
        print(normalized_coordinates)
        return e
    return normalized_coordinates

def adjust_mouse(self, args):
    x = args["x"]
    y = args["y"]
    screen_width, screen_height = gui.size()
    unnormalized_coordinates = x * screen_width, y * screen_height
    gui.moveTo(unnormalized_coordinates[0], unnormalized_coordinates[1], 0.5, gui.easeOutQuad)
    return "adjusted mouse"

def type_text(self, args):
    text = args["text"]
    gui.write(text)
    return "typed text"

def hotkey(self, args):
    keys = args["keys"]
    # keys = tuple(keys)
    print("keys: ", end="")
    print(keys)
    gui.hotkey(keys, interval=0.05)
    return "pressed hotkey"


tools = {
                    "click": {
                        "function": click,
                        "description": "clicks the mouse. example inputs: {\"button\": \"left\"} {\"button\": \"right\"}",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "button": {"type": "string", "description": "The button to click"}
                            },
                            "required": ["button"]
                        }
                    },
                    "scroll": {
                        "function": scroll,
                        "description": "scrolls the screen up or down. example inputs: {\"direction\": \"up\"} {\"direction\": \"down\"}",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "direction": {"type": "string", "description": "The direction to scroll"}
                            },
                            "required": ["direction"]
                        },
                    },

                        "move_mouse_to_element": {
                        "function": move_mouse_to_element,
                        "description": "Moves mouse to the element given. example inputs: {\"element\": \"search bar\"} {\"element\": \"fullscreen\"} {\"element\": \"close button\"}",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "element" : {"type": "string", "description": "The element to move the mouse to"}
                            },
                            "required": []
                        }
                    },
                    "adjust_mouse": {
                        "function": adjust_mouse,
                        "description": "Moves mouse to the coordinates given to adjust the mouse position. example inputs: {\"x\": 0.35, \"y\": 0.47} {\"x\": 0.12, \"y\": 0.39}",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "x": {"type": "number", "description": "x coordinate"},
                                "y": {"type": "number", "description": "y coordinate"},
                            },
                            "required": ["x", "y"]
                        }
                    },
                    "type_text": {
                        "function": type_text,
                        "description": "Types the given text",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string", "description": "The text to type"},
                            },
                            "required": ["text"]
                        }
                    },
                    "hotkey": {
                        "function": hotkey,
                        "description": "Presses the given hotkey",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "keys": {"type": "array", "items": {"type": "string"}, "description": "The keys to press"},
                            },
                            "required": ["keys"]
                        }
                    }
                }

def execute_action(self, action):
    tool = action["tool"]
    args = action["args"]
    output = tools[tool]["function"](self, args)

    self.trace.append(
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": f"OUTPUT: {output}"}
            ]
        }
    )