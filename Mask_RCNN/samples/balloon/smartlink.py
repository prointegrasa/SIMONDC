import matplotlib
import os
import sys
from keras import backend as K

matplotlib.use('TKAgg', force=True)

import sort_ports
import detect as yolodetect
import detect_wires as dw
import yolo2mask
import group_masks as gm
import cv2
from PIL import Image

sys.path.append(r"Mask_RCNN")
sys.path.append(r"Mask_RCNN/samples/balloon")

def smartlink(path:str):
    K.clear_session()
    ROOT_DIR = os.path.abspath("../")

    #zdj = '/15.jpg'

    #images = 'C:/Users/jpalachniak/Desktop/barcode/datasetall/test'
    # images = path
    #
    # #images2 = 'C:/Users/jpalachniak/Desktop/barcode/datasetall/test'+zdj
    images2 = path#+"/" + (os.listdir(path))[0]


    weights = os.path.join(ROOT_DIR, "smartlink_server/Mask_RCNN/samples/balloon/weights/barcode_weights.pt")
    weights2 = os.path.join(ROOT_DIR, "smartlink_server/Mask_RCNN/samples/balloon/weights/ports_model.pt")


    org_img = cv2.imread(images2)
    #im1 = Image.open(images2)

    wires_masks = dw.detect_wires(images2)

    barcodes_coords = yolodetect.detect(images2,weights)
    ports_coords = yolodetect.detect(images2,weights2)
    if len(ports_coords) != 0:
        temp = ports_coords
        ports_coords = sort_ports.sort(temp)

    barcodes_masks, thrash, thrash2 = yolo2mask.yolo2mask(barcodes_coords, images2)
    ports_masks_unplug,ports_masks_plug, ports_coords, = yolo2mask.yolo2mask(ports_coords, images2)

    wynik, device_name = gm.group(barcodes_masks, barcodes_coords, ports_masks_plug, ports_coords, wires_masks, images2)

    final_image, data = gm.visualize_results(wynik, org_img, device_name)
    K.clear_session()

    return (final_image, data)










