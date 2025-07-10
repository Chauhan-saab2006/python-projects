import cv2 as cv
import numpy as np

# Load the template image (Messi)
template_path = r'C:\Users\lenovo\Desktop\VS_DATA\face_recog\imges\mess2.jpg'
template = cv.imread(template_path)

if template is None:
    print(f"Error: Template image not found at {template_path}")
    exit()

# Convert to grayscale and resize if needed
template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

# Optional: Resize template if it's too big
# template_gray = cv.resize(template_gray, (100, 100))

w, h = template_gray.shape[::-1]

# Start webcam capture
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    res = cv.matchTemplate(frame_gray, template_gray, cv.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(res >= threshold)

    found = False
    for pt in zip(*loc[::-1]):
        cv.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
        found = True

    label = "Messi" if found else "Unknown Person"
    color = (0, 255, 0) if found else (0, 0, 255)
    cv.putText(frame, label, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Debug: Print match confidence
    min_val, max_val, _, _ = cv.minMaxLoc(res)
    print(f"Match confidence: {max_val:.2f}", end='\r')

    cv.imshow('Camera', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
