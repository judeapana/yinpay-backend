from yinpay.ext import rq


@rq.job(description='Send SMS')
def send_sms():
    return
