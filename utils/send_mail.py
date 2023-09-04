from flask_mail import Mail, Message

mail = Mail()


def send_mail(subject, recipients, body):
    msg = Message(subject, sender='congthanhtr1510@gmail.com', recipients=recipients)
    msg.body = body
    mail.send(msg)
    return 'Mail sent successfully'
