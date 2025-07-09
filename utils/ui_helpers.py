"""
UI helper functions for the virtual drawing application
"""
import cv2
import time
from config.settings import *

class UIHelpers:
    def __init__(self):
        self.time_init = True
        self.selection_radius = SELECTION_RADIUS
        self.selection_start_time = 0
    
    def load_tools_image(self):
        """Load and return tools image"""
        try:
            tools = cv2.imread("tools.png")
            if tools is not None:
                return tools.astype('uint8')
        except:
            pass
        
        # Create default tools image if file not found
        tools = self.create_default_tools_image()
        return tools
    
    def create_default_tools_image(self):
        """Create a default tools selection image"""
        tools = cv2.rectangle(
            np.zeros((TOOL_AREA_HEIGHT + 5, TOOL_AREA_WIDTH - TOOL_MARGIN_LEFT + 5, 3), dtype="uint8"),
            (0, 0), (TOOL_AREA_WIDTH - TOOL_MARGIN_LEFT, TOOL_AREA_HEIGHT), (0, 0, 255), 2
        )
        
        # Add tool separators
        for i, pos in enumerate([50, 100, 150, 200]):
            cv2.line(tools, (pos, 0), (pos, TOOL_AREA_HEIGHT), (0, 0, 255), 2)
        
        return tools
    
    def handle_tool_selection(self, x, y, get_tool_callback):
        """Handle tool selection with timer"""
        if x < TOOL_AREA_WIDTH and y < TOOL_AREA_HEIGHT and x > TOOL_MARGIN_LEFT:
            if self.time_init:
                self.selection_start_time = time.time()
                self.time_init = False
            
            current_time = time.time()
            
            # Show selection indicator
            remaining_time = SELECTION_TIME_THRESHOLD - (current_time - self.selection_start_time)
            if remaining_time > 0:
                self.selection_radius = int(SELECTION_RADIUS * (remaining_time / SELECTION_TIME_THRESHOLD))
                return None, (x, y, self.selection_radius)
            else:
                # Selection complete
                selected_tool = get_tool_callback(x)
                self.time_init = True
                self.selection_radius = SELECTION_RADIUS
                return selected_tool, None
        else:
            self.time_init = True
            self.selection_radius = SELECTION_RADIUS
            return None, None
    
    def draw_ui_elements(self, frame, tools_image, current_tool, selection_indicator=None):
        """Draw all UI elements on the frame"""
        # Add tools overlay
        frame[:TOOL_AREA_HEIGHT, TOOL_MARGIN_LEFT:TOOL_AREA_WIDTH] = cv2.addWeighted(
            tools_image, 0.7, 
            frame[:TOOL_AREA_HEIGHT, TOOL_MARGIN_LEFT:TOOL_AREA_WIDTH], 0.3, 0
        )
        
        # Show selection indicator
        if selection_indicator:
            x, y, radius = selection_indicator
            cv2.circle(frame, (x, y), radius, COLORS["selection_circle"], 2)
        
        # Show current tool
        cv2.putText(
            frame, current_tool, 
            (270 + TOOL_MARGIN_LEFT, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, COLORS["text"], 2
        )
