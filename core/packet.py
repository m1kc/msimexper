class MSIMPacket:
	layer: int = None  # Protocol layer specified by packet originator
	ptype: str = None  # Packet type
	payload: dict = None  # Packet body (if any)
	sessid: str = None  # Session ID (if any)
	code: int = None  # Response code (for server responses)

	user: object = None  # User instance (if sessid was specified and it's valid)

	# @classmethod
	# def ingress(cls, layer, ptype, payload=None, sessid=None):
	# 	return cls()

	# TODO: split constructors for ingress/egress
	def __init__(self, layer=None, ptype=None, payload=None, code=None, sessid=None):
		assert layer != None
		assert code != None

		self.layer = layer
		self.ptype = ptype
		self.payload = payload
		self.code = code
		self.sessid = sessid

	def __str__(self):
		return str(self.__dict__)

	def response(self, code, ptype=None, payload=None):
		return MSIMPacket(
			layer=self.layer,  # TODO: maybe we don't need this in server responses
			ptype=ptype,
			payload=payload,
			code=code,
			sessid=self.sessid,  # TODO: maybe we don't need this in server responses
		)
