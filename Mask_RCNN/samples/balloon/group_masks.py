import cv2
import numpy as np
from PIL import Image as im
from PIL import ImageDraw

import random
import read_barcodes as rb


def group(barcodes_masks,barcodes_coords,ports_masks_plugged,ports_coords,wires_masks, img):

    wynik = [None]*len(barcodes_masks)
    cnt2 = 0
    for i in range(len(barcodes_masks)):
        maxoverlap = [False]*6
        cnt = 0
        for k in range(len(wires_masks)):
            overlaps = wires_masks[k] & barcodes_masks[i]

            if np.sum(overlaps) > np.sum(maxoverlap[0]):
                maxoverlap[0] = overlaps
                maxoverlap[1] = barcodes_masks[i]
                maxoverlap[2] = wires_masks[k]
                maxoverlap[3] = barcodes_coords[i]

        if maxoverlap[0] is not False:
            boolean = maxoverlap[1] | maxoverlap[2]
            maxoverlap[0] = boolean
            maxoverlap[5] = rb.read_barcodes(img,maxoverlap[3])
            test = im.fromarray(boolean)
            test = test.convert("L")
            cnt = cnt+1
        wynik[cnt2] = maxoverlap
        cnt2 = cnt2+1

    cnt2 = 0
    cnt1 = 0
    for l in range(len(wynik)):
        maxoverlap2 = [False]*6
        for p in range(len(ports_masks_plugged)):
            overlaps = ports_masks_plugged[p] & wynik[l][0]

            if np.sum(overlaps) > np.sum(maxoverlap2[0]):
                maxoverlap2[0] = overlaps
                maxoverlap2[1] = wynik[l][0]
                maxoverlap2[2] = ports_masks_plugged[p]
                maxoverlap2[4] = ports_coords[p]

                cnt1 = cnt1+1

        if maxoverlap2[0] is not False:
            boolean = maxoverlap2[1] | maxoverlap2[2]
            maxoverlap2[0] = boolean
            maxoverlap2[1] = wynik[l][1]   # barcodes masks
            maxoverlap2[3] = wynik[l][3]   # barcodes coords
            maxoverlap2[5] = wynik[l][5]   # barcodes data
            test = im.fromarray(boolean)
            test = test.convert("L")

        wynik[cnt2] = maxoverlap2
        cnt2 = cnt2+1


    barcodes_temp = [list(ele) for ele in barcodes_coords]
    barcodes_temp.sort(reverse=True, key = lambda x: x[3])
    device_barcode = barcodes_temp[0]
    device_name = rb.read_barcodes(img,device_barcode)

    if device_name ==[]:
        device_name = "No device found"
    else:
        device_name = device_name[0][0]

    if device_name.isnumeric():
        device_name = "No device found"

    return wynik, device_name


def visualize_masks(masks, org_img):
    cnt = 0
    for msk in masks:
        green = org_img
        greenw = org_img
        green[(msk[0]==True)] = [random.randrange(255),random.randrange(255),random.randrange(255)]
        greenw = cv2.addWeighted(green, 0.3, greenw, 0.7, 0)
        cnt = cnt+1


def visualize_ports(masks, masks1, org_img):
    cnt = 0
    for msk in masks:
        green = org_img
        greenw = org_img
        green[(msk==True)] = [0,0,random.randrange(255)]
        greenw = cv2.addWeighted(green, 0.3, greenw, 0.7, 0)
        cnt = cnt+1
    for msk1 in masks1:
        green[(msk1==True)] = [0,random.randrange(255),0]
        greenw = cv2.addWeighted(green, 0.3, greenw, 0.7, 0)
        cnt = cnt+1

def visualize_wires(masks, org_img):
    cnt = 0
    for msk in masks:
        green = org_img
        greenw = org_img
        green[(msk==True)] = [random.randrange(255),random.randrange(255),random.randrange(255)]
        greenw = cv2.addWeighted(green, 0.3, greenw, 0.7, 0)
        cnt = cnt+1

def visualize_results(results, img1, device_name):

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (100, 100)
    fontScale = 1
    color = (0, 0, 255)
    thickness = 2
    clean = img1
    iheight, iwidth, channels = img1.shape

    barcodes_ports = ""
    for i in range(len(results)):

        color = (random.randrange(255),random.randrange(255),random.randrange(255))
        mask = 0
        mask = results[i][1] | results[i][2]


        if np.any(results[i][1]):
            contours,hierarchy = cv2.findContours((results[i][1]*255).astype(np.uint8),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            print("Number of contours 1:" + str(len(contours)))
            x1,y1,w1,h1 = cv2.boundingRect(contours[0])
            img1 = cv2.rectangle(img1,(x1,y1),(x1+w1,y1+h1),color,4)
            img1 = cv2.putText(img1, str(results[i][5])[2:10], (x1, y1-10), font,
                                fontScale, color, thickness, cv2.LINE_AA)

        if np.any(results[i][2]):
            contours2,hierarchy2 = cv2.findContours((results[i][2]*255).astype(np.uint8),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            print("Number of contours 1:" + str(len(contours2)))
            x2,y2,w2,h2 = cv2.boundingRect(contours2[0])
            img1 = cv2.rectangle(img1,(x2,y2),(x2+w2,y2+h2),color,4)
            img1 = cv2.putText(img1, str(results[i][4][6]), (x2, y2-10), font,
                               fontScale, color, thickness, cv2.LINE_AA)

            barcodes_ports = barcodes_ports + str(results[i][4][6])+"," + str(results[i][5])[2:10] +";"


    img1 = cv2.putText(img1, ("Device: " + device_name), (100, 100), font, 3, (255,0,0), 4, cv2.LINE_AA)
    barcodes_ports = barcodes_ports + device_name


    return(img1, barcodes_ports)






