import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_spoofed_email():
    try:
        spoofed_sender_email = "nasa@mastercard.us"
        recipient_email = ""
        smtp_server = ""
        port = 465
        password = ""

        subject = "Testing spoofed email"
        html_message = """\
        <html>
        <body>
            <p>Hello,<br>
               This is a test email to check how spoofed sender addresses are handled.<br>
               Please review the headers to verify the sender.
            </p>
        </body>
        </html>
        """

        # MIME
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = spoofed_sender_email  # This is the spoofed address
        message["To"] = recipient_email

        # HTML
        text_part = MIMEText(
            "Hello, this is a test email with a spoofed sender address.", "plain"
        )
        html_part = MIMEText(html_message, "html")

        # Attach both parts to the message
        message.attach(text_part)
        message.attach(html_part)

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(actual_sender_email, password)
            server.sendmail(actual_sender_email, recipient_email, message.as_string())

        print("Spoofed email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")


send_spoofed_email()
