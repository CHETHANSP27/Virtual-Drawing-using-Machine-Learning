"""
Hand detection and tracking using MediaPipe
"""
import mediapipe as mp
import cv2
from config.settings import MIN_DETECTION_CONFIDENCE, MIN_TRACKING_CONFIDENCE, MAX_NUM_HANDS, WINDOW_WIDTH, WINDOW_HEIGHT

class HandDetector:
    def __init__(self):
        self.hands = mp.solutions.hands
        self.hand_landmark = self.hands.Hands(
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
            max_num_hands=MAX_NUM_HANDS
        )
        self.draw_utils = mp.solutions.drawing_utils
    
    def detect_hands(self, frame):
        """
        Detect hands in the given frame
        Returns: processed results from MediaPipe
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hand_landmark.process(rgb_frame)
    
    def draw_landmarks(self, frame, hand_landmarks):
        """Draw hand landmarks on the frame"""
        self.draw_utils.draw_landmarks(
            frame, hand_landmarks, self.hands.HAND_CONNECTIONS
        )
    
    def get_finger_positions(self, hand_landmarks):
        """
        Extract finger positions from hand landmarks
        Returns: dict with finger positions
        """
        positions = {}
        positions['index_tip'] = (
            int(hand_landmarks.landmark[8].x * WINDOW_WIDTH),
            int(hand_landmarks.landmark[8].y * WINDOW_HEIGHT)
        )
        positions['middle_tip'] = (
            int(hand_landmarks.landmark[12].x * WINDOW_WIDTH),
            int(hand_landmarks.landmark[12].y * WINDOW_HEIGHT)
        )
        positions['middle_pip'] = (
            int(hand_landmarks.landmark[9].y * WINDOW_HEIGHT)
        )
        return positions
    
    def is_index_raised(self, middle_tip_y, middle_pip_y):
        """Check if index finger is raised based on finger positions"""
        from config.settings import INDEX_FINGER_THRESHOLD
        return (middle_pip_y - middle_tip_y) > INDEX_FINGER_THRESHOLD
