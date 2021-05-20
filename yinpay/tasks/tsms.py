from yinpay.common.sms import SMS
from yinpay.ext import rq


@rq.job(description='Send SMS')
def send_sms(sms_type: str, message: str, destination: list, sender='YINPAY'):
    sms = SMS(sms_type, message, sender, destination)
    return sms.send()
