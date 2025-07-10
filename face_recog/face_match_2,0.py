import cv2
from deepface import DeepFace

# Load reference image
reference_path = r"C:\Users\lenovo\Desktop\VS_DATA\face_recog\imges\ron.jpg"
reference_img = cv2.imread(reference_path)
if reference_img is None:
    print("Could not load reference image!")
    exit()

# Start webcam
cap = cv2.VideoCapture(0)
counter = 0
face_found = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Check every 30 frames for efficiency
    if counter % 30 == 0:
        try:
            result = DeepFace.verify(frame, reference_img, enforce_detection=False)
            if result['verified']:
                print("ron")
                face_found = True
            else:
                face_found = False
        except Exception:
            face_found = False

    counter += 1

    # Optional: Show result on frame
    label = "ron" if face_found else "not ron"
    color = (0, 255, 0) if face_found else (0, 0, 255)
    cv2.putText(frame, label, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)
    cv2.imshow("video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()