from PIL import Image, ImageOps
import threading

def invertColors(imgs, threadIndex):
    imgs[threadIndex] = ImageOps.invert(imgs[threadIndex])

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
    merged_image = Image.new('RGB', (width, height))
    midpoint_x, midpoint_y = getMidpoints(width, height)

    merged_image.paste(imageParts[0], (0, 0))
    merged_image.paste(imageParts[1], (midpoint_x, 0))
    merged_image.paste(imageParts[2], (0, midpoint_y))
    merged_image.paste(imageParts[3], (midpoint_x, midpoint_y))

    merged_image.save(savePath)

