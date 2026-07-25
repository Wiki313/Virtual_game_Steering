# 🎮 Virtual Game Steering

<p align="center">
  <a href="https://github.com/Wiki313/Virtual_game_Steering/stargazers">
    <img src="https://img.shields.io/github/stars/Wiki313/Virtual_game_Steering?style=social" alt="Stars"/>
  </a>
  <a href="https://github.com/Wiki313/Virtual_game_Steering/network/members">
    <img src="https://img.shields.io/github/forks/Wiki313/Virtual_game_Steering?style=social" alt="Forks"/>
  </a>
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python"/>
  <img src="https://img.shields.io/badge/OpenCV-4.x-green.svg" alt="OpenCV"/>
  <img src="https://img.shields.io/badge/MediaPipe-0.10+-orange.svg" alt="MediaPipe"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"/>
</p>

> **Hands-free driving control using real-time hand gesture recognition.**
>
> Steer with wrist movement, accelerate with your right thumb, and brake with your left thumb — no physical controller needed!

---

## ✨ Features

- 🖐️ **Hands-Free Steering** — Control direction using wrist movement
- ⬆️ **Gesture Acceleration** — Right thumb up = accelerate (`W`)
- ⬇️ **Gesture Braking** — Left thumb up = brake (`S`)
- 🔄 **Real-Time Processing** — Smooth 30+ FPS performance with MediaPipe
- 🎨 **Visual Feedback** — Live overlay showing current action on screen
- 🎮 **Universal Compatibility** — Works with any game that uses `WASD` keys
- ♿ **Accessibility Friendly** — Great alternative for users with mobility challenges

---

## 📸 How It Works

| Gesture | Action | Key Pressed |
|---------|--------|-------------|
| Move wrists left | Turn Left | `A` |
| Move wrists right | Turn Right | `D` |
| Both hands centered | Keep Straight | `W` |
| One hand only | Reverse | `S` |
| Right thumb up | Accelerate | `W` |
| Left thumb up | Brake | `S` |

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Webcam

### Step 1: Clone the Repository
```bash
git clone https://github.com/Wiki313/Virtual_game_Steering.git
cd Virtual_game_Steering


