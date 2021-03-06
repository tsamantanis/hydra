"""Dependency and package import."""
import os
import smtplib


def sendMail(subject, message, receiver):
    """Connect to mail server and send message."""
    username = os.getenv("MAIL_USERNAME")
    password = os.getenv("MAIL_PASSWORD")

    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)

        # Start tls for security

        s.starttls()

        s.login(username, password)
    except Exception as e:
        print("FAILED TO LOGIN, PLEASE CHECK CREDENTIALS.")

    """Send email in the format

    {subject}
    Hi {receiver},
    {message}
    """
    message = f"""
    Subject: {subject}

    {message}
    """

    is_fail = False

    s.sendmail(
        username,
        receiver,
        message,
    )
    s.quit()

    return is_fail


# Testing mail send:

if __name__ == "__main__":
    send_mail("Test", "Testing mail send", "unhumanartist@gmail.com")
