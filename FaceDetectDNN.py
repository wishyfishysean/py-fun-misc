# -------------------------------
# Real-time Face Detection with DNN
# -------------------------------

import cv2

# --- Load the pre-trained DNN face detector ---
# These 2 files are needed (download from OpenCV's GitHub):
# - deploy.prototxt.txt (model architecture)
# - res10_300x300_ssd_iter_140000.caffemodel (pre-trained weights)
modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
configFile = "deploy.prototxt.txt"

net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

# --- Start webcam capture --- webcam (0), first external USB (1) --> 2, 3, 4
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Get frame dimensions
    h, w = frame.shape[:2]

    # Preprocess: resize to 300x300, mean subtraction as required by model
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                 scalefactor=1.0,
                                 size=(300, 300),
                                 mean=(104.0, 177.0, 123.0))

    net.setInput(blob)
    detections = net.forward()

    # Loop through detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Only consider detections above 50% confidence
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (x1, y1, x2, y2) = box.astype("int")

            # Draw rectangle + confidence label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            text = f"{confidence*100:.1f}%"
            cv2.putText(frame, text, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("DNN Face Detection", frame)

    # Exit on Esc
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
