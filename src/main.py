"""
Virtual Game Steering - Main Application Entry Point

A hands-free driving control system using real-time hand gesture recognition.
Steer with wrist movement, accelerate with right thumb, brake with left thumb.

Usage:
    python src/main.py

Press 'Q' to exit.
"""

import time
import cv2
from hand_tracker import HandTracker
from key_mapper import KeyMapper
import config


def initialize_camera() -> cv2.VideoCapture:
    """
    Initialize and configure the webcam.
    
    Returns:
        Configured VideoCapture object
        
    Raises:
        RuntimeError: If camera cannot be opened
    """
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    
    if not cap.isOpened():
        raise RuntimeError(
            f"Cannot open camera at index {config.CAMERA_INDEX}. "
            "Try changing CAMERA_INDEX in config.py (0, 1, 2, etc.)"
        )
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, config.FPS_LIMIT)
    
    print(f"Camera initialized: {config.FRAME_WIDTH}x{config.FRAME_HEIGHT}")
    return cap


def main():
    """Main application loop."""
    print("=" * 50)
    print("  Virtual Game Steering")
    print("  Hands-Free Driving Control")
    print("=" * 50)
    print("\nControls:")
    print("  - Both hands: Steering")
    print("  - Right thumb up: Accelerate")
    print("  - Left thumb up: Brake")
    print("  - One hand: Reverse")
    print("  - Press 'Q' to exit\n")
    
    # Initialize components
    try:
        cap = initialize_camera()
    except RuntimeError as e:
        print(f"Error: {e}")
        return
    
    tracker = HandTracker()
    key_mapper = KeyMapper()
    
    # FPS calculation
    prev_time = 0
    fps = 0
    
    try:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Warning: Failed to read frame from camera.")
                continue
            
            # Calculate FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time) if prev_time > 0 else 0
            prev_time = current_time
            
            # Process frame
            processed_image, hand_data = tracker.process_frame(image)
            
            # Determine action
            steering = tracker.calculate_steering(hand_data['wrists'])
            action = steering['action']
            
            # Map gestures to keyboard inputs
            if action == 'left':
                key_mapper.steer_left()
                print("Turn left")
                
            elif action == 'right':
                key_mapper.steer_right()
                print("Turn right")
                
            elif action == 'straight':
                key_mapper.go_straight()
                print("Keeping straight")
                
            elif action == 'none' and hand_data['num_hands'] == 1:
                key_mapper.go_backward()
                print("Keeping back")
                action = 'backward'
            
            # Handle thumb gestures (accelerate/brake override)
            if hand_data['thumbs_up_right'] and not hand_data['thumbs_up_left']:
                key_mapper.accelerate()
                print("Accelerate")
                cv2.putText(
                    processed_image, "Accelerate", (25, 25),
                    config.OVERLAY_FONT, config.OVERLAY_FONT_SCALE,
                    config.OVERLAY_COLOR, config.OVERLAY_THICKNESS, cv2.LINE_AA
                )
                
            if hand_data['thumbs_up_left'] and not hand_data['thumbs_up_right']:
                key_mapper.brake()
                print("Brake")
                cv2.putText(
                    processed_image, "Brake", (50, 150),
                    config.OVERLAY_FONT, config.OVERLAY_FONT_SCALE,
                    config.OVERLAY_COLOR, config.OVERLAY_THICKNESS, cv2.LINE_AA
                )
            
            # Draw visual feedback
            if action != 'none':
                processed_image = tracker.draw_steering_wheel(
                    processed_image, steering['center'], action
                )
            
            processed_image = tracker.draw_debug_info(
                processed_image, fps, hand_data['num_hands']
            )
            
            # Display
            display_image = cv2.flip(processed_image, 1) if config.FLIP_IMAGE else processed_image
            cv2.imshow('Virtual Game Steering', display_image)
            
            # Exit on 'Q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nExiting...")
                break
                
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    
    finally:
        # Cleanup
        key_mapper.release_all()
        tracker.close()
        cap.release()
        cv2.destroyAllWindows()
        print("Resources released. Goodbye!")


if __name__ == "__main__":
    main()
