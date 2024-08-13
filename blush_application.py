import cv2
import numpy as np
from face_landmarking import FaceLandmarkDetector

class VirtualBlush:
    def __init__(self):
        self.detector = FaceLandmarkDetector()

    def apply_blush(self, img, color=(255, 192, 203)):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detector(gray)
        for face in faces:
            landmarks = self.detector.predictor(gray, face)
            left_cheek_points = [(landmarks.part(2).x, landmarks.part(2).y),
                                 (landmarks.part(31).x, landmarks.part(31).y),
                                 (landmarks.part(48).x, landmarks.part(48).y)]
            right_cheek_points = [(landmarks.part(14).x, landmarks.part(14).y),
                                  (landmarks.part(35).x, landmarks.part(35).y),
                                  (landmarks.part(54).x, landmarks.part(54).y)]
            cv2.fillPoly(img, [np.array(left_cheek_points, np.int32)], color)
            cv2.fillPoly(img, [np.array(right_cheek_points, np.int32)], color)
        return img

def main():
    cap = cv2.VideoCapture(0)
    blush = VirtualBlush()

    while True:
        ret, frame = cap.read()
        frame = blush.apply_blush(frame)
        cv2.imshow("Virtual Blush", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()