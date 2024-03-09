import cv2
import numpy
startSearchingFromRow=0
stopSearchingAtRow=100
startSearchingFromColumn=0
stopSearchingAtColumn=100
numOfCloseColorColumnsInABlock=50
numOfCloseColorRowsInABlock=50
def isCubeColor(b,g,r):
    return (numpy.uint16(b)+numpy.uint16(g)+numpy.uint16(r)<90)
def isBlockCloseColor(i, j, frame):
    for k in range(numOfCloseColorRowsInABlock):
        for l in range(numOfCloseColorColumnsInABlock):
            b,g,r=frame[i+k,j+l]
            if not isCubeColor(b,g,r):
                return False
    return True

def recognizeVideo(video):
    while True:
        isOk, frame = video.read()
        if not isOk:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        height=frame.shape[0]
        width=frame.shape[1]
        for i in range(height-50):
            if i > startSearchingFromRow and i < stopSearchingAtRow:
                for j in range(width-50):
                    if j > startSearchingFromColumn and j < stopSearchingAtColumn:
                        if (isBlockCloseColor(i, j, frame)):
                            return True
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    return False


video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Cannot open camera")
    exit()
if recognizeVideo(video):
    print("Recognized")
else:
    print("Not Recognized")
video.release()

