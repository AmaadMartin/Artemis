from mss import mss, tools
import base64
import tempfile

def screen_shot():
    with mss() as sct:
        # The screen part to capture
        monitor = sct.monitors[1]
        # Capture the screen
        sct_img = sct.grab(monitor)

    with tempfile.TemporaryDirectory() as temp_dir:
        output = f'{temp_dir}/screen.png'
        # Save to the picture file
        tools.to_png(sct_img.rgb, sct_img.size, output=output)

        with open(output, 'rb') as imgfile:
            base64_bytes = base64.b64encode(imgfile.read())
            base64_encoded = base64_bytes.decode()

    return base64_encoded

def image_to_file(image_b64):
    with tempfile.TemporaryDirectory() as temp_dir:
        output = f'{temp_dir}/screen.png'
        with open(output, 'wb') as imgfile:
            imgfile.write(base64.b64decode(image_b64))
    return output