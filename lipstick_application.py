import cv2
import numpy as np
from face_landmarking import FaceLandmarkDetector

class VirtualLipstick:
    def __init__(self):
        self.detector = FaceLandmarkDetector()

    def apply_lipstick(self, img, color=(0, 0, 255)):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detector(gray)
        for face in faces:
            landmarks = self.detector.predictor(gray, face)
            lips_points = []
            for i in range(48, 61):
                x = landmarks.part(i).x
                y = landmarks.part(i).y
                lips_points.append((x, y))
            lips_points = np.array(lips_points, np.int32)
            cv2.fillPoly(img, [lips_points], color)
        return img

def main():
    cap = cv2.VideoCapture(0)
    lipstick = VirtualLipstick()

    while True:
        ret, frame = cap.read()
        frame = lipstick.apply_lipstick(frame)
        cv2.imshow("Virtual Lipstick", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()