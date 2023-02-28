import os
import smtplib
import imghdr
from email.message import EmailMessage

key = 'PASSWORD_EMAILBOT'
PASSWORD = os.getenv(key)
SENDER = "automata.python@gmail.com"
RECEIVER = "automata.python@gmail.com"


def send_email(object_image):
    email_message = EmailMessage()
    email_message["Subject"] = "Motion detected on webcam"
    # noinspection PyTypeChecker
    email_message.set_content("Motion has been detected on webcam. Please see attached image.")

    with open(object_image, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email(object_image="images/13.png")