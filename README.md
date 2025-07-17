# Virtual Drawing using Machine Learning

A computer vision-based virtual drawing application that allows users to draw in the air using hand gestures. The application uses MediaPipe for hand detection and OpenCV for real-time video processing and drawing operations.

🌐 **Live Demo**: [Click to Try the App](https://virtual-drawing-using-machine-learning-production.up.railway.app/)  
📂 **GitHub Repo**: [CHETHANSP27/Virtual-Drawing-using-Machine-Learning](https://github.com/CHETHANSP27/Virtual-Drawing-using-Machine-Learning)

## Features

- **Real-time Hand Detection**: Uses MediaPipe for accurate hand landmark detection with 21 hand landmarks
- **Multiple Drawing Tools**: 
  - Freehand drawing
  - Line drawing
  - Rectangle drawing
  - Circle drawing
  - Eraser tool
- **Gesture-based Tool Selection**: Select tools by hovering over tool icons with timer-based confirmation
- **Air Drawing**: Draw in the air using index finger movements with gesture recognition
- **Real-time Preview**: See drawing shapes before finalizing them
- **Scalable Window Size**: Configurable window dimensions from 640x480 to 1280x720 or larger
- **Smart Coordinate Scaling**: Automatic scaling between camera resolution and display resolution

## Project Structure

```
Virtual-Drawing-using-Machine-Learning/
├── config/
│   └── settings.py          # Configuration settings (display, camera, scaling)
├── core/
│   ├── hand_detector.py     # Hand detection and tracking with MediaPipe
│   └── drawing_tools.py     # Drawing operations and tools management
├── utils/
│   └── ui_helpers.py        # UI helper functions and tool selection
├── main.py                  # Main application entry point with scaling support
├── requirements.txt         # Project dependencies
├── README.md               # Project documentation
└── tools.png              # Optional: Tool icons image
```

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- Webcam/Camera (640x480 minimum resolution)
- Windows/macOS/Linux
- Minimum 4GB RAM recommended for smooth performance

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Virtual-Drawing-using-Machine-Learning
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import cv2, mediapipe, numpy; print('All dependencies installed successfully!')"
```

## Running the Application

### Basic Usage

```bash
python main.py
```

### Using the Application

1. **Start the Application**: Run `python main.py`
2. **Position Your Hand**: Hold your hand in front of the camera (arm's length distance)
3. **Select Tools**: 
   - Hover your index finger over the tool selection area (top-left)
   - Wait for the yellow circle to shrink completely (0.8 seconds) to select a tool
   - Current tool name will be displayed on screen
4. **Draw**: 
   - Raise your index finger (keep middle finger down) to start drawing
   - Move your index finger to draw
   - Lower your index finger to stop drawing
5. **Preview Mode**: For shapes (line, rectangle, circle), see real-time preview before finalizing
6. **Exit**: Press the ESC key to close the application

### Available Tools

- **Line**: Draw straight lines between two points
- **Rectangle**: Draw rectangles by defining corners
- **Draw**: Freehand drawing with continuous lines
- **Circle**: Draw circles by defining center and radius
- **Erase**: Erase drawings with circular eraser tool

### Gesture Controls

- **Index Finger Up + Middle Finger Down**: Drawing/Active mode
- **Index Finger Down**: Stop drawing/Inactive mode
- **Hover in Tool Area**: Tool selection mode (with timer)

## Configuration

The application can be customized by modifying `config/settings.py`:

### Display Settings
```python
WINDOW_WIDTH = 640          # Camera feed width
WINDOW_HEIGHT = 480         # Camera feed height
```

### Hand Detection Settings
```python
MIN_DETECTION_CONFIDENCE = 0.6    # Minimum confidence for hand detection (0.1-1.0)
MIN_TRACKING_CONFIDENCE = 0.6     # Minimum confidence for hand tracking (0.1-1.0)
MAX_NUM_HANDS = 1                  # Maximum number of hands to detect
```

### Drawing Settings
```python
DEFAULT_THICKNESS = 4              # Default drawing line thickness
SELECTION_TIME_THRESHOLD = 0.8     # Time to hold for tool selection (seconds)
INDEX_FINGER_THRESHOLD = 40        # Sensitivity for finger gesture detection
ERASER_RADIUS = 30                 # Eraser tool radius
SELECTION_RADIUS = 50              # Tool selection indicator radius
```

### Color Customization
```python
COLORS = {
    "selection_circle": (0, 255, 255),    # Yellow selection indicator
    "line_preview": (50, 152, 255),       # Orange line preview
    "rectangle_preview": (0, 255, 255),   # Yellow rectangle preview
    "circle_preview": (255, 255, 0),      # Cyan circle preview
    "text": (0, 0, 255),                  # Red text
    "eraser": (0, 0, 0)                   # Black eraser
}
```

## Troubleshooting

### Common Issues

1. **OpenCV Dimension Error**
   ```
   Error: (-215:Assertion failed) (mtype == CV_8U || mtype == CV_8S) && _mask.sameSize(*psrc1)
   ```
   - **Solution**: Ensure `WINDOW_WIDTH` and `WINDOW_HEIGHT` match your camera's actual resolution or enable proper scaling
   - Check that mask dimensions match frame dimensions

2. **MediaPipe Warning**
   ```
   Using NORM_RECT without IMAGE_DIMENSIONS is only supported for the square ROI
   ```
   - **Solution**: This is a warning and doesn't affect functionality. Ensure camera is properly initialized

3. **Camera Not Working**
   - Ensure your camera is not being used by another application
   - Try changing the camera index: `cv2.VideoCapture(1)` instead of `cv2.VideoCapture(0)`
   - Check camera permissions in system settings

4. **Hand Detection Not Working**
   - Ensure good lighting conditions (avoid backlighting)
   - Keep your hand clearly visible in the camera frame
   - Maintain distance of 1-3 feet from camera
   - Adjust `MIN_DETECTION_CONFIDENCE` (try 0.5 for better detection)

5. **Tool Selection Not Responsive**
   - Ensure you're hovering over the correct tool area (top-left corner)
   - Wait for the full selection time (default 0.8 seconds)
   - Check if your hand is properly detected (landmarks should be visible)
   - Try adjusting `SELECTION_TIME_THRESHOLD` to 0.5 for faster selection

6. **Drawing Not Working**
   - Make sure you're raising your index finger while keeping other fingers down
   - Adjust `INDEX_FINGER_THRESHOLD` (try 30 for more sensitivity, 50 for less)
   - Ensure proper lighting and hand visibility

7. **Window Too Small/Large**
   - Modify `WINDOW_WIDTH` and `WINDOW_HEIGHT` in `config/settings.py`
   - Common resolutions: 640x480, 1280x720, 1920x1080
   - Ensure your display supports the chosen resolution

### Performance Optimization

- Close other applications using the camera
- Ensure good lighting for better hand detection
- Use a dedicated GPU if available for better performance
- Lower `MIN_DETECTION_CONFIDENCE` slightly if detection is slow
- Reduce window size if experiencing lag

### Debug Mode

Enable debug mode in `config/settings.py`:
```python
DEBUG_MODE = True
PRINT_DIMENSIONS = True
```

This will print frame and mask dimensions to help troubleshoot dimension mismatch issues.

## Technical Details

### Hand Detection
- Uses MediaPipe Hands solution for real-time hand landmark detection
- Tracks 21 hand landmarks for precise gesture recognition
- Optimized for single-hand detection with configurable confidence thresholds
- Supports coordinate scaling between camera and display resolutions

### Drawing Algorithm
- Uses OpenCV for all drawing operations with hardware acceleration
- Maintains a binary mask for persistent drawings
- Implements real-time preview for shape tools
- Supports variable thickness and colors

### Gesture Recognition
- Index finger tip (landmark 8) for drawing position
- Middle finger landmarks (9, 12) for drawing state detection
- Custom algorithm for finger-up/down detection with configurable sensitivity
- Timer-based tool selection to prevent accidental switches

### Scaling System
- Automatic coordinate transformation between camera and display space
- Supports different aspect ratios and resolutions
- Maintains drawing accuracy across different window sizes

## System Requirements

### Minimum Requirements
- Python 3.7+
- 2GB RAM
- Webcam (480p)
- CPU: Dual-core 2.0GHz

### Recommended Requirements
- Python 3.8+
- 4GB RAM
- Webcam (720p or higher)
- CPU: Quad-core 2.5GHz
- GPU: Integrated graphics or better

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MediaPipe team for the excellent hand detection solution
- OpenCV community for computer vision tools and documentation
- Contributors and beta testers
- Python community for the robust ecosystem

## Future Enhancements

- [ ] Color palette for drawing tools
- [ ] Save/load drawing functionality (PNG, JPG export)
- [ ] Multiple hand support for collaborative drawing
- [ ] Advanced gesture recognition (pinch, zoom, rotate)
- [ ] 3D drawing capabilities with depth sensing
- [ ] Mobile app version (Android/iOS)
- [ ] Voice commands for tool selection
- [ ] Drawing layers and undo/redo functionality
- [ ] Custom brush shapes and textures
- [ ] Network multiplayer drawing sessions

## Changelog

### Version 2.0
- Added scalable window support (640x480 to 1280x720+)
- Improved coordinate scaling system
- Enhanced error handling and debugging
- Better tool selection with visual feedback
- Optimized performance for larger windows

### Version 1.0
- Initial release with basic drawing functionality
- Hand detection and gesture recognition
- Five drawing tools (line, rectangle, circle, draw, erase)
- Real-time preview system

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the configuration options in `config/settings.py`
3. Enable debug mode for detailed error information
4. Open an issue on GitHub with:
   - Your system specifications
   - Python version
   - Error messages (if any)
   - Steps to reproduce the issue

## FAQ

**Q: Why is my drawing lagging?**
A: Try reducing the window size, closing other applications, or lowering the detection confidence.

**Q: Can I use multiple hands?**
A: Currently, the application is optimized for single-hand use. Multi-hand support is planned for future versions.

**Q: How do I change drawing colors?**
A: Currently, drawing is in black. Color selection is planned for the next version. You can modify colors in `config/settings.py`.

**Q: Can I save my drawings?**
A: Save functionality is not implemented yet but is planned for future updates.

---

**Happy Drawing! 🎨✨**
