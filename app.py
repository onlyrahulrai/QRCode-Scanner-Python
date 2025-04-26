import requests
import json
import cv2


def sendDataToServer(payload):
    try:
        url = "http://127.0.0.1:5000/api/attendance/business/"
        bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NzYwMTgwNGQ0ODFlNGYxNWJhMWZiZmUiLCJtb2JpbGUiOiI5OTk5OTk5OTk5Iiwicm9sZSI6eyJpZCI6IjY3ODU0MDA3MzIyMjQ5ZWI1YTI2YWY3NSIsIm5hbWUiOiJCdXNpbmVzcyIsIm9yZGVyIjoyfSwiaWF0IjoxNzQ1NjUyNDQyLCJleHAiOjE3NDgyNDQ0NDJ9.zjgGqab76Ch06-XpWNTBi2cZlokDbCIMwzTFBn-_Djk"

        payload = {
            "business": "6760230dd481e4f15ba1fc19",
            "payload": payload
        }

        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print("Error: ", e)

# Initialize the QRCode detector
detector = cv2.QRCodeDetector()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect and decode
    data, bbox, _ = detector.detectAndDecode(frame)

    if bbox is not None:
        # Draw bounding box around QR code
        for i in range(len(bbox)):
            pt1 = tuple(map(int, bbox[i][0]))
            pt2 = tuple(map(int, bbox[(i+1) % len(bbox)][0]))
            cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

        if data:
            # Print and display the result
            print(f"QR Code detected: {data}")

            sendDataToServer(data)

            cv2.putText(frame, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow('Fast QR Code Scanner', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
