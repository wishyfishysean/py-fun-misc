# -------------------------------
# Real-time Face & Eye Detection
# using Haar Cascade Classifiers
# -------------------------------

import cv2  

# --- Load pre-trained classifiers ---
# Haar cascades are XML files trained on lots of positive (faces/eyes) and negative (non-faces/non-eyes) images.
# Make sure these XML files are in the same folder as this script OR provide the full path.
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml') 

# --- Start video capture from default webcam ---
cap = cv2.VideoCapture(0)

# --- Main loop (runs until "Esc" is pressed) ---
while True:  
    # Read a single frame from the webcam
    ret, img = cap.read()
    if not ret:   # safety check if camera fails
        print("Failed to grab frame")
        break  

    # Convert the frame to grayscale (needed for Haar cascades)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces (scaleFactor=1.3, minNeighbors=5 are tuning parameters)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Loop through all detected faces
    for (x, y, w, h) in faces:
        # Draw a rectangle around each face
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)

        # Define the "region of interest" (ROI) for eyes inside the detected face
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        # Detect eyes inside the face ROI
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Draw rectangles around detected eyes
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 127, 255), 2)

    # Show the current frame in a window
    cv2.imshow('Face & Eye Detection', img)

    # Exit loop if "Esc" key is pressed
    if cv2.waitKey(30) & 0xFF == 27:
        break

# --- Cleanup ---
cap.release()            # release webcam
cv2.destroyAllWindows()  # close any OpenCV windows
