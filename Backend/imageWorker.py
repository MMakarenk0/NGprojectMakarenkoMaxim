from PIL import Image
import threading

def invertColors(img, filePath, threadIndex, threadNumber, lock):
    pixels = img.load()
    width, height = img.size

    
    for i in range(threadIndex, width, threadNumber):
        for j in range(height):
            red, green, blue, a = pixels[i, j]
            pixels[i, j] = 255 - red, 255 - green, 255 - blue, a

    with lock:
        img.save(filePath)

def threadManager(threadNumber, func, args):
    lock = threading.Lock()
    threads = []

    for threadIndex in range(threadNumber):
        copyArgs = args[:]
        copyArgs = copyArgs + (threadIndex, threadNumber, lock)
        threads.append(threading.Thread(target=func, args=copyArgs))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
