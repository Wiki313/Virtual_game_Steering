"""
Hand tracking and gesture recognition module.
Uses MediaPipe for hand detection and extracts steering gestures.
"""

import math
import cv2
import mediapipe as mp
import config


class HandTracker:
    """
    Tracks hands via webcam and recognizes steering gestures.
    """
    
    def __init__(self):
        """Initialize MediaPipe hands and drawing utilities."""
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        
        self.hands = self.mp_hands.Hands(
            model_complexity=config.MODEL_COMPLEXITY,
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE,
            max_num_hands=config.MAX_NUM_HANDS
        )
        
        # Drawing specs for landmarks
        self.landmark_spec = self.mp_drawing.DrawingSpec(
            color=(121, 22, 76), thickness=2, circle_radius=4
        )
        self.connection_spec = self.mp_drawing.DrawingSpec(
            color=(250, 44, 250), thickness=2, circle_radius=2
        )
    
    def process_frame(self, image: cv2.Mat) -> tuple:
        """
        Process a single video frame for hand detection.
        
        Args:
            image: BGR image from OpenCV
            
        Returns:
            Tuple of (processed_image, hand_data)
            hand_data contains wrist positions and thumb states
        """
        image.flags.writeable = False
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_image)
        
        image.flags.writeable = True
        output_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        
        hand_data = {
            'wrists': [],
            'thumbs_up_right': False,
            'thumbs_up_left': False,
            'num_hands': 0
        }
        
        if results.multi_hand_landmarks:
            hand_data['num_hands'] = len(results.multi_hand_landmarks)
            
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, 
                results.multi_handedness
            ):
                hand_label = handedness.classification[0].label
                
                # Draw landmarks
                if config.SHOW_LANDMARKS:
                    self.mp_drawing.draw_landmarks(
                        output_image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.landmark_spec,
                        self.connection_spec
                    )
                
                # Extract wrist position
                wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                h, w, _ = output_image.shape
                wrist_px = self.mp_drawing._normalized_to_pixel_coordinates(
                    wrist.x, wrist.y, w, h
                )
                
                if wrist_px is not None:
                    hand_data['wrists'].append({
                        'position': list(wrist_px),
                        'label': hand_label
                    })
                
                # Detect thumb-up gesture
                thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP]
                
                thumb_distance = math.sqrt(
                    (thumb_tip.x - thumb_ip.x) ** 2 + 
                    (thumb_tip.y - thumb_ip.y) ** 2
                )
                
                if thumb_distance < config.THUMB_DISTANCE_THRESHOLD:
                    if hand_label == 'Right':
                        hand_data['thumbs_up_right'] = True
                    elif hand_label == 'Left':
                        hand_data['thumbs_up_left'] = True
        
        return output_image, hand_data
    
    def calculate_steering(self, wrists: list) -> dict:
        """
        Calculate steering direction based on wrist positions.
        
        Args:
            wrists: List of wrist position dictionaries
            
        Returns:
            Dictionary with steering info: {
                'action': str,  # 'left', 'right', 'straight', 'none'
                'angle': float,
                'center': tuple
            }
        """
        if len(wrists) != 2:
            return {'action': 'none', 'angle': 0, 'center': (0, 0)}
        
        co = [w['position'] for w in wrists]
        
        # Calculate center point
        xm = (co[0][0] + co[1][0]) / 2
        ym = (co[0][1] + co[1][1]) / 2
        
        # Calculate slope
        dx = co[1][0] - co[0][0]
        dy = co[1][1] - co[0][1]
        
        if abs(dx) < 1:  # Avoid division by zero
            return {'action': 'straight', 'angle': 0, 'center': (xm, ym)}
        
        # Determine direction based on wrist positions
        left_wrist = co[0] if co[0][0] < co[1][0] else co[1]
        right_wrist = co[1] if co[0][0] < co[1][0] else co[0]
        
        # Check steering conditions
        if right_wrist[1] - left_wrist[1] > config.STEER_ANGLE_THRESHOLD:
            return {'action': 'left', 'angle': dy/dx, 'center': (xm, ym)}
        
        if left_wrist[1] - right_wrist[1] > config.STEER_ANGLE_THRESHOLD:
            return {'action': 'right', 'angle': dy/dx, 'center': (xm, ym)}
        
        return {'action': 'straight', 'angle': dy/dx, 'center': (xm, ym)}
    
    def draw_steering_wheel(self, image: cv2.Mat, center: tuple, action: str) -> cv2.Mat:
        """
        Draw steering wheel visualization on the image.
        
        Args:
            image: OpenCV image
            center: Center point of the wheel
            action: Current steering action
            
        Returns:
            Image with steering wheel drawn
        """
        cx, cy = int(center[0]), int(center[1])
        radius = config.WHEEL_RADIUS
        
        # Draw outer circle
        cv2.circle(
            img=image,
            center=(cx, cy),
            radius=radius,
            color=config.WHEEL_COLOR,
            thickness=config.WHEEL_THICKNESS
        )
        
        # Draw action text
        text_map = {
            'left': 'Turn Left',
            'right': 'Turn Right',
            'straight': 'Keep Straight',
            'backward': 'Reverse',
            'none': 'No Hands Detected'
        }
        text = text_map.get(action, action)
        
        cv2.putText(
            image, text, (33, 33),
            config.OVERLAY_FONT,
            config.OVERLAY_FONT_SCALE,
            config.OVERLAY_COLOR,
            config.OVERLAY_THICKNESS,
            cv2.LINE_AA
        )
        
        return image
    
    def draw_debug_info(self, image: cv2.Mat, fps: float, num_hands: int) -> cv2.Mat:
        """
        Draw debug information on the image.
        
        Args:
            image: OpenCV image
            fps: Current frames per second
            num_hands: Number of hands detected
            
        Returns:
            Image with debug info
        """
        if not config.SHOW_DEBUG_INFO:
            return image
        
        debug_text = f"FPS: {fps:.1f} | Hands: {num_hands}"
        cv2.putText(
            image, debug_text, (10, image.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1
        )
        return image
    
    def close(self):
        """Release MediaPipe resources."""
        self.hands.close()
