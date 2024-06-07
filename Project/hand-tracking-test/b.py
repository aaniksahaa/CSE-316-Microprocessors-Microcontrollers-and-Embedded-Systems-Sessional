import numpy as np
import cv2

# Create a white image
width, height = 1600, 1200
white_image = np.full((height, width, 3), 255, dtype=np.uint8)

# Display the white image
cv2.imshow('White Image', white_image)
cv2.waitKey(0)

# Example of updating the image in a loop (replace this with your actual logic)
for _ in range(10000):  # Update the image 1000 times, you can adjust this
    # Get the coordinates where you want to turn pixels black (replace this with your actual logic)
    x = np.random.randint(0, width)
    y = np.random.randint(0, height)

    print(x,y)
    
    # Update the pixel to black
    #white_image[y, x] = [0, 0, 0]  # Assuming RGB image

    # Draw a black circle around the point (x, y)
    cv2.circle(white_image, (x, y), radius=2, color=(0, 0, 0), thickness=-1)  # Assuming RGB image, -1 for filled circle


    # Display the updated image
    cv2.imshow('White Image', white_image)
    
    # Check for user input to break the loop if needed
    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' to exit the loop
        break

cv2.destroyAllWindows()
