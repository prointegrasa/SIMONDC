import cv2
import numpy as np
from PIL import Image as im



def yolo2mask(coord:list, img):
    image = cv2.imread(img)
    iheight, iwidth, channels = image.shape
    mark = 0

    for c in range(len(coord)):
        if int(coord[c][0]) == 1:
            mark = mark +1

    masks_unplug = [np.zeros((iheight, iwidth), dtype="uint8")]*(len(coord)-mark)
    masks_plug = [np.zeros((iheight, iwidth), dtype="uint8")]*mark
    masks_plug_coords = [None]*mark

    iter_pl=0
    iter_unpl=0

    for c in range(len(coord)):
        temp_coords = [None]*7
        if int(coord[c][0]) == 0:
            label = coord[c][0]
            xcenter = float(coord[c][1])
            ycenter = float(coord[c][2])
            xsize = float(coord[c][3])
            ysize = float(coord[c][4])

            xcenterpx = xcenter * iwidth
            ycenterpx = ycenter * iheight
            xsizepx = xsize * iwidth
            ysizepx = ysize * iheight
            ystart = round(ycenterpx - (ysizepx/2))
            ystop = round(ycenterpx + (ysizepx/2))

            xstart = round(xcenterpx - (xsizepx/2))
            xstop = round(xcenterpx + (xsizepx/2))

            masks_unplug[iter_unpl] = np.zeros((iheight, iwidth), dtype="uint8")
            masks_unplug[iter_unpl] = cv2.rectangle(masks_unplug[iter_unpl], (xstart, ystart), (xstop, ystop), 255, -1)
            iter_unpl = iter_unpl +1
        else:
            label = coord[c][0]
            xcenter = float(coord[c][1])
            ycenter = float(coord[c][2])
            xsize = float(coord[c][3])
            ysize = float(coord[c][4])

            xcenterpx = xcenter * iwidth
            ycenterpx = ycenter * iheight
            xsizepx = xsize * iwidth
            ysizepx = ysize * iheight
            ystart = round(ycenterpx - (ysizepx/2))
            ystop = round(ycenterpx + (ysizepx/2))

            xstart = round(xcenterpx - (xsizepx/2))
            xstop = round(xcenterpx + (xsizepx/2))

            masks_plug[iter_pl] = np.zeros((iheight, iwidth), dtype="uint8")
            masks_plug[iter_pl] = cv2.rectangle(masks_plug[iter_pl], (xstart, ystart), (xstop, ystop), 255, -1)

            temp_coords[0] = coord[c][0]
            temp_coords[1] = coord[c][1]
            temp_coords[2] = coord[c][2]
            temp_coords[3] = coord[c][3]
            temp_coords[4] = coord[c][4]
            temp_coords[5] = coord[c][5]
            temp_coords[6] = coord[c][6]

            masks_plug_coords[iter_pl] = temp_coords
            iter_pl = iter_pl+1


    for i in range(len(masks_unplug)):
        masks_unplug[i] = masks_unplug[i].astype(dtype=bool)
    for o in range(len(masks_plug)):
        masks_plug[o] = masks_plug[o].astype(dtype=bool)

    return(masks_unplug,masks_plug,masks_plug_coords)