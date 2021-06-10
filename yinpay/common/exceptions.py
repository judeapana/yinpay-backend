

class FlashError(Exception):
    def __init__(self, message, **kwargs):
        self.messages = message
        self.kwargs = kwargs
        super().__init__(message)
