import math
import keyinput
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
font = cv2.FONT_HERSHEY_SIMPLEX

# For webcam input:
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # To improve performance, optionally mark the image as not writeable to
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        imageHeight, imageWidth, _ = image.shape

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        co = []
        thumbs_up_right = False
        thumbs_up_left = False

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = handedness.classification[0].label
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                )
                for point in mp_hands.HandLandmark:
                    if str(point) == "HandLandmark.WRIST":
                        normalizedLandmark = hand_landmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(
                            normalizedLandmark.x,
                            normalizedLandmark.y,
                            imageWidth, imageHeight
                        )
                        if pixelCoordinatesLandmark is not None:
                            co.append(list(pixelCoordinatesLandmark))

                # Thumb tip and IP coordinates
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

                # Calculate the distance between thumb tip and thumb IP
                thumb_distance = math.sqrt((thumb_tip.x - thumb_ip.x) ** 2 + (thumb_tip.y - thumb_ip.y) ** 2)

                if thumb_distance < 0.04:  # Adjust this threshold based on testing
                    if hand_label == 'Right':
                        thumbs_up_right = True
                    elif hand_label == 'Left':
                        thumbs_up_left = True

        if len(co) == 2:
            xm, ym = (co[0][0] + co[1][0]) / 2, (co[0][1] + co[1][1]) / 2
            radius = 150
            try:
                m = (co[1][1] - co[0][1]) / (co[1][0] - co[0][0])
            except ZeroDivisionError:
                continue
            a = 1 + m ** 2
            b = -2 * xm - 2 * co[0][0] * (m ** 2) + 2 * m * co[0][1] - 2 * m * ym
            c = xm ** 2 + (m ** 2) * (co[0][0] ** 2) + co[0][1] ** 2 + ym ** 2 - 2 * co[0][1] * ym - 2 * co[0][1] * co[0][0] * m + 2 * m * ym * co[0][0] - 22500
            try:
                xa = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
                xb = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
                ya = m * (xa - co[0][0]) + co[0][1]
                yb = m * (xb - co[0][0]) + co[0][1]
            except ValueError:
                continue

            if m != 0:
                ap = 1 + ((-1 / m) ** 2)
                bp = -2 * xm - 2 * xm * ((-1 / m) ** 2) + 2 * (-1 / m) * ym - 2 * (-1 / m) * ym
                cp = xm ** 2 + ((-1 / m) ** 2) * (xm ** 2) + ym ** 2 + ym ** 2 - 2 * ym * ym - 2 * ym * xm * (-1 / m) + 2 * (-1 / m) * ym * xm - 22500
                try:
                    xap = (-bp + (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
                    xbp = (-bp - (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
                    yap = (-1 / m) * (xap - xm) + ym
                    ybp = (-1 / m) * (xbp - xm) + ym
                except ValueError:
                    continue

            cv2.circle(img=image, center=(int(xm), int(ym)), radius=radius, color=(195, 255, 62), thickness=15)

            l = (int(math.sqrt((co[0][0] - co[1][0]) ** 2 * (co[0][1] - co[1][1]) ** 2)) - 150) // 2
            cv2.line(image, (int(xa), int(ya)), (int(xb), int(yb)), (195, 255, 62), 20)
            if co[0][0] > co[1][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65:
                print("Turn left.")
                keyinput.release_key('s')
                keyinput.release_key('d')
                keyinput.press_key('a')
                cv2.putText(image, "Turn left", (33, 33), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)

            elif co[1][0] > co[0][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65:
                print("Turn left.")
                keyinput.release_key('s')
                keyinput.release_key('d')
                keyinput.press_key('a')
                cv2.putText(image, "Turn left", (33, 33), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)

            elif co[0][0] > co[1][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65:
                print("Turn right.")
                keyinput.release_key('s')
                keyinput.release_key('a')
                keyinput.press_key('d')
                cv2.putText(image, "Turn right", (33, 33), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)

            elif co[1][0] > co[0][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65:
                print("Turn right.")
                keyinput.release_key('s')
                keyinput.release_key('a')
                keyinput.press_key('d')
                cv2.putText(image, "Turn right", (33, 33), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)

            else:
                print("keeping straight")
                keyinput.release_key('s')
                keyinput.release_key('a')
                keyinput.release_key('d')
                keyinput.press_key('w')
                cv2.putText(image, "keep straight", (33, 33), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                if ybp > yap:
                    cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)
                else:
                    cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)

        if len(co) == 1:
            print("keeping back")
            keyinput.release_key('a')
            keyinput.release_key('d')
            keyinput.release_key('w')
            keyinput.press_key('s')
            cv2.putText(image, "keeping back", (33, 33), font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        # Accelerate if right thumb is pressed
        if thumbs_up_right and not thumbs_up_left:
            print("Accelerate")
            keyinput.press_key('w')
            keyinput.release_key('s')
            cv2.putText(image, "Accelerate", (25, 25), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        # Brake if left thumb is pressed
        if thumbs_up_left and not thumbs_up_right:
            print("Brake")
            keyinput.press_key('s')
            keyinput.release_key('w')
            cv2.putText(image, "Brake", (50, 150), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

        # Flip the image horizontally for a selfie-view display.
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

