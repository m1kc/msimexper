class MSIMPacket:
	# TODO: split constructors for ingress/egress
	# TODO: validate
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
