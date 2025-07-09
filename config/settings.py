"""
Configuration settings for Virtual Drawing Application
"""

# Display settings
WINDOW_WIDTH = 640  # Changed back to 640 to match camera standard resolution
WINDOW_HEIGHT = 480

# Tool selection area
TOOL_MARGIN_LEFT = 150
TOOL_AREA_WIDTH = 250 + TOOL_MARGIN_LEFT
TOOL_AREA_HEIGHT = 50

# Hand detection settings
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6
MAX_NUM_HANDS = 1

# Drawing settings
DEFAULT_THICKNESS = 4
SELECTION_RADIUS = 40
SELECTION_TIME_THRESHOLD = 0.8
INDEX_FINGER_THRESHOLD = 40
ERASER_RADIUS = 30

# Tool positions (relative to tool area)
TOOL_POSITIONS = {
    "line": 50,
    "rectangle": 100,
    "draw": 150,
    "circle": 200,
    "erase": 250
}

# Colors (BGR format)
COLORS = {
    "selection_circle": (0, 255, 255),
    "line_preview": (50, 152, 255),
    "rectangle_preview": (0, 255, 255),
    "circle_preview": (255, 255, 0),
    "circle_mask": (0, 255, 0),
    "text": (0, 0, 255),
    "eraser": (0, 0, 0)
}

# Debug settings (add these to help troubleshoot)
DEBUG_MODE = True
PRINT_DIMENSIONS = True

# Mask initialization settings
MASK_DTYPE = 'uint8'
MASK_INITIAL_VALUE = 255
