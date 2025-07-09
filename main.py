"""
Virtual Drawing Application using Machine Learning
Main application entry point
"""
import cv2
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.hand_detector import HandDetector
from core.drawing_tools import DrawingTools
from utils.ui_helpers import UIHelpers
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT

class VirtualDrawingApp:
    def __init__(self):
        self.hand_detector = HandDetector()
        self.drawing_tools = DrawingTools()
        self.ui_helpers = UIHelpers()
        self.tools_image = self.ui_helpers.load_tools_image()
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")
    
    def run(self):
        """Main application loop"""
        print("Virtual Drawing Application Started")
        print("Press ESC to exit")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read from camera")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect hands
            results = self.hand_detector.detect_hands(frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.hand_detector.draw_landmarks(frame, hand_landmarks)
                    
                    # Get finger positions
                    finger_positions = self.hand_detector.get_finger_positions(hand_landmarks)
                    x, y = finger_positions['index_tip']
                    
                    # Handle tool selection
                    selected_tool, selection_indicator = self.ui_helpers.handle_tool_selection(
                        x, y, self.drawing_tools.get_tool_from_position
                    )
                    
                    if selected_tool:
                        self.drawing_tools.set_current_tool(selected_tool)
                        print(f"Tool selected: {selected_tool}")
                    
                    # Check if user is drawing (index finger raised)
                    is_drawing = self.hand_detector.is_index_raised(
                        finger_positions['middle_tip'][1],
                        finger_positions['middle_pip']
                    )
                    
                    # Process drawing
                    self.drawing_tools.process_drawing(frame, finger_positions, is_drawing)
                    
                    # Draw selection indicator if active
                    if selection_indicator:
                        x_sel, y_sel, radius = selection_indicator
                        cv2.circle(frame, (x_sel, y_sel), radius, (0, 255, 255), 2)
            
            # Apply drawing mask to frame
            frame = self.drawing_tools.apply_mask_to_frame(frame)
            
            # Draw UI elements
            self.ui_helpers.draw_ui_elements(
                frame, self.tools_image, self.drawing_tools.current_tool
            )
            
            # Display frame
            cv2.imshow("Virtual Drawing App", frame)
            
            # Check for exit
            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("Application closed")

if __name__ == "__main__":
    try:
        app = VirtualDrawingApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
