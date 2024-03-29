from flask_mail import Message

from yinpay.ext import rq, mail


@rq.job(description='Send E-mail', func_or_queue='yin_pay_default')
def send_mail(subject: str, message: str, recipients: list):
    try:
        msg = Message(subject, recipients)
        msg.html = message
        mail.send(msg)
    except Exception as e:
        print(e)
        return e
