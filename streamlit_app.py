# """
# Virtual Drawing Application using Machine Learning - Streamlit Version
# Main application entry point for web deployment
# """
# import streamlit as st
# import cv2
# import numpy as np
# import sys
# import os
# import threading
# import traceback

# # Add project root to path
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# # Import streamlit-webrtc components
# try:
#     from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
#     import av
#     WEBRTC_AVAILABLE = True
# except ImportError as e:
#     st.error(f"WebRTC components not available: {e}")
#     WEBRTC_AVAILABLE = False

# # Import your existing modules with error handling
# try:
#     from core.hand_detector import HandDetector
#     from core.drawing_tools import DrawingTools
#     from utils.ui_helpers import UIHelpers
#     MODULES_AVAILABLE = True
# except ImportError as e:
#     st.error(f"Failed to import modules: {e}")
#     st.error("Please check your project structure and dependencies.")
#     MODULES_AVAILABLE = False

# # Configuration
# WINDOW_WIDTH = 640
# WINDOW_HEIGHT = 480

# # WebRTC configuration for deployment
# RTC_CONFIGURATION = RTCConfiguration(
#     {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
# )

# # Configure Streamlit page
# st.set_page_config(
#     page_title="Virtual Drawing System",
#     page_icon="🎨",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# class VirtualDrawingTransformer(VideoTransformerBase):
#     def __init__(self):
#         if not MODULES_AVAILABLE:
#             raise ImportError("Required modules not available")
            
#         try:
#             self.hand_detector = HandDetector()
#             self.drawing_tools = DrawingTools()
#             self.ui_helpers = UIHelpers()
#             self.tools_image = None
            
#             # Try to load tools image, if it fails, we'll create a simple UI
#             try:
#                 self.tools_image = self.ui_helpers.load_tools_image()
#             except:
#                 self.tools_image = None
            
#             # State management
#             self.frame_lock = threading.Lock()
#             self.current_tool_display = "select tool"
            
#         except Exception as e:
#             st.error(f"Failed to initialize transformer: {e}")
#             raise e
        
#     def transform(self, frame):
#         try:
#             img = frame.to_ndarray(format="bgr24")
            
#             # Resize to standard dimensions
#             img = cv2.resize(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
            
#             # Flip frame horizontally for mirror effect
#             img = cv2.flip(img, 1)
            
#             with self.frame_lock:
#                 # Detect hands
#                 results = self.hand_detector.detect_hands(img)
                
#                 if results.multi_hand_landmarks:
#                     for hand_landmarks in results.multi_hand_landmarks:
#                         # Draw hand landmarks
#                         self.hand_detector.draw_landmarks(img, hand_landmarks)
                        
#                         # Get finger positions
#                         finger_positions = self.hand_detector.get_finger_positions(hand_landmarks)
#                         x, y = finger_positions['index_tip']
                        
#                         # Handle tool selection
#                         selected_tool, selection_indicator = self.ui_helpers.handle_tool_selection(
#                             x, y, self.drawing_tools.get_tool_from_position
#                         )
                        
#                         if selected_tool:
#                             self.drawing_tools.set_current_tool(selected_tool)
#                             self.current_tool_display = selected_tool
                        
#                         # Check if user is drawing (index finger raised)
#                         is_drawing = self.hand_detector.is_index_raised(
#                             finger_positions['middle_tip'][1],
#                             finger_positions['middle_pip']
#                         )
                        
#                         # Process drawing
#                         self.drawing_tools.process_drawing(img, finger_positions, is_drawing)
                        
#                         # Draw selection indicator if active
#                         if selection_indicator:
#                             x_sel, y_sel, radius = selection_indicator
#                             cv2.circle(img, (x_sel, y_sel), radius, (0, 255, 255), 2)
                
#                 # Apply drawing mask to frame
#                 img = self.drawing_tools.apply_mask_to_frame(img)
                
#                 # Draw UI elements
#                 self.ui_helpers.draw_ui_elements(
#                     img, self.tools_image, self.drawing_tools.current_tool
#                 )
                
#                 # Add simple tool indicator if tools_image not available
#                 if self.tools_image is None:
#                     cv2.putText(img, f"Tool: {self.drawing_tools.current_tool}", 
#                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
#             return img
            
#         except Exception as e:
#             # Return error frame
#             error_img = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
#             cv2.putText(error_img, f"Error: {str(e)}", (10, 50), 
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
#             return error_img
    
#     def clear_canvas(self):
#         """Clear the drawing canvas"""
#         try:
#             with self.frame_lock:
#                 self.drawing_tools.mask = np.ones((WINDOW_HEIGHT, WINDOW_WIDTH)) * 255
#                 self.drawing_tools.mask = self.drawing_tools.mask.astype('uint8')
#                 self.drawing_tools.var_inits = False
#         except Exception as e:
#             st.error(f"Failed to clear canvas: {e}")

# def main():
#     # Custom CSS for better styling
#     st.markdown("""
#     <style>
#     .main-header {
#         font-size: 2.5rem;
#         font-weight: bold;
#         color: #1e88e5;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .tool-info {
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         padding: 1rem;
#         border-radius: 10px;
#         color: white;
#         text-align: center;
#         margin: 1rem 0;
#     }
#     .status-success {
#         background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
#         padding: 0.5rem;
#         border-radius: 5px;
#         color: white;
#         text-align: center;
#     }
#     .status-error {
#         background: linear-gradient(90deg, #ff6b6b 0%, #ffa726 100%);
#         padding: 0.5rem;
#         border-radius: 5px;
#         color: white;
#         text-align: center;
#     }
#     .error-box {
#         background: #fff3cd;
#         border: 1px solid #ffeaa7;
#         border-radius: 5px;
#         padding: 1rem;
#         margin: 1rem 0;
#     }
#     </style>
#     """, unsafe_allow_html=True)
    
#     # Main header
#     st.markdown('<div class="main-header">🎨 Virtual Drawing System</div>', unsafe_allow_html=True)
    
#     # Check if all dependencies are available
#     if not MODULES_AVAILABLE:
#         st.markdown("""
#         <div class="error-box">
#         <h3>❌ Module Import Error</h3>
#         <p>Some required modules could not be imported. Please check:</p>
#         <ul>
#             <li>All files are in the correct directory structure</li>
#             <li>All dependencies are installed</li>
#             <li>Python path is configured correctly</li>
#         </ul>
#         </div>
#         """, unsafe_allow_html=True)
#         return
    
#     if not WEBRTC_AVAILABLE:
#         st.markdown("""
#         <div class="error-box">
#         <h3>❌ WebRTC Not Available</h3>
#         <p>WebRTC components are not available. Please install streamlit-webrtc:</p>
#         <code>pip install streamlit-webrtc</code>
#         </div>
#         """, unsafe_allow_html=True)
#         return
    
#     # Create transformer instance
#     try:
#         if 'transformer' not in st.session_state:
#             st.session_state.transformer = VirtualDrawingTransformer()
#     except Exception as e:
#         st.error(f"Failed to initialize the drawing system: {e}")
#         st.error("Please check your configuration and try again.")
#         return
    
#     # Sidebar controls
#     with st.sidebar:
#         st.header("🛠️ Drawing Controls")
        
#         # Tool selection
#         st.subheader("Select Tool")
#         tool_options = ["select tool", "line", "rectangle", "draw", "circle", "erase"]
#         selected_tool = st.selectbox("Choose your tool:", tool_options)
        
#         # Update tool in transformer
#         if selected_tool != "select tool":
#             st.session_state.transformer.drawing_tools.set_current_tool(selected_tool)
        
#         # Clear canvas button
#         if st.button("🗑️ Clear Canvas", type="primary"):
#             st.session_state.transformer.clear_canvas()
#             st.success("Canvas cleared!")
        
#         # Instructions
#         st.markdown("---")
#         st.subheader("📋 Instructions")
#         st.markdown("""
#         1. **Start Camera**: Click 'Start' below
#         2. **Select Tool**: Choose from sidebar or gesture
#         3. **Draw**: Raise index finger to draw
#         4. **Stop Drawing**: Lower index finger
#         5. **Clear**: Use clear button when needed
#         """)
        
#         # Current tool display
#         current_tool = st.session_state.transformer.drawing_tools.current_tool
#         st.markdown(f"""
#         <div class="tool-info">
#             <strong>Current Tool:</strong><br>
#             {current_tool.upper()}
#         </div>
#         """, unsafe_allow_html=True)
    
#     # Main content area
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         st.subheader("📹 Camera Feed")
        
#         # WebRTC streamer
#         try:
#             webrtc_ctx = webrtc_streamer(
#                 key="virtual-drawing",
#                 video_processor_factory=lambda: st.session_state.transformer,
#                 rtc_configuration=RTC_CONFIGURATION,
#                 media_stream_constraints={"video": True, "audio": False},
#                 async_processing=True,
#             )
            
#             # Status display
#             if webrtc_ctx.state.playing:
#                 st.markdown('<div class="status-success">✅ Camera Active - Ready to Draw!</div>', 
#                            unsafe_allow_html=True)
#             else:
#                 st.markdown('<div class="status-error">❌ Camera Inactive - Click START to begin</div>', 
#                            unsafe_allow_html=True)
                
#         except Exception as e:
#             st.error(f"WebRTC Error: {e}")
#             st.error("Please check your internet connection and browser permissions.")
    
#     with col2:
#         st.subheader("🎨 Features")
        
#         # Feature list
#         features = [
#             "✋ Hand Gesture Recognition",
#             "🖊️ Multiple Drawing Tools",
#             "📏 Line & Shape Drawing",
#             "🎨 Free-hand Drawing",
#             "🗑️ Eraser Tool",
#             "🔄 Real-time Processing",
#             "🖥️ Web-based Interface"
#         ]
        
#         for feature in features:
#             st.markdown(f"- {feature}")
        
#         # Tips
#         st.markdown("---")
#         st.subheader("💡 Tips")
#         st.markdown("""
#         - Ensure good lighting
#         - Keep hand in frame
#         - Use smooth movements
#         - Try different tools
#         - Have fun creating!
#         """)
    
#     # Footer
#     st.markdown("---")
#     st.markdown("""
#     <div style='text-align: center; color: #666; padding: 1rem;'>
#         <p>Virtual Drawing System - Powered by MediaPipe & Streamlit</p>
#         <p>Move your hand to control, raise index finger to draw!</p>
#     </div>
#     """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

"""
Virtual Drawing Application using Machine Learning - Streamlit Version
Main application entry point for web deployment
"""
import streamlit as st
import cv2
import numpy as np
import sys
import os
import threading
import traceback

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import streamlit-webrtc components
try:
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
    import av
    WEBRTC_AVAILABLE = True
except ImportError as e:
    st.error(f"WebRTC components not available: {e}")
    WEBRTC_AVAILABLE = False

# Import your existing modules with error handling
try:
    from core.hand_detector import HandDetector
    from core.drawing_tools import DrawingTools
    from utils.ui_helpers import UIHelpers
    MODULES_AVAILABLE = True
