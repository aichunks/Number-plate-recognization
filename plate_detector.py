import cv2 as cv
import numpy as np
import pytesseract
from superresolution import superme

confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold

inpWidth = 416  # 608     #Width of network's input image
inpHeight = 416  # 608     #Height of network's input image





# Load names of classes
classesFile = "detector/classes.names";

classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.

modelConfiguration = "detector/darknet-yolov3.cfg";
modelWeights = "detector/lapi.weights";

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    boxes = []
    for out in outs:
        #print("out.shape : ", out.shape)
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                boxes.append([left, top, width, height])
                frame = superme(frame[top:top + height, left:left + width])
                frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(frame, lang='eng', config='--psm 4 --oem 3')
                # print('NUMBER ', text)
                return  text
                # cv.imshow('', frame)
                # cv.waitKey(0)


def detect_plate(image_path):
    frame = cv.imread(image_path)
    blob = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))
    plate_number=postprocess(frame, outs)
    return plate_number
