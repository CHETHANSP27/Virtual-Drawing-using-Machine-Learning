"""
UI helper functions for the virtual drawing application
"""
import cv2
import numpy as np
import os
from config.settings import *

class UIHelpers:
    def __init__(self):
        self.tool_positions = {
            "line": (TOOL_MARGIN_LEFT, 10, TOOL_MARGIN_LEFT + TOOL_WIDTH, 10 + TOOL_HEIGHT),
            "rectangle": (TOOL_MARGIN_LEFT + 50, 10, TOOL_MARGIN_LEFT + 100, 10 + TOOL_HEIGHT),
            "draw": (TOOL_MARGIN_LEFT + 100, 10, TOOL_MARGIN_LEFT + 150, 10 + TOOL_HEIGHT),
            "circle": (TOOL_MARGIN_LEFT + 150, 10, TOOL_MARGIN_LEFT + 200, 10 + TOOL_HEIGHT),
            "erase": (TOOL_MARGIN_LEFT + 200, 10, TOOL_MARGIN_LEFT + 250, 10 + TOOL_HEIGHT),
        }
        
    def load_tools_image(self):
        """Load tools image if available, otherwise return None"""
        try:
            tools_path = os.path.join(os.path.dirname(__file__), '..', 'tools.png')
            if os.path.exists(tools_path):
                return cv2.imread(tools_path)
            return None
        except:
            return None
    
    def draw_ui_elements(self, frame, tools_image, current_tool):
        """Draw UI elements on the frame"""
        # Draw header background
        cv2.rectangle(frame, (0, 0), (WINDOW_WIDTH, UI_HEADER_HEIGHT), COLORS["ui_background"], -1)
        
        # Draw tool boxes
        for tool_name, (x1, y1, x2, y2) in self.tool_positions.items():
            color = COLORS["ui_active"] if tool_name == current_tool else COLORS["ui_text"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Add tool text
            cv2.putText(frame, tool_name, (x1 + 5, y1 + 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        # Draw current tool indicator
        cv2.putText(frame, f"Tool: {current_tool}", (10, WINDOW_HEIGHT - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLORS["ui_text"], 2)
        
        return frame
    
    def handle_tool_selection(self, x, y, get_tool_function):
        """Handle tool selection based on cursor position"""
        selection_indicator = None
        selected_tool = None
        
        # Check if cursor is in tool area
        if y < UI_HEADER_HEIGHT:
            # Check which tool is being pointed at
            for tool_name, (x1, y1, x2, y2) in self.tool_positions.items():
                if x1 <= x <= x2 and y1 <= y <= y2:
                    selected_tool = tool_name
                    # Create selection indicator
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    selection_indicator = (center_x, center_y, 25)
                    break
        
        return selected_tool, selection_indicator
    
    def draw_cursor(self, frame, position, is_drawing=False):
        """Draw cursor at the given position"""
        color = COLORS["ui_active"] if is_drawing else COLORS["ui_text"]
        cv2.circle(frame, position, 5, color, -1)
        return frame