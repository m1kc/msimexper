import logging; log = logging.getLogger(__name__)


class MSIMRequest:
	layer: int = None  # Protocol layer as specified by packet originator
	ptype: str = None  # Packet type
	payload: dict = None  # Packet body (if any)
	sessid: str = None  # Session ID (if any)

	user: object = None  # User instance associated with this request (if any)

	def __init__(self, layer, ptype, payload=None, sessid=None, user=None):
		self.layer = layer
		self.ptype = ptype
		self.payload = payload
		self.sessid = sessid
		self.user = user
		log.warning(f'MSIM request: {self.__dict__}')

	def response(self, code, ptype=None, payload=None):
		return MSIMResponse(
			code=code,
			ptype=ptype,
			payload=payload,

			_layer=self.layer,
			_sessid=self.sessid,
			_user=self.user,
		)


class MSIMResponse:
	code: int = None  # Response code
	ptype: str = None  # Packet type (if any)
	payload: dict = None  # Packet body (if any)

	_layer: int = None
	_sessid: str = None
	_user: object = None

	def __init__(self, code, *, ptype=None, payload=None, _layer=None, _sessid=None, _user=None):
		self.code = code
		self.ptype = ptype
		self.payload = payload
		self._layer = _layer
		self._sessid = _sessid
		self._user = _user
