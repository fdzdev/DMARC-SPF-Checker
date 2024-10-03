import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_spoofed_email():
    try:
        # Email details
        spoofed_sender_email = "nasa@mastercard.us"  # Spoofed sender
        recipient_email = "facu.tha@gmail.com"  # Recipient email
        auth_email = "personas@fedeyclau.info"  # Email used for authentication
        smtp_server = "c1310741.ferozo.com"
        port = 465
        password = "40@P@CR8yG"  # Password for personas@fedeyclau.info

        # Email message content
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

        # Create MIME message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = spoofed_sender_email  # Spoofed sender address
        message["To"] = recipient_email

        # Create plain-text and HTML versions of the message
        text_part = MIMEText(
            "Hello, this is a test email with a spoofed sender address.", "plain"
        )
        html_part = MIMEText(html_message, "html")

        # Attach both parts to the message
        message.attach(text_part)
        message.attach(html_part)

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Send email
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(
                auth_email, password
            )  # Authenticate using personas@fedeyclau.info
            server.sendmail(spoofed_sender_email, recipient_email, message.as_string())

        print("Spoofed email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")


# Call the function to send the spoofed email
send_spoofed_email()
