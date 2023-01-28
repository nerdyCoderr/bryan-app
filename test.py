import threading
import cv2
import queue


def image_generator(q):
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Run in a loop indefinitely
    while True:
        # Read an image from the camera
        ret, image = cap.read()

        # Put the image in the queue
        q.put(image)


# Create a queue
q = queue.Queue()

# Create a thread and start it
thread = threading.Thread(target=image_generator, args=(q,))
thread.start()

# Wait for keyboard input in the main thread
while True:
    user_input = input("Enter something: ")

    # If the user presses 's', get the image from the queue
    if user_input == 's':
        # Get the image from the queue, or None if the queue is empty
        image = q.get_nowait()

        # Display the image using cv2
        cv2.imshow("Image", image)
        cv2.waitKey(0)
    else:
        print("You entered:", user_input)
