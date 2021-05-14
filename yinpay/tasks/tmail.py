from flask import current_app

from yinpay.ext import rq

queue = current_app.config['RQ_QUEUES'][0]


@rq.job(description='Send mail', func_or_queue=queue)
def send_mail():
    return
