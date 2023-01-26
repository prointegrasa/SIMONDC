import base64

with open(r"C:\Users\arbat\Desktop\Praca\back\smartlink_app\media\smartlink_pics\papiez.png", "rb") as image_file:
        encoded_string = str(base64.b64encode(image_file.read()))[2:-1]

with open(r"C:\Users\arbat\Desktop\Praca\back\smartlink_app\media\smartlink_pics\papiez.txt", "w") as text_file:
        text_file.write(encoded_string)
