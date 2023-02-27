import cv2
import time
from emailing import send_email

video = cv2.VideoCapture(0)
# this gives the webcam time to warm up
time.sleep(1)

first_frame = None
status_list = []

# the while loop lets the webcam run infinitely until stopped. the frame variable in video read
# allows us to look at individual webcam frames (image captures) think frames per second.
while True:
    status = 0
    check, frame = video.read()
    # With this I convert all the frames to grayscale, as BGR is more complex data and this allows us
    # to have less to process when detecting changes to the static variable image
    # The gaussian blur is applied to make the image simpler for analysis. 21 denotes the level of blur
    # . 0 the standard deviation
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    # this essentially begins the video after a change has been detected in the first_frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # this below code essentially checks if a pixel has a value color value above 65,
    # and then its reassigned the value 255
    # dil frame then dilutes the frame removing more noise
    thresh_frame = cv2.threshold(delta_frame, 65, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # this finds all the white contours and calculates their area
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # this makes it so any white displayed less than 5000 pixels is ignored as a false positive
    # the bounding rect draws a rectangle around the contours of the area of a true positive detected obj
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        detected = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if detected.any():
            status = 1

    # by doing status list[-2:], we are only looking at the last two items in the status array
    # after which, we limit the amount of emails sent by only sending an email
    # if the 1 (motion detected) changes to 0 (object left camera), counting as motion and submitting one email only
    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email()
    print(status_list)

    # waitKey asks the program to display an image until a certain key is pressed
    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)

    # This closes the program by determining which key stops it (q)
    if key == ord("q"):
        break

video.release()