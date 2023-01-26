import glob
import cv2
from dbr import *
import time
import matplotlib.pyplot as plt






def yolo2crop(pathimages:str, pathlabels:list, dbr:BarcodeReader):
    data = []
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    thickness = 2
    #listdr=os.listdir(pathlabels)
    # for i in range(len(listdr)):
    #     with open(pathlabels + '/'+listdr[i], 'r') as f:
    #         lines = f.readlines()
    #         splitedlines = [None] * len(lines)
    #         cnt = 0;
    #         for l in lines:
    #             splitedlines[cnt] = l.split()
    #             cnt = cnt+1
    #
    #             listjpg = [None] * len(listdr)
    #         for u in range(len(listdr)):
    #             listjpg[u]=listdr[u]
    #             listjpg[u] = listjpg[u][:len(listjpg[u])-3]
    #             listjpg[u] = listjpg[u]+"jpg"
    #

    image = cv2.imread(pathimages)
    imagesq = image
    iheight, iwidth, channels = image.shape

    tmp = 0
    splitedlines = [None]*len(pathlabels)
    for path in pathlabels:
        splitedlines[tmp] = path
        tmp = tmp+1;


    label = splitedlines[0]
    xcenter = float(splitedlines[1])
    ycenter = float(splitedlines[2])
    xsize = float(splitedlines[3])
    ysize = float(splitedlines[4])

    xcenterpx = xcenter * iwidth
    ycenterpx = ycenter * iheight
    xsizepx = xsize * iwidth
    ysizepx = ysize * iheight
    ystart = round(ycenterpx - (ysizepx/2))
    ystop = round(ycenterpx + (ysizepx/2))

    xstart = round(xcenterpx - (xsizepx/2))
    xstop = round(xcenterpx + (xsizepx/2))

    cropped_image = image[ystart:ystop, xstart:xstop]

                # plt.imshow(cropped_image)
                # plt.show

    results = dbr.decode_buffer(cropped_image)
    text = 'test'
    if results is not None:

        for result in results:
                        #print("Barcode says: " + str(result.barcode_text))
            text = str(result.barcode_text)
                    # imagesq = cv2.rectangle(imagesq,(xstart,ystart),(xstop,ystop),(0,0,255),2)
                    # imagesq = cv2.putText(imagesq, text, (xstart,ystart-5), font, fontScale, (0,0,255), thickness, cv2.LINE_AA)
                    #cv2.imwrite('C:/Users/jpalachniak/Desktop/barcode/Wykrywanie_barcodow/crop/'+ str(c) + str(listjpg[i]),cropped_image)

                    #print(listjpg[i], label, text, xstart,xstop,ystart,ystop)
        data.append([text, xstart,xstop,ystart,ystop])
                # else:
                #     print('No barcode detected')

        #cv2.imwrite('C:/Users/jpalachniak/Desktop/barcode/Wykrywanie_barcodow/'+str(listjpg[i]) ,imagesq)
    return data


def config_readrate_first(dbr:BarcodeReader):

    # Obtain current runtime settings of instance.
    sts = dbr.get_runtime_settings()

    # Parameter 1. Set expected barcode formats
    # Here the barcode scanner will try to find the maximal barcode formats.
    sts.barcode_format_ids = EnumBarcodeFormat.BF_ALL
    sts.barcode_format_ids_2 = EnumBarcodeFormat_2.BF2_DOTCODE | EnumBarcodeFormat_2.BF2_POSTALCODE

    # Parameter 2. Set expected barcode count.
    # Here the barcode scanner will try to find 64 barcodes.
    # If the result count does not reach the expected amount, the barcode scanner will try other algorithms in the setting list to find enough barcodes.
    sts.expected_barcodes_count = 1

    # Parameter 3. Set more binarization modes.
    sts.binarization_modes = [EnumBinarizationMode.BM_LOCAL_BLOCK,EnumBinarizationMode.BM_THRESHOLD,0,0,0,0,0,0]

    # Parameter 4. Set more localization modes.
    # LocalizationModes are all enabled as default. Barcode reader will automatically switch between the modes and try decoding continuously until timeout or the expected barcode count is reached.
    # Please manually update the enabled modes list or change the expected barcode count to promote the barcode scanning speed.
    # Read more about localization mode members: https://www.dynamsoft.com/barcode-reader/parameters/enum/parameter-mode-enums.html?ver=latest#localizationmode
    sts.localization_modes = [EnumLocalizationMode.LM_CONNECTED_BLOCKS,EnumLocalizationMode.LM_SCAN_DIRECTLY,EnumLocalizationMode.LM_STATISTICS,
                              EnumLocalizationMode.LM_LINES,EnumLocalizationMode.LM_STATISTICS_MARKS,EnumLocalizationMode.LM_STATISTICS_POSTAL_CODE,0,0]

    # Parameter 5. Set more deblur modes.
    # DeblurModes are all enabled as default. Barcode reader will automatically switch between the modes and try decoding continuously until timeout or the expected barcode count is reached.
    # Please manually update the enabled modes list or change the expected barcode count to promote the barcode scanning speed.
    # Read more about deblur mode members: https://www.dynamsoft.com/barcode-reader/parameters/enum/parameter-mode-enums.html#deblurmode
    sts.deblur_modes = [EnumDeblurMode.DM_DIRECT_BINARIZATION,EnumDeblurMode.DM_THRESHOLD_BINARIZATION,EnumDeblurMode.DM_GRAY_EQUALIZATION,
                        EnumDeblurMode.DM_SMOOTHING,EnumDeblurMode.DM_MORPHING,EnumDeblurMode.DM_DEEP_ANALYSIS,EnumDeblurMode.DM_SHARPENING,0,0,0]

    # Parameter 6. Set scale up modes.
    # It is a parameter to control the process for scaling up an image used for detecting barcodes with small module size
    sts.scale_up_modes = [EnumScaleUpMode.SUM_AUTO,0,0,0,0,0,0,0]

    # Parameter 7. Set grayscale transformation modes.
    # By default, the library can only locate the dark barcodes that stand on a light background. "GTM_INVERTED":The image will be transformed into inverted grayscale.
    sts.grayscale_transformation_modes = [EnumGrayscaleTransformationMode.GTM_ORIGINAL,EnumGrayscaleTransformationMode.GTM_INVERTED,0,0,0,0,0,0]

    # Parameter 8. Enable dpm modes.
    # It is a parameter to control how to read direct part mark (DPM) barcodes.
    sts.dpm_code_reading_modes = [EnumDPMCodeReadingMode.DPMCRM_GENERAL,0,0,0,0,0,0,0]

    # Parameter 9. Increase timeout(ms). The barcode scanner will have more chances to find the expected barcode until it times out
    sts.timeout = 30000

    # Apply the new settings to the instance
    dbr.update_runtime_settings(sts)

