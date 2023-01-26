import os
import sys
import json
import datetime
import numpy as np
import skimage.draw
import time
import imgaug.augmenters as iaa
import matplotlib.pyplot as plt

# Root directory of the project
ROOT_DIR = os.path.abspath("../../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils
from mrcnn import visualize


# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")



class BalloonConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "wire"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + balloon

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.1


class InferenceConfig(BalloonConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


config = InferenceConfig()

def detect_and_color_splash(model, image_path=None):
    assert image_path
    class_names = ['bg', 'wire']

    # Image or video?
    if image_path:
        # Run model detection and generate the color splash effect
        print("Running on {}".format(image_path))
        # Read image
        image = skimage.io.imread(image_path)
        # Detect objects
        tic = time.perf_counter()
        r = model.detect([image], verbose=1)[0]
        toc = time.perf_counter()
        print(f"Czas {toc - tic:0.4f} seconds")
        # det = visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
        #                                   class_names, r['scores'])

        # Color splash
        lists_of_masks = color_splash(image, r['masks'])


        # # Save output
        # file_name = "splash_{:%Y%m%dT%H%M%S}.png".format(datetime.datetime.now())
        # skimage.io.imsave(file_name, det)
        return lists_of_masks

def color_splash(image, mask):
    """Apply color splash effect.
    image: RGB image [height, width, 3]
    mask: instance segmentation mask [height, width, instance count]
    Returns result image.
    """
    list_of_masks = []
    # Make a grayscale copy of the image. The grayscale copy still
    # has 3 RGB channels, though.
    gray = skimage.color.gray2rgb(skimage.color.rgb2gray(image)) * 0
    # Copy color pixels from the original color image where mask is set
    for msk in range (mask.shape[-1]):
        list_of_masks.append(mask[:,:,msk])
        # plt.imshow(mask[:,:,msk])
        # plt.show()
    if mask.shape[-1] > 0:
        # We're treating all instances as one, so collapse the mask into one layer
        mask = (np.sum(mask, -1, keepdims=True) >= 1)

        splash = np.where(mask, image, gray).astype(np.uint8)
    else:
        splash = gray.astype(np.uint8)

    return list_of_masks

def detect_wires(img_path:str):

    path_to_images = img_path


    model = modellib.MaskRCNN(mode="inference", config=config, model_dir=DEFAULT_LOGS_DIR)



    #weights_path = r'C:\Users\mkrol\IdeaProjects\smartlink_server\Mask_RCNN\samples\balloon\weights\wires_model.h5'
    weights_path = os.path.abspath('../smartlink_server/Mask_RCNN/samples/balloon/weights/wires_model.h5')

    #weights_path = r'C:\Users\jpalachniak\IdeaProjects\Smartlink\Mask_RCNN\logs\wire20221115T1406\mask_rcnn_balloon_1262.h5'

    model.load_weights(weights_path, by_name=True)

    list_of_masks = detect_and_color_splash(model, image_path=path_to_images)
    return list_of_masks
