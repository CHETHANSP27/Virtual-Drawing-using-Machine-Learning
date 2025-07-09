"""
Drawing tools and operations for virtual drawing
"""
import cv2
import numpy as np
from config.settings import *

class DrawingTools:
    def __init__(self):
        self.current_tool = "select tool"
        self.var_inits = False
        self.prev_x, self.prev_y = 0, 0
        self.start_x, self.start_y = 0, 0
        
        # Initialize mask for drawing
        self.mask = np.ones((WINDOW_HEIGHT, WINDOW_WIDTH)) * 255
        self.mask = self.mask.astype('uint8')
    
    def get_tool_from_position(self, x):
        """Determine which tool is selected based on x position"""
        relative_x = x - TOOL_MARGIN_LEFT
        
        if relative_x < 50:
            return "line"
        elif relative_x < 100:
            return "rectangle"
        elif relative_x < 150:
            return "draw"
        elif relative_x < 200:
            return "circle"
        else:
            return "erase"
    
    def set_current_tool(self, tool):
        """Set the current drawing tool"""
        self.current_tool = tool
        self.var_inits = False  # Reset initialization state
    
    def draw_line(self, frame, start_pos, end_pos, preview=False):
        """Draw a line on frame or mask"""
        target = frame if preview else self.mask
        color = COLORS["line_preview"] if preview else 0
        cv2.line(target, start_pos, end_pos, color, DEFAULT_THICKNESS)
    
    def draw_rectangle(self, frame, start_pos, end_pos, preview=False):
        """Draw a rectangle on frame or mask"""
        target = frame if preview else self.mask
        color = COLORS["rectangle_preview"] if preview else 0
        cv2.rectangle(target, start_pos, end_pos, color, DEFAULT_THICKNESS)
    
    def draw_circle(self, frame, center, radius, preview=False):
        """Draw a circle on frame or mask"""
        target = frame if preview else self.mask
        color = COLORS["circle_preview"] if preview else COLORS["circle_mask"]
        cv2.circle(target, center, radius, color, DEFAULT_THICKNESS)
    
    def draw_freehand(self, start_pos, end_pos):
        """Draw freehand line on mask"""
        cv2.line(self.mask, start_pos, end_pos, 0, DEFAULT_THICKNESS)
    
    def erase(self, frame, position):
        """Erase at given position"""
        cv2.circle(frame, position, ERASER_RADIUS, COLORS["eraser"], -1)
        cv2.circle(self.mask, position, ERASER_RADIUS, 255, -1)
    
    def process_drawing(self, frame, finger_positions, is_drawing):
        """Process drawing based on current tool and finger positions"""
        x, y = finger_positions['index_tip']
        
        if self.current_tool == "draw":
            if is_drawing:
                self.draw_freehand((self.prev_x, self.prev_y), (x, y))
                self.prev_x, self.prev_y = x, y
            else:
                self.prev_x, self.prev_y = x, y
        
        elif self.current_tool == "line":
            if is_drawing:
                if not self.var_inits:
                    self.start_x, self.start_y = x, y
                    self.var_inits = True
                self.draw_line(frame, (self.start_x, self.start_y), (x, y), preview=True)
            else:
                if self.var_inits:
                    self.draw_line(frame, (self.start_x, self.start_y), (x, y), preview=False)
                    self.var_inits = False
        
        elif self.current_tool == "rectangle":
            if is_drawing:
                if not self.var_inits:
                    self.start_x, self.start_y = x, y
                    self.var_inits = True
                self.draw_rectangle(frame, (self.start_x, self.start_y), (x, y), preview=True)
            else:
                if self.var_inits:
                    self.draw_rectangle(frame, (self.start_x, self.start_y), (x, y), preview=False)
                    self.var_inits = False
        
        elif self.current_tool == "circle":
            if is_drawing:
                if not self.var_inits:
                    self.start_x, self.start_y = x, y
                    self.var_inits = True
                radius = int(((self.start_x - x)**2 + (self.start_y - y)**2)**0.5)
                self.draw_circle(frame, (self.start_x, self.start_y), radius, preview=True)
            else:
                if self.var_inits:
                    radius = int(((self.start_x - x)**2 + (self.start_y - y)**2)**0.5)
                    self.draw_circle(frame, (self.start_x, self.start_y), radius, preview=False)
                    self.var_inits = False
        
        elif self.current_tool == "erase":
            if is_drawing:
                self.erase(frame, (x, y))
    
    def apply_mask_to_frame(self, frame):
        """Apply drawing mask to frame"""
        masked_frame = cv2.bitwise_and(frame, frame, mask=self.mask)
        frame[:, :, 1] = masked_frame[:, :, 1]
        frame[:, :, 2] = masked_frame[:, :, 2]
        return frame