def config_readrate_first_by_template(dbr:BarcodeReader):
    # Compared with PublicRuntimeSettings, parameter templates have a richer ability to control parameter details.
    # Please refer to the parameter explanation in "read-rate-first-template.json" to understand how to control read rate first.
    template_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "read-rate-first-template.json"
    error = dbr.init_runtime_settings_with_file(template_path, EnumConflictMode.CM_OVERWRITE)
    if error[0] != EnumErrorCode.DBR_OK:
        print("init_runtime_settings_with_file error: " + error[1])

def output_results(results:TextResult):
    if results != None:
        i = 0
        for res in results:
            barcode_format = res.barcode_format_string_2 if res.barcode_format==0 else res.barcode_format_string

            print("Barcode " + str(i) + ":" + barcode_format + "," + res.barcode_text)
            i = i+1
    else:
        print("No data detected.")



def read_barcodes(img_path:str, labels_path:list):


    try:
        # 1.Initialize license.
        # The string "DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9" here is a free public trial license. Note that network connection is required for this license to work.
        # You can also request a 30-day trial license in the customer portal: https://www.dynamsoft.com/customer/license/trialLicense?product=dbr&utm_source=samples&package=python
        error = BarcodeReader.init_license("t0076oQAAAJQBnsbxOzwunZvBZVOd+QWr/hhalXyPIV5Ijt0TJ/0c4qvCkYq/EczhK5c/Cw8uHz6Izn+6Pk4GZQDfps8bZZjCIrJe/6gi8g==")
        if error[0] != EnumErrorCode.DBR_OK:
            print("License error: "+ error[1])

        # 2.Create an instance of Barcode Reader.
        dbr = BarcodeReader()
        # #
        # #         # Replace by your own image path
        # #         #image_path = "C:/Users/jpalachniak/Desktop/barcode/test21.jpg"
        # #
        # #         # Accuracy = The number of correctly decoded barcodes/the number of all decoded barcodes
        # #         # There are two ways to configure runtime parameters. One is through PublicRuntimeSettings, the other is through parameters template.
        # #         print("Decode through PublicRuntimeSettings:")
        # #
        #         # 3.a config through PublicRuntimeSettings
        config_readrate_first(dbr)
        #
        #         tic = time.perf_counter()
        # #
        # #         # 4.a Decode barcodes from an image file by current runtime settings. The second parameter value "" means to decode through the current PublicRuntimeSettings.
        # #         # results = dbr.decode_file(image_path,"")
        #         image_folder = 'C:/Users/jpalachniak/IdeaProjects/barcodereader/object_detection/yolov5/runs/detect/exp41_/crops/barcode'
        #         barcodecounter = 0



        data = yolo2crop(img_path, labels_path, dbr)



        #         for idx, img in enumerate(glob.glob(os.path.join(image_folder, "*.*"))):
        #             print('Test', idx+1, img)
        #             image = cv2.imread(img)
        #             # 3. Decode barcodes from an image file
        #             results = dbr.decode_file(img)
        #             if results is not None:
        #
        #                 for result in results:
        #                     barcodecounter = barcodecounter+1
        #                     print("Confidence: " + str(result.extended_results[0].confidence))
        #                     print("Angle: " + str(result.localization_result.angle))
        #                     print("Localization points: " + str(result.localization_result.localization_points))
        #                     print("Barcode says: " + str(result.barcode_text))
        #
        #                     points = result.localization_result.localization_points
        #                     for p in points:
        #                         image = cv2.circle(image, p, radius=10, color=(255, 255, 0), thickness=-1)
        #
        #                     plt.imshow(image)
        #                     plt.show()
        #             else:
        #
        #                 plt.imshow(image)
        #                 plt.show()
        #
        #         toc = time.perf_counter()
        #         print(f"Time: {toc - tic:0.4f} seconds")
        #         # 5.a Output the barcode format and barcode text.
        #         output_results(results)
        #         print("Liczba znalezionych barcodów: " + str(barcodecounter))
        #
        #
        #
    except BarcodeReaderError as bre:
        print(bre)
    return data
