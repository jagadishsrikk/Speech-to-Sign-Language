
import cv2

cap = cv2.VideoCapture(0)

lower_thresh1=129
upper_thresh1=0xFF

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.rectangle(frame, (60, 60), (300, 300), (0xFF, 0xFF, 2), 4)
    cv2.imshow('Input', frame)

    crop_img = frame[70:300,70:300]
    grey = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)
    value = (35,35)

    blurred = cv2.GaussianBlur(grey,value,0)
    (_, thresh1) = cv2.threshold(blurred, lower_thresh1,upper_thresh1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)


    cv2.imshow('Binary Image',thresh1)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()