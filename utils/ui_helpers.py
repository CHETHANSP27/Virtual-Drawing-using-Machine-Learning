# """
# UI helper functions for the virtual drawing application
# """
# import cv2
# import time
# from config.settings import *

# class UIHelpers:
#     def __init__(self):
#         self.time_init = True
#         self.selection_radius = SELECTION_RADIUS
#         self.selection_start_time = 0
    
#     def load_tools_image(self):
#         """Load and return tools image"""
#         try:
#             tools = cv2.imread("tools.png")
#             if tools is not None:
#                 return tools.astype('uint8')
#         except:
#             pass
        
#         # Create default tools image if file not found
#         tools = self.create_default_tools_image()
#         return tools
    
#     def create_default_tools_image(self):
#         """Create a default tools selection image"""
#         tools = cv2.rectangle(
#             np.zeros((TOOL_AREA_HEIGHT + 5, TOOL_AREA_WIDTH - TOOL_MARGIN_LEFT + 5, 3), dtype="uint8"),
#             (0, 0), (TOOL_AREA_WIDTH - TOOL_MARGIN_LEFT, TOOL_AREA_HEIGHT), (0, 0, 255), 2
#         )
        
#         # Add tool separators
#         for i, pos in enumerate([50, 100, 150, 200]):
#             cv2.line(tools, (pos, 0), (pos, TOOL_AREA_HEIGHT), (0, 0, 255), 2)
        
#         return tools
    
#     def handle_tool_selection(self, x, y, get_tool_callback):
#         """Handle tool selection with timer"""
#         if x < TOOL_AREA_WIDTH and y < TOOL_AREA_HEIGHT and x > TOOL_MARGIN_LEFT:
#             if self.time_init:
#                 self.selection_start_time = time.time()
#                 self.time_init = False
            
#             current_time = time.time()
            
#             # Show selection indicator
#             remaining_time = SELECTION_TIME_THRESHOLD - (current_time - self.selection_start_time)
#             if remaining_time > 0:
#                 self.selection_radius = int(SELECTION_RADIUS * (remaining_time / SELECTION_TIME_THRESHOLD))
#                 return None, (x, y, self.selection_radius)
#             else:
#                 # Selection complete
#                 selected_tool = get_tool_callback(x)
#                 self.time_init = True
#                 self.selection_radius = SELECTION_RADIUS
#                 return selected_tool, None
#         else:
#             self.time_init = True
#             self.selection_radius = SELECTION_RADIUS
#             return None, None
    
#     def draw_ui_elements(self, frame, tools_image, current_tool, selection_indicator=None):
#         """Draw all UI elements on the frame"""
#         # Add tools overlay
#         frame[:TOOL_AREA_HEIGHT, TOOL_MARGIN_LEFT:TOOL_AREA_WIDTH] = cv2.addWeighted(
#             tools_image, 0.7, 
#             frame[:TOOL_AREA_HEIGHT, TOOL_MARGIN_LEFT:TOOL_AREA_WIDTH], 0.3, 0
#         )
        
#         # Show selection indicator
#         if selection_indicator:
#             x, y, radius = selection_indicator
#             cv2.circle(frame, (x, y), radius, COLORS["selection_circle"], 2)
        
#         # Show current tool
#         cv2.putText(
#             frame, current_tool, 
#             (270 + TOOL_MARGIN_LEFT, 30), 
#             cv2.FONT_HERSHEY_SIMPLEX, 1, COLORS["text"], 2
#         )

"""
UI helpers for virtual drawing application
Streamlit-compatible version
"""
import cv2
import numpy as np
import os
from config.settings import *

class UIHelpers:
    def __init__(self):
        self.selection_counter = 0
        self.selected_tool = None
        self.selection_start_time = 0
        
    def load_tools_image(self):
        """Load tools image, create simple version if not found"""
        try:
            tools_path = os.path.join(os.path.dirname(__file__), '..', 'tools.png')
            if os.path.exists(tools_path):
                return cv2.imread(tools_path)
            else:
                # Create a simple tools image
                return self.create_simple_tools_image()
        except Exception as e:
            print(f"Could not load tools image: {e}")
            return self.create_simple_tools_image()
    
    def create_simple_tools_image(self):
        """Create a simple tools image programmatically"""
        # Create white background
        img = np.ones((TOOL_MAX_Y, TOOL_MAX_X, 3), dtype=np.uint8) * 255
        
        # Draw tool icons
        tools = ["LINE", "RECT", "DRAW", "CIRCLE", "ERASE"]
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 0, 0)]
        
        for i, (tool, color) in enumerate(zip(tools, colors)):
            x_pos = 25 + i * 50
            y_pos = 25
            
            # Draw simple icon
            cv2.rectangle(img, (x_pos - 20, y_pos - 15), (x_pos + 20, y_pos + 15), color, 2)
            
            # Add text
            cv2.putText(img, tool[:4], (x_pos - 15, y_pos + 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)
        
        return img
    
    def handle_tool_selection(self, x, y, get_tool_function):
        """Handle tool selection with timing"""
        selection_indicator = None
        selected_tool = None
        
        # Check if cursor is in tool area
        if (TOOL_MARGIN_LEFT <= x <= TOOL_MARGIN_LEFT + TOOL_MAX_X and 
            TOOL_MARGIN_TOP <= y <= TOOL_MARGIN_TOP + TOOL_MAX_Y):
            
            current_tool = get_tool_function(x)
            
            # Check if same tool is being selected
            if current_tool == self.selected_tool:
                self.selection_counter += 1
                # Show selection indicator
                selection_indicator = (x, y, SELECTION_RADIUS)
                
                # Tool selected after holding for required frames
                if self.selection_counter >= SELECTION_FRAMES:
                    selected_tool = current_tool
                    self.selection_counter = 0
                    self.selected_tool = None
            else:
                # Different tool selected, reset counter
                self.selected_tool = current_tool
                self.selection_counter = 1
                selection_indicator = (x, y, SELECTION_RADIUS)
        else:
            # Not in tool area, reset selection
            self.selection_counter = 0
            self.selected_tool = None
        
        return selected_tool, selection_indicator
    
    def draw_ui_elements(self, frame, tools_image, current_tool):
        """Draw UI elements on frame"""
        try:
            if tools_image is not None:
                # Draw tools area
                h, w = tools_image.shape[:2]
                roi = frame[TOOL_MARGIN_TOP:TOOL_MARGIN_TOP + h, 
                           TOOL_MARGIN_LEFT:TOOL_MARGIN_LEFT + w]
                
                # Blend tools image with frame
                tools_gray = cv2.cvtColor(tools_image, cv2.COLOR_BGR2GRAY)
                mask = cv2.threshold(tools_gray, 240, 255, cv2.THRESH_BINARY)[1]
                mask_inv = cv2.bitwise_not(mask)
                
                # Apply mask
                roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
                tools_fg = cv2.bitwise_and(tools_image, tools_image, mask=mask_inv)
                
                # Combine
                result = cv2.add(roi_bg, tools_fg)
                frame[TOOL_MARGIN_TOP:TOOL_MARGIN_TOP + h, 
                      TOOL_MARGIN_LEFT:TOOL_MARGIN_LEFT + w] = result
            
            # Draw current tool indicator
            cv2.putText(frame, f"Current Tool: {current_tool.upper()}", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 255, 0), 2)
            
            # Draw instructions
            cv2.putText(frame, "Raise index finger to draw", 
                       (10, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (255, 255, 255), 1)
            
        except Exception as e:
            print(f"Error drawing UI elements: {e}")
            # Fallback: just draw current tool
            cv2.putText(frame, f"Tool: {current_tool}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)