"""
Configuration settings for Virtual Game Steering.
Edit these values to customize the application behavior.
"""

# Camera settings
CAMERA_INDEX = 0          # 0 = default webcam, try 1, 2, etc. if multiple cameras
FRAME_WIDTH = 1280        # Camera resolution width
FRAME_HEIGHT = 720        # Camera resolution height
FPS_LIMIT = 30            # Target frames per second

# MediaPipe hand detection settings
MIN_DETECTION_CONFIDENCE = 0.5    # Minimum confidence for hand detection (0.0 - 1.0)
MIN_TRACKING_CONFIDENCE = 0.5     # Minimum confidence for hand tracking (0.0 - 1.0)
MODEL_COMPLEXITY = 0              # 0 = lite, 1 = full, 2 = heavy (slower but more accurate)
MAX_NUM_HANDS = 2                 # Maximum number of hands to detect

# Gesture detection thresholds
THUMB_DISTANCE_THRESHOLD = 0.04   # Distance threshold for thumb-up detection
STEER_ANGLE_THRESHOLD = 65        # Minimum pixel difference for steering detection
STEERING_DEADZONE = 20            # Deadzone to prevent jitter when hands are centered

# Visual settings
SHOW_LANDMARKS = True             # Draw hand skeleton on video
SHOW_DEBUG_INFO = True            # Show FPS and hand count on screen
FLIP_IMAGE = True                 # Mirror the camera feed (selfie view)
OVERLAY_FONT = 0                  # 0 = HERSHEY_SIMPLEX
OVERLAY_FONT_SCALE = 0.8          # Text size for overlay
OVERLAY_COLOR = (0, 255, 0)       # Green text for overlay
OVERLAY_THICKNESS = 2             # Text thickness

# Steering wheel visualization
WHEEL_RADIUS = 150                # Radius of steering wheel overlay
WHEEL_COLOR = (195, 255, 62)      # Lime green wheel color
WHEEL_THICKNESS = 15              # Wheel line thickness

# Key mapping (customize for different games)
KEY_FORWARD = 'w'
KEY_BACKWARD = 's'
KEY_LEFT = 'a'
KEY_RIGHT = 'd'
