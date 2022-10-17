# import the opencv library
import logging
import time
import cv2
from HandSolver import HandSolver


class HandDetector:

    # The detector itself
    detector = HandSolver()

    # FPS counter
    previousTime = 0
    currentTime = 0
    fps = 0

    # Debug font
    fontType = cv2.FONT_HERSHEY_PLAIN
    fontScale = 1
    fontColor = (255, 255, 0)
    fontColorHighlighted = (255, 0, 255)    
    fontThickness = 1


    def main(self):
        cameraDeviceIndex = 0
        # cv2.VideoCapture(0): Means first camera or webcam.
        # cv2.VideoCapture(1): Means second camera or webcam.
        # cv2.VideoCapture(“file name.mp4”): Means video file

        # define a video capture object
        cap = cv2.VideoCapture(cameraDeviceIndex)
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if not cap.isOpened():
            logging.error('Video capture not opened.')
        else:
            while cap.isOpened():
                # Capture the video frame by frame
                captureSuccessful, frame = cap.read()
                if captureSuccessful:
                    # Detection
                    landmarkResults = self.detector.detect(frame)
                    handsData = self.detector.handsData

                    # Landmarks
                    self.detector.drawLandmarks(frame, landmarkResults)
                    
                    # Debug data
                    self._drawBackground(frame)
                    # FPS counter
                    self._countFps()
                    self._drawFps(frame, self.fps)
                    # Gestures
                    for handData in handsData:
                        self._drawGesture(frame, handData)
                        self._drawFingerCount(frame, handData)
                        self._drawFingerLength(frame, handData)

                    # Display the resulting frame with landmarks
                    cv2.imshow('frame', frame)

                # Get pressed key
                # Returns -1 if no key is pressed
                key = cv2.waitKey(1)
                # Press Esc to quit
                if key == 27:
                    break
            
            # After the loop release the cap object
            cap.release()
            # Destroy all the windows
            cv2.destroyAllWindows()


    def _countFps(self):
        # FPS counter
        self.currentTime = time.time()
        self.fps = 1 / (self.currentTime - self.previousTime)
        self.previousTime = self.currentTime

    def _drawFps(self, image, fps):
        cv2.putText(image, 'FPS:' + str(int(fps)), (10, 30), self.fontType, self.fontScale, self.fontColor, self.fontThickness)

    def _drawGesture(self, image, handData):
        cv2.putText(image, 'Gesture: ' + handData.gestureName(), (10, 60), self.fontType, self.fontScale, self.fontColorHighlighted, self.fontThickness)

    def _drawFingerCount(self, image, handData):
        cv2.putText(image, 'Fingers: ' + str(handData.fingerCount()), (10, 80), self.fontType, self.fontScale, self.fontColorHighlighted, self.fontThickness)

    def _drawFingerLength(self, image, handData):
        # Offset
        x = 10
        y = 110

        cv2.putText(image, 'Thumb: ' + str(handData.thumbFinger.isStretched) + '   ' + ('%.3f' % handData.thumbFinger.length), (x, y + 0), self.fontType, self.fontScale, self.fontColor, self.fontThickness)
        cv2.putText(image, 'Index : ' + str(handData.indexFinger.isStretched) + '   ' + ('%.3f' % handData.indexFinger.length), (x, y + 20), self.fontType, self.fontScale, self.fontColor, self.fontThickness)
        cv2.putText(image, 'Middle: ' + str(handData.middleFinger.isStretched) + '   ' + ('%.3f' % handData.middleFinger.length), (x, y + 40), self.fontType, self.fontScale, self.fontColor, self.fontThickness)
        cv2.putText(image, 'Ring  : ' + str(handData.ringFinger.isStretched) + '   ' + ('%.3f' % handData.ringFinger.length), (x, y + 60), self.fontType, self.fontScale, self.fontColor, self.fontThickness)
        cv2.putText(image, 'Pinky : ' + str(handData.pinkyFinger.isStretched) + '   ' + ('%.3f' % handData.pinkyFinger.length), (x, y + 80), self.fontType, self.fontScale, self.fontColor, self.fontThickness)
    
    def _drawBackground(self, image):
        # Using thickness of -1 px to fill the rectangle
        cv2.rectangle(image, (5, 5), (200, 200), (42, 42, 42), -1)
  

if __name__ == "__main__":
    detector = HandDetector()
    detector.main()
