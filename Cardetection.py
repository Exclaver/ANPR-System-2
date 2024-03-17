
import time
from ultralytics import YOLO
import cv2
import cvzone
import math
import datetime
import ocr
import json
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import requests
import json

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://number-plate-detection-56492-default-rtdb.asia-southeast1.firebasedatabase.app",

})

start_time = datetime.datetime.now()
prev_seconds = 0
ThresholdStopTime = 4


def process_plate_image(img):
    global prev_plate_pos, stopped_frames, count, scanner, prev_seconds, prevsecond

    results = model(img, stream=True)

    now = datetime.datetime.now()

    # Process each detection result
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))
            conf = math.ceil((box.conf[0] * 100)) / 100

            cls = int(box.cls[0])
            cvzone.putTextRect(
                img, f'{classNames[cls]}{conf}', (max(0, x1), max(35, y1-50)))

            # Check if the plate is stationary
            if prev_plate_pos is not None and (abs(x1 - prev_plate_pos[0]) < 10 and abs(y1 - prev_plate_pos[1]) < 10):
                stopped_frames += 1
            else:
                stopped_frames = 0

            # Save the cropped image when the car comes to a stop
            seconds_passed = (now - start_time).total_seconds()

            if stopped_frames > 5 and seconds_passed - prev_seconds >= ThresholdStopTime:  # Adjust the threshold as needed
                # Crop the region of interest (ROI) containing the number plate
                plate_roi = img[y1:y2, x1:x2]
                # Save the cropped image
                plate_image_filename = f"plates/scaned_img_{now.strftime('%H_%M_%S')}.jpg"
                cv2.imwrite(plate_image_filename, plate_roi)
                count += 1
                stopped_frames = 0
                scanner = True
                prev_seconds = seconds_passed

                # Start OCR processing in a separate thread
                ocr_thread = threading.Thread(
                    target=perform_ocr, args=(plate_image_filename,))
                ocr_thread.start()

            prev_plate_pos = (x1, y1)


def perform_ocr(plate_image_filename):
    global prev_plate_pos

    test_file = ocr.ocr_space_file(
        filename=plate_image_filename, language='eng')
    data = json.loads(test_file)
    parsed_text = data["ParsedResults"][0]["ParsedText"]
    print("Parsed Text:", parsed_text)
    ref = db.reference(f'Cars/{parsed_text}').get()
    if (ref):
        with open("scanned_plates.txt", "a") as file:
            # Write text to the file
            file.write(
                f'{parsed_text} Date and Time: {str(datetime.datetime.now())}\n')
            file.write(f'{ref}\n\n')
    else:
        ref2 = db.reference('/Cars')

        new_data = {
            parsed_text: {
                "name": "henry Doe",
                "NumPlate": "ABC1234",
                "Credits": 80
            }
        }
        ref2.update(new_data)
        with open("scanned_plates.txt", "a") as file:
            # Write text to the file
            file.write(
                f'{parsed_text} Date and Time: {str(datetime.datetime.now())}\n')
            file.write(f'{ref2}\n\n')


model = YOLO('yolo-weights/Plates1.pt')
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

classNames = ["plate"]

# Initialize variables for tracking motion and stopping
prev_plate_pos = None
stopped_frames = 0
count = 0
scanner = False
prevsecond = 0
while True:
    scanner = False
    success, img = cap.read()
    process_plate_image(img)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
