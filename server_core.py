from msim.models import Session, User

import logging; log = logging.getLogger(__name__)
import json
import secrets

from django.db import transaction
import tornado.ioloop
import tornado.web
# from tornado.httputil import HTTPServerRequest


class MSIMPacket:
	# TODO: split constructors for ingress/egress
	# TODO: validate
	# TODO: response()
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


def _parse_packet(layer: int, ptype: str, payload: dict):
	# TODO: validate payload against JSON schema
	ret = MSIMPacket(
		layer=layer,
		code=0,
		ptype=ptype,
		sessid=None,  # TODO
		payload=payload,
	)
	log.warning(ret)
	return ret


def parse_packet_from_tornado(layer: int, ptype: str, rh: tornado.web.RequestHandler):
	payload = None
	if len(rh.request.body) > 0:
		payload = json.loads(rh.request.body)
	return _parse_packet(layer, ptype, payload)


def handle_packet(p: MSIMPacket):
	# TODO: define some way to return HTTP code
	if p.ptype == 'HELLO':
		return p.response(200, payload={
			'highest-supported-layer': 1,
			'servername': 'dev.test',  # TODO
			'federated': False,
			'supported-auth-methods': ['AUTH-PLAIN'],
			'supported-register-methods': ['REGISTER-PLAIN', 'REGISTER-INSTRUCTIONS'],
		})
	elif p.ptype == 'AUTH-PLAIN':
		try:
			user = User.objects.get(login=p.payload['login'], password_plaintext=p.payload['password'])  # TODO: base64
			# TODO: make sure sessid doesn't exist
			sessid = secrets.token_hex(32)
			Session.objects.create(user=user, extid=sessid)
			return p.response(200, payload={
				'sessid': sessid,
			})
		except Exception:
			return p.response(403)
	elif p.ptype == 'REGISTER-PLAIN':
		with transaction.atomic():
			if User.objects.filter(login=p.payload['login']).exists():
				return p.response(403)
			user = User.objects.create(login=p.payload['login'], password_plaintext=p.payload['password'])  # TODO: base64
			return p.response(200)
	elif p.ptype == 'REGISTER-INSTRUCTIONS':
		return p.response(200, payload={
			'text': 'Подайте заявление в бумажном виде',
			'url': 'https://example.com/register',
		})
	else:
		raise ValueError(f'Unknown packet type: {p.ptype}')
