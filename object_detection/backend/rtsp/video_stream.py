import cv2 as cv

STREAM_URL = "video_test.MOV"

# Capture object
cap = cv.VideoCapture(STREAM_URL)

if not cap.isOpened():
    raise ValueError("No stream or video available")

while cap.isOpened():
    # Capture each frame
    retval, frame = cap.read()
    # return is true if there is frame/image read
    if retval:
        cv.imshow("Frame", frame)
        cv.waitKey(1)
        if 0xFF == ord("q"):
            break
    else:
        break

# Release video capture object
cap.release()

# Close all frames
cv.destroyAllWindows()
