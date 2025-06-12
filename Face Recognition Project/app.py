

from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
app=Flask(__name__)
camera = cv2.VideoCapture(0)
# Load a sample picture and learn how to recognize it.
Ajay_image = face_recognition.load_image_file("Ajay/Ajay_picture (1).jpg")
Ajay_face_encoding = face_recognition.face_encodings(Ajay_image)[0]

# Load a second sample picture and learn how to recognize it.


# Create arrays of known face encodings and their names
known_face_encodings = [
    Ajay_face_encoding,
    
]
known_face_names = [
    "Ajay"
]
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            try:
                # Get face locations as tuples (top, right, bottom, left)
                face_locations = face_recognition.face_locations(rgb_small_frame)
                
                # Verify all face_locations are tuples, not dlib rectangles
                for loc in face_locations:
                    if not isinstance(loc, tuple):
                        print(f"Warning: face location is not tuple: {loc}")

                # Pass locations to get encodings
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            except Exception as e:
                print("Error getting face encodings:", e)
                face_locations = []
                face_encodings = []

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)

            # Display results on original frame
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True)