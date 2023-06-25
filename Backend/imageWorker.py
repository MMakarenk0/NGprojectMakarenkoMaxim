from PIL import Image, ImageOps
import threading

def invertColors(imageParts, threadIndex):
    imageParts[threadIndex] = ImageOps.invert(imageParts[threadIndex])

def threadManager(threadNumber, func, args):
    threads = []
    
    for threadIndex in range(threadNumber):
        copyArgs = args[:]
        copyArgs = copyArgs + (threadIndex,)
        threads.append(threading.Thread(target=func, args=copyArgs))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def getMidpoints(width, height):
    midpoint_x = width // 2
    midpoint_y = height // 2
    return midpoint_x, midpoint_y

def cropImage(img):
    width, height = img.size
    midpoint_x, midpoint_y = getMidpoints(width, height)

    imageParts = []

    top_left_image = img.crop((0, 0, midpoint_x, midpoint_y))
    imageParts.append(top_left_image.copy())

    top_right_image = img.crop((midpoint_x, 0, width, midpoint_y))
    imageParts.append(top_right_image.copy())

    bottom_left_image = img.crop((0, midpoint_y, midpoint_x, height))
    imageParts.append(bottom_left_image.copy())

    bottom_right_image = img.crop((midpoint_x, midpoint_y, width, height))
    imageParts.append(bottom_right_image.copy())
    
    return imageParts, width, height

def mergeImage(savePath, imageParts, width, height):
    MergedImage = Image.new('RGB', (width, height))
    midpoint_x, midpoint_y = getMidpoints(width, height)

    MergedImage.paste(imageParts[0], (0, 0))
    MergedImage.paste(imageParts[1], (midpoint_x, 0))
    MergedImage.paste(imageParts[2], (0, midpoint_y))
    MergedImage.paste(imageParts[3], (midpoint_x, midpoint_y))

    MergedImage.save(savePath)
    return MergedImage

def colorOffset(pixelValue, offset):
    return pixelValue + offset

def imageColorShift(imageParts, RGBoffset, threadIndex):
    r, g, b = imageParts[threadIndex].split()
    rgbList = [r, g, b]
    for index in range(3):
        if RGBoffset[index] != 0:
            rgbList[index] = rgbList[index].point(lambda pixelValue: colorOffset(pixelValue, RGBoffset[index]))
    
    imageParts[threadIndex] = Image.merge("RGB", (rgbList[0], rgbList[1], rgbList[2]))
    
def createActionHistory(token, undoHistory, redoHistory):
    if token not in undoHistory.keys():
        undoHistory[token] = []
        redoHistory[token] = []

def updateHistory(token, undoHistory, redoHistory, image):
    undoHistory[token].append(image.copy())
    redoHistory[token] = []


