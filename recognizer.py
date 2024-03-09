import cv2
import numpy
targetStartRow=190
targetEndRow=290
targetStartColumn=270
targetEndColumn=370
minNumOfCloseColorColumnsInTarget=60
minNumOfCloseColorRowsInTarget=60
maxNumOfCloseColorColumnsInTarget=70
maxNumOfCloseColorRowsInTarget=70
minNumOfCloseColorColumnsNotInTarget=20
minNumOfCloseColorRowsNotInTarget=20
showVideo = True
def isCubeColor(frame, i, j):
    b,g,r=frame[i,j]
    return (numpy.uint16(b)+numpy.uint16(g)+numpy.uint16(r)<90)
def isBlockCloseColorInTarget(i, j, frame):
    if not isCubeColor(frame, i, j) or not isCubeColor(frame, i+minNumOfCloseColorRowsInTarget, j) or not isCubeColor(frame, i, j+minNumOfCloseColorColumnsInTarget) or not isCubeColor(frame, i+minNumOfCloseColorRowsInTarget, j+minNumOfCloseColorColumnsInTarget):
        return False
    for k in range(minNumOfCloseColorRowsInTarget):
        for l in range(minNumOfCloseColorColumnsInTarget):
            if not isCubeColor(frame, i+k, j+l):
                return False
    isMissingPixels=False
    for k in range(maxNumOfCloseColorRowsInTarget):
        for l in range(maxNumOfCloseColorColumnsInTarget):
            if not isCubeColor(frame, i+k, j+l):
                isMissingPixels = True
    return isMissingPixels

def isBlockCloseColorNotInTarget(i, j, frame):
    if not isCubeColor(frame, i, j) or not isCubeColor(frame, i+minNumOfCloseColorRowsNotInTarget, j) or not isCubeColor(frame, i, j+minNumOfCloseColorColumnsNotInTarget) or not isCubeColor(frame, i+minNumOfCloseColorRowsNotInTarget, j+minNumOfCloseColorColumnsNotInTarget):
        return False
    for k in range(minNumOfCloseColorRowsNotInTarget):
        for l in range(minNumOfCloseColorColumnsNotInTarget):
            if not isCubeColor(frame, i+k, j+l):
                return False
    return True


def recognizeVideo(video):
    first = True
    while True:
        isOk, frame = video.read()
        if first:
            first = False
            print("height: "+str(frame.shape[0])+", width: "+str(frame.shape[1]))
        if not isOk:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        height=frame.shape[0]
        width=frame.shape[1]
        objectBegining=None
        for i in range(height-maxNumOfCloseColorRowsInTarget):
            for j in range(width-maxNumOfCloseColorColumnsInTarget):
                if j > targetStartColumn and j < targetEndColumn and i > targetStartRow and i < targetEndRow:
                    if (isBlockCloseColorInTarget(i, j, frame)):
                        return True
                elif objectBegining == None:
                    if (isBlockCloseColorNotInTarget(i, j, frame)):
                        objectBegining = (i,j)
        if objectBegining is not None:
            objectRow = objectBegining[0]
            objectColumn = objectBegining[1]
            if (objectColumn < targetStartColumn):
                print("Object on the left. Turning left...")
            elif (objectColumn > targetEndColumn):
                print("Object on the right. Turning right...")
            elif (objectRow < targetStartRow):
                print("Object on the top. Moving forward...")
            elif (objectRow > targetEndRow):
                print("Object on the bottom. Moving backwards...")
        else:
            print("Object not found yet.")
        if showVideo:
            cv2.rectangle(frame, (targetStartColumn, targetStartRow), (targetEndColumn, targetEndRow), (0, 255, 0), 2)
            if (objectBegining != None):
                cv2.rectangle(frame, (objectColumn, objectRow), (objectColumn+minNumOfCloseColorColumnsNotInTarget, objectRow+minNumOfCloseColorRowsNotInTarget), (0, 0, 255), 2)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
    return False


video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Cannot open camera")
    exit()
if recognizeVideo(video):
    print("Object in place. Lifting...")
else:
    print("Object not found. The program was stopped by the user.")
video.release()

