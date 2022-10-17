import cv2
import mediapipe as mp
import math
from HandData import HandData


class HandSolver():
    mpHands = mp.solutions.hands
    mpDrawing = mp.solutions.drawing_utils
    mpDrawingStyles = mp.solutions.drawing_styles
 
    results = None
    handsData = []

    
    def __init__(self):
        # model_complexity: 0, 1, or 2.
        # As the model complexity of the model increases the landmark accuracy and latency increase.
        # The default value is 1.
        self.model = self.mpHands.Hands(
            # model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
            

    def detect(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False
        # "results" contains positions of tracked fingers
        results = self.model.process(image)
        self.results = results
        
        self.handsData = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                handData = HandData()
                handData.landmarks = hand_landmarks
                self._detectFingers(handData)
                self.handsData.append(handData)

        return results


    def _detectFingers(self, handData):
        if not handData.landmarks:
            return

        handLandmarks = handData.landmarks
        mpHandLandmark = self.mpHands.HandLandmark
 
        handData.thumbFinger.length = self._fingerLength(handLandmarks, mpHandLandmark.THUMB_TIP)
        handData.indexFinger.length = self._fingerLength(handLandmarks, mpHandLandmark.INDEX_FINGER_TIP)
        handData.middleFinger.length = self._fingerLength(handLandmarks, mpHandLandmark.MIDDLE_FINGER_TIP)
        handData.ringFinger.length = self._fingerLength(handLandmarks, mpHandLandmark.RING_FINGER_TIP)
        handData.pinkyFinger.length = self._fingerLength(handLandmarks, mpHandLandmark.PINKY_TIP)
        
        # TODO: Length is absolute. i.e. the closer the hand is to the camera, the bigger the number (length) is
        handData.thumbFinger.isStretched = True if handData.thumbFinger.length > 0.3 else False
        handData.indexFinger.isStretched = True if handData.indexFinger.length > 0.15 else False
        handData.middleFinger.isStretched = True if handData.middleFinger.length> 0.15 else False
        handData.ringFinger.isStretched = True if handData.ringFinger.length > 0.15 else False
        handData.pinkyFinger.isStretched = True if handData.pinkyFinger.length > 0.15 else False


    def _fingerLength(self, handLandmarks, fingerTip):
        l = handLandmarks.landmark

        width = l[fingerTip].x - l[fingerTip - 3].x
        height = l[fingerTip].y - l[fingerTip - 3].y

        return math.sqrt(width ** 2 + height ** 2)



    def drawLandmarks(self, image, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self._drawHandLandmarks(image, hand_landmarks)
    
    def _drawHandLandmarks(self, image, handLandmarks):
        image.flags.writeable = True
        self.mpDrawing.draw_landmarks(
            image,
            handLandmarks,
            self.mpHands.HAND_CONNECTIONS,
            self.mpDrawingStyles.get_default_hand_landmarks_style(),
            self.mpDrawingStyles.get_default_hand_connections_style())
                                