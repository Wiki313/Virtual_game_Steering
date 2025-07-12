# VirtualSteering
Project Title: Virtual Steering Control System Using Hand Gestures
Description:
This project presents an innovative and intuitive virtual steering system that allows users to control directional movement using hand gestures detected via a webcam. The system is developed using Python with OpenCV and MediaPipe for real-time hand tracking and gesture recognition.

How It Works:
A webcam captures real-time video input.

MediaPipe's hand tracking model detects and tracks both hands, extracting key landmark positions such as the wrist and thumb tip.

Based on the geometric positions and movements of the wrists and thumbs:

The system determines the direction (left, right, forward, or reverse).

Specific hand postures like a thumbs-up gesture are interpreted as acceleration (right hand) or braking (left hand).

Detected directions are mapped to keyboard keys (w, a, s, d) using the pynput library to simulate vehicle movement in a game or simulation.

Features:
Hands-Free Driving Control: Users steer virtually using only hand movements.

Gesture-Based Acceleration and Braking: Right thumb = accelerate, left thumb = brake.

Direction Control: Lateral wrist movement calculates the turn angle and triggers left or right steering.

Live Feedback Overlay: Real-time instructions (e.g., "Turn Left", "Accelerate") are displayed on the video frame.

Applications:
Driving simulators or educational tools.

Virtual reality or gaming input systems.

Accessibility tools for users with mobility challenges.

Technologies Used:
Python

OpenCV – For video processing and visualization.

MediaPipe – For real-time hand landmark detection.

pynput – For simulating keyboard inputs.

Requirements:
Copy
Edit
opencv-python
mediapipe


