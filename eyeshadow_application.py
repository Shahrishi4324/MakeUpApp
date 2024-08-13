import cv2
import numpy as np
from face_landmarking import FaceLandmarkDetector

class VirtualEyeshadow:
    def __init__(self):
        self.detector = FaceLandmarkDetector()

    def apply_eyeshadow(self, img, color=(128, 0, 128)):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detector(gray)
        for face in faces:
            landmarks = self.detector.predictor(gray, face)
            left_eye_points = []
            for i in range(36, 42):
                x = landmarks.part(i).x
                y = landmarks.part(i).y
                left_eye_points.append((x, y))
            right_eye_points = []
            for i in range(42, 48):
                x = landmarks.part(i).x
                y = landmarks.part(i).y
                right_eye_points.append((x, y))
            left_eye_points = np.array(left_eye_points, np.int32)
            right_eye_points = np.array(right_eye_points, np.int32)
            cv2.fillPoly(img, [left_eye_points], color)
            cv2.fillPoly(img, [right_eye_points], color)
        return img

def main():
    cap = cv2.VideoCapture(0)
    eyeshadow = VirtualEyeshadow()

    while True:
        ret, frame = cap.read()
        frame = eyeshadow.apply_eyeshadow(frame)
        cv2.imshow("Virtual Eyeshadow", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()