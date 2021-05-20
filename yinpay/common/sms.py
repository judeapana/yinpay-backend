from requests import post

from yinpay.common.exceptions import FlashError


class SMS:
    BaseUrl = 'https://sms.textcus.com/api'
    PLAIN_TEXT = '0'
    FLASH = '1'

    def __init__(self, sms_type, message: str, sender: str, destination: list):
        self.destination = ','.join(destination)
        self.source = sender
        self.dlr = "1"
        self.type = '1' if sms_type == 'Flash Text' else '0'
        self.message = message
        self.apikey = 'Gdgns33D5JRaaBsYDm5W7NG31EDZoCP5'

    def __dict__(self):
        return {
            'apikey': self.apikey,
            'destination': self.destination,
            'source': self.source,
            'dlr': self.dlr,
            'type': self.type,
            'message': self.message
        }

    def send(self):
        try:
            req = post(f'{self.BaseUrl}/send', params=self.__dict__())
            return req.json()
        except Exception:
            raise FlashError('Sorry we could\'nt send your message at this moment')
