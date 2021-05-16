from yinpay.ext import rq


@rq.job(description='Send mail')
def send_mail():
    return
