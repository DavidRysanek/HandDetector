from enum import Enum


class FingerData():
    isStretched = False
    length = 0


class HandData():
    landmarks = None

    thumbFinger = FingerData()
    indexFinger = FingerData()
    middleFinger = FingerData()
    ringFinger = FingerData()
    pinkyFinger = FingerData()


    def fingerCount(self):
        count = 0
        count += 1 if self.thumbFinger.isStretched else 0
        count += 1 if self.indexFinger.isStretched else 0
        count += 1 if self.middleFinger.isStretched else 0
        count += 1 if self.ringFinger.isStretched else 0
        count += 1 if self.pinkyFinger.isStretched else 0
        return count


    def gesture(self):
        fingers = self.fingerCount()

        if fingers == 1:
            if self.thumbFinger.isStretched:
                return HandGesture.ThumbUp
            elif self.indexFinger.isStretched:
                return HandGesture.Pointing
            elif self.middleFinger.isStretched:
                return HandGesture.MiddleFinger
            elif self.ringFinger.isStretched:
                return HandGesture.Married
            elif self.pinkyFinger.isStretched:
                return HandGesture.PinkySwear

        elif fingers == 2:
            if self.indexFinger.isStretched and self.middleFinger.isStretched:
                return HandGesture.Victory
            elif self.indexFinger.isStretched and self.pinkyFinger.isStretched:
                return HandGesture.RockTwo

        elif fingers == 3:
            if self.indexFinger.isStretched and self.pinkyFinger.isStretched and self.thumbFinger.isStretched:
                return HandGesture.RockThree
            elif self.indexFinger.isStretched and self.middleFinger.isStretched and self.ringFinger.isStretched:
                return HandGesture.ThreeAmericans

        elif fingers == 5:
            return HandGesture.AllFingers
            
        return HandGesture.Unknown


    def gestureName(self):
        return self._gestureName(self.gesture())

    def _gestureName(self, gesture):
        if gesture is gesture.Fist:
            return 'Fist'
        elif gesture is gesture.ThumbUp:
            return 'Thumbs up'
        elif gesture is gesture.Pointing:
            return 'Pointing'
        elif gesture is gesture.MiddleFinger:
            return 'F*ck you'
        elif gesture is gesture.Married:
            return 'Married'
        elif gesture is gesture.PinkySwear:
            return 'Pinky swear'
        elif gesture is gesture.Victory:
            return 'Victory'
        elif gesture is gesture.RockTwo:
            return 'Rock you'
        elif gesture is gesture.RockThree:
            return 'Hard rock'
        elif gesture is gesture.ThreeAmericans:
            return '3 americans'
        elif gesture is gesture.AllFingers:
            return 'All fingers'
        else:
            return 'Unknown'


class HandGesture(Enum):
    Unknown = 0
    # No finger
    Fist = 1
    # 1 finger
    ThumbUp = 2
    Pointing = 3
    MiddleFinger = 4
    Married = 5
    PinkySwear = 6
    # 2 fingers
    Victory = 7
    RockTwo = 8
    # 3 fingers
    RockThree = 9
    ThreeAmericans = 10
    # 5 fingers
    AllFingers = 11
