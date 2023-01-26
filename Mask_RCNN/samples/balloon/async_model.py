
import sys
sys.path.append(r"/Mask_RCNN")
sys.path.append(r"/Mask_RCNN/samples/balloon")
from Mask_RCNN.samples.balloon import smartlink as smartlink_model

img = smartlink_model.smartlink()