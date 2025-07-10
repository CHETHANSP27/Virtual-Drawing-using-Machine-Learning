"""
Virtual Drawing Application using Machine Learning - Streamlit Version
Main application entry point for web deployment
"""
import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av
import sys
import os
import threading
import queue

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your existing modules
from core.hand_detector import HandDetector
from core.drawing_tools import DrawingTools
from utils.ui_helpers import UIHelpers

# Configuration
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# WebRTC configuration for deployment
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Configure Streamlit page
st.set_page_config(
    page_title="Virtual Drawing System",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

class VirtualDrawingTransformer(VideoTransformerBase):
    def __init__(self):
        self.hand_detector = HandDetector()
        self.drawing_tools = DrawingTools()
        self.ui_helpers = UIHelpers()
        self.tools_image = None
        
        # Try to load tools image, if it fails, we'll create a simple UI
        try:
            self.tools_image = self.ui_helpers.load_tools_image()
        except:
            self.tools_image = None
        
        # State management
        self.frame_lock = threading.Lock()
        self.current_tool_display = "select tool"
        
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Resize to standard dimensions
        img = cv2.resize(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Flip frame horizontally for mirror effect
        img = cv2.flip(img, 1)
        
        with self.frame_lock:
            # Detect hands
            results = self.hand_detector.detect_hands(img)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.hand_detector.draw_landmarks(img, hand_landmarks)
                    
                    # Get finger positions
                    finger_positions = self.hand_detector.get_finger_positions(hand_landmarks)
                    x, y = finger_positions['index_tip']
                    
                    # Handle tool selection
                    selected_tool, selection_indicator = self.ui_helpers.handle_tool_selection(
                        x, y, self.drawing_tools.get_tool_from_position
                    )
                    
                    if selected_tool:
                        self.drawing_tools.set_current_tool(selected_tool)
                        self.current_tool_display = selected_tool
                    
                    # Check if user is drawing (index finger raised)
                    is_drawing = self.hand_detector.is_index_raised(
                        finger_positions['middle_tip'][1],
                        finger_positions['middle_pip']
                    )
                    
                    # Process drawing
                    self.drawing_tools.process_drawing(img, finger_positions, is_drawing)
                    
                    # Draw selection indicator if active
                    if selection_indicator:
                        x_sel, y_sel, radius = selection_indicator
                        cv2.circle(img, (x_sel, y_sel), radius, (0, 255, 255), 2)
            
            # Apply drawing mask to frame
            img = self.drawing_tools.apply_mask_to_frame(img)
            
            # Draw UI elements
            self.ui_helpers.draw_ui_elements(
                img, self.tools_image, self.drawing_tools.current_tool
            )
            
            # Add simple tool indicator if tools_image not available
            if self.tools_image is None:
                cv2.putText(img, f"Tool: {self.drawing_tools.current_tool}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return img
    
    def clear_canvas(self):
        """Clear the drawing canvas"""
        with self.frame_lock:
            self.drawing_tools.mask = np.ones((WINDOW_HEIGHT, WINDOW_WIDTH)) * 255
            self.drawing_tools.mask = self.drawing_tools.mask.astype('uint8')
            self.drawing_tools.var_inits = False

def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e88e5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .tool-info {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .status-success {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 0.5rem;
        border-radius: 5px;
        color: white;
        text-align: center;
    }
    .status-error {
        background: linear-gradient(90deg, #ff6b6b 0%, #ffa726 100%);
        padding: 0.5rem;
        border-radius: 5px;
        color: white;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<div class="main-header">🎨 Virtual Drawing System</div>', unsafe_allow_html=True)
    
    # Create transformer instance
    if 'transformer' not in st.session_state:
        st.session_state.transformer = VirtualDrawingTransformer()
    
    # Sidebar controls
    with st.sidebar:
        st.header("🛠️ Drawing Controls")
        
        # Tool selection
        st.subheader("Select Tool")
        tool_options = ["select tool", "line", "rectangle", "draw", "circle", "erase"]
        selected_tool = st.selectbox("Choose your tool:", tool_options)
        
        # Update tool in transformer
        if selected_tool != "select tool":
            st.session_state.transformer.drawing_tools.set_current_tool(selected_tool)
        
        # Clear canvas button
        if st.button("🗑️ Clear Canvas", type="primary"):
            st.session_state.transformer.clear_canvas()
            st.success("Canvas cleared!")
        
        # Instructions
        st.markdown("---")
        st.subheader("📋 Instructions")
        st.markdown("""
        1. **Start Camera**: Click 'Start' below
        2. **Select Tool**: Choose from sidebar or gesture
        3. **Draw**: Raise index finger to draw
        4. **Stop Drawing**: Lower index finger
        5. **Clear**: Use clear button when needed
        """)
        
        # Gesture Guide
        st.markdown("---")
        st.subheader("✋ Gesture Guide")
        st.markdown("""
        - **Index Finger Up**: Drawing mode
        - **Index Finger Down**: Navigation mode
        - **Point to Tool Area**: Select tools
        - **Move Hand**: Control cursor
        """)
        
        # Current tool display
        current_tool = st.session_state.transformer.drawing_tools.current_tool
        st.markdown(f"""
        <div class="tool-info">
            <strong>Current Tool:</strong><br>
            {current_tool.upper()}
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📹 Camera Feed")
        
        # WebRTC streamer
        webrtc_ctx = webrtc_streamer(
            key="virtual-drawing",
            video_transformer_factory=lambda: st.session_state.transformer,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )
        
        # Status display
        if webrtc_ctx.state.playing:
            st.markdown('<div class="status-success">✅ Camera Active - Ready to Draw!</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-error">❌ Camera Inactive - Click START to begin</div>', 
                       unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎨 Features")
        
        # Feature list
        features = [
            "✋ Hand Gesture Recognition",
            "🖊️ Multiple Drawing Tools",
            "📏 Line & Shape Drawing",
            "🎨 Free-hand Drawing",
            "🗑️ Eraser Tool",
            "🔄 Real-time Processing",
            "🖥️ Web-based Interface"
        ]
        
        for feature in features:
            st.markdown(f"- {feature}")
        
        # System status
        st.markdown("---")
        st.subheader("📊 System Status")
        
        if webrtc_ctx.state.playing:
            st.success("🟢 Camera: Active")
            st.success("🟢 Hand Detection: Ready")
            st.success("🟢 Drawing Tools: Loaded")
        else:
            st.error("🔴 Camera: Inactive")
            st.warning("🟡 Hand Detection: Waiting")
            st.warning("🟡 Drawing Tools: Standby")
        
        # Tips
        st.markdown("---")
        st.subheader("💡 Tips")
        st.markdown("""
        - Ensure good lighting
        - Keep hand in frame
        - Use smooth movements
        - Try different tools
        - Have fun creating!
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Virtual Drawing System - Powered by MediaPipe & Streamlit</p>
        <p>Move your hand to control, raise index finger to draw!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()