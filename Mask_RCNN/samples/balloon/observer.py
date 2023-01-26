import os
import sys
import base64
import asyncio

from PIL import Image
import devices_program
import smartlink
import io
sys.path.append(r'..\balloon\UdcScriptExecutorAndTestSkrypt\udchttp')
sys.path.append(r'..\balloon\UdcScriptExecutorAndTestSkrypt')
from UdcScriptExecutorAndTestSkrypt import UdcScriptExecutor

sys.path.append(r"../..")
sys.path.append(r"")

def image_to_base64(image):
    img = Image.fromarray(image)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str

async def process_image(img):
    print(f'Processing {img}')
    if img.endswith("_0.png"):
        image = smartlink.smartlink(os.path.abspath('../../../media' + '/' + img))
        image_base64 = image_to_base64(image[0])
        data = {
            'device': image[1],
            'image_name': img
        }
    elif img.endswith("_1.png"):
        image = devices_program.detect_devices(os.path.abspath('../../../media' + '/' + img))
        image_base64 = image_to_base64(image[0])
        data = {
            'device': image[1],
            'image_name': img
        }


    udcServer = 'http://udcdev1:8080/'
    udcUserName = 'administrator'
    udcPassword = 'password1'
    scriptPath = os.path.abspath(r'..\balloon\UdcScriptExecutorAndTestSkrypt\sampleProcedureScriptExecutor.py')
    scriptParameter = f'{image_base64} {data}'
    isLdap = 'false'

    executor = UdcScriptExecutor.UdcScriptExecutor(udcServer, udcUserName, udcPassword, isLdap == 'True')
    result = executor.executeScriptFromFile(scriptPath, scriptParameter)

    print(f'Processed {img} and sent to UDC {result}')
    os.remove(os.path.abspath('../../../media' +'/'+ img))



async def main():

    while True:
        tasks = []
        for img in os.listdir(os.path.abspath('../../../media')):
            task = asyncio.create_task(process_image(img))
            tasks.append(task)
        await asyncio.gather(*tasks)
        await asyncio.sleep(10)

asyncio.run(main())