except ImportError as e:
    st.error(f"Failed to import modules: {e}")
    st.error("Please check your project structure and dependencies.")
    MODULES_AVAILABLE = False

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
        if not MODULES_AVAILABLE:
            raise ImportError("Required modules not available")
            
        try:
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
            
        except Exception as e:
            st.error(f"Failed to initialize transformer: {e}")
            raise e
        
    def transform(self, frame):
        try:
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
            
        except Exception as e:
            # Return error frame
            error_img = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
            cv2.putText(error_img, f"Error: {str(e)}", (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            return error_img
    
    def clear_canvas(self):
        """Clear the drawing canvas"""
        try:
            with self.frame_lock:
                self.drawing_tools.mask = np.ones((WINDOW_HEIGHT, WINDOW_WIDTH)) * 255
                self.drawing_tools.mask = self.drawing_tools.mask.astype('uint8')
                self.drawing_tools.var_inits = False
        except Exception as e:
            st.error(f"Failed to clear canvas: {e}")

def initialize_session_state():
    """Initialize session state variables"""
    if 'transformer_initialized' not in st.session_state:
        st.session_state.transformer_initialized = False
    
    if 'transformer' not in st.session_state:
        st.session_state.transformer = None
    
    if 'current_tool' not in st.session_state:
        st.session_state.current_tool = "select tool"

def get_transformer():
    """Get or create transformer instance"""
    if not st.session_state.transformer_initialized:
        try:
            if MODULES_AVAILABLE:
                st.session_state.transformer = VirtualDrawingTransformer()
                st.session_state.transformer_initialized = True
            else:
                st.error("Cannot initialize transformer - modules not available")
                return None
        except Exception as e:
            st.error(f"Failed to initialize transformer: {e}")
            return None
    
    return st.session_state.transformer

def main():
    # Initialize session state first
    initialize_session_state()
    
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
    .error-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<div class="main-header">🎨 Virtual Drawing System</div>', unsafe_allow_html=True)
    
    # Check if all dependencies are available
    if not MODULES_AVAILABLE:
        st.markdown("""
        <div class="error-box">
        <h3>❌ Module Import Error</h3>
        <p>Some required modules could not be imported. Please check:</p>
        <ul>
            <li>All files are in the correct directory structure</li>
            <li>All dependencies are installed</li>
            <li>Python path is configured correctly</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        return
    
    if not WEBRTC_AVAILABLE:
        st.markdown("""
        <div class="error-box">
        <h3>❌ WebRTC Not Available</h3>
        <p>WebRTC components are not available. Please install streamlit-webrtc:</p>
        <code>pip install streamlit-webrtc</code>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Get transformer instance
    transformer = get_transformer()
    
    if transformer is None:
        st.error("Failed to initialize the drawing system. Please refresh the page.")
        return
    
    # Sidebar controls
    with st.sidebar:
        st.header("🛠️ Drawing Controls")
        
        # Tool selection
        st.subheader("Select Tool")
        tool_options = ["select tool", "line", "rectangle", "draw", "circle", "erase"]
        selected_tool = st.selectbox("Choose your tool:", tool_options, key="tool_selector")
        
        # Update tool in transformer and session state
        if selected_tool != "select tool" and transformer:
            transformer.drawing_tools.set_current_tool(selected_tool)
            st.session_state.current_tool = selected_tool
        
        # Clear canvas button
        if st.button("🗑️ Clear Canvas", type="primary"):
            if transformer:
                transformer.clear_canvas()
                st.success("Canvas cleared!")
            else:
                st.error("Transformer not available")
        
        # Instructions
        st.markdown("---")
        st.subheader("📋 Instructions")
        st.markdown("""
        1. **Start Camera**: Click 'Start' below
        2. **Select Tool**: Choose from sidebar or gesture by raising index finger
        3. **Draw**: Raise index and middle finger to draw
        4. **Stop Drawing**: Lower index and middle finger
        5. **Clear**: Use clear button when needed
        """)
        
        # Current tool display
        current_tool = st.session_state.current_tool
        if transformer:
            current_tool = transformer.drawing_tools.current_tool
        
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
        try:
            webrtc_ctx = webrtc_streamer(
                key="virtual-drawing",
                video_processor_factory=lambda: transformer,
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
                
        except Exception as e:
            st.error(f"WebRTC Error: {e}")
            st.error("Please check your internet connection and browser permissions.")
            # Show debug info
            st.markdown("**Debug Info:**")
            st.write(f"Transformer available: {transformer is not None}")
            st.write(f"Session state keys: {list(st.session_state.keys())}")
    
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
        
        # Debug section (remove in production)
        if st.checkbox("Show Debug Info"):
            st.markdown("**Debug Information:**")
            st.write(f"MODULES_AVAILABLE: {MODULES_AVAILABLE}")
            st.write(f"WEBRTC_AVAILABLE: {WEBRTC_AVAILABLE}")
            st.write(f"Transformer initialized: {st.session_state.transformer_initialized}")
            st.write(f"Current tool: {st.session_state.current_tool}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Virtual Drawing System - Powered by MediaPipe & Streamlit</p>
        <p>Move your hand to control, raise index and middle finger to draw!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()