from .constants import HTTPStatusCode

class Response:
    def __init__(self):
        self._msg     = str()
        self._data    = dict()
        self._success = bool(False)
        self._status_code = HTTPStatusCode.PROCESSING

    @property
    def msg(self):
        return self._msg
    
    @msg.setter
    def msg(self, value):
        self._msg = value

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value

    @property
    def status_code(self):
        return self._status_code
    
    @status_code.setter
    def status_code(self, value):
        self._status_code = value
    
    # DEPRECATED #
    def set_success(self):
        self._success = True

    def set_failure(self):
        self._success = False

    def set_msg(self, msg):
        self._msg = msg

    def set_data(self, data):
        self._data = data
    # DEPRECATED #

    def serialize(self):
        return {
            'msg'    : self._msg,
            'data'   : self._data,
            'success': self._success,
            'status_code': self._status_code.value
        }
    
    def respond(self):
        return self.serialize()
    
class Success(Response):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._success = True
    
class Failure(Response):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._success = False