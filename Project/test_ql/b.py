import cv2

def draw_circle_at_center(frame):
    height, width, _ = frame.shape

    # Calculate the center coordinates
    center_coordinates = (width // 2, height // 2)

    # Radius of the circle
    radius = 50

    # Color of the circle in BGR format (green in this case)
    color = (0, 255, 0)

    # Thickness of the circle outline
    thickness = 2

    # Draw the circle on the frame
    cv2.circle(frame, center_coordinates, radius, color, thickness)

    return frame

# Set the desired display dimensions
display_width = 1400
display_height = 1000

# Open a video capture object (0 for default camera, or specify the video file path)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame is successfully captured
    if not ret:
        print("Failed to capture frame")
        break

    # Resize the frame to the desired display dimensions
    frame = cv2.resize(frame, (display_width, display_height))

    # Draw a circle at the center
    frame_with_circle = draw_circle_at_center(frame)

    # Display the resulting frame
    cv2.imshow('Video with Circle', frame_with_circle)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
