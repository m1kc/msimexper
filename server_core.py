from msim.models import Session, User

import logging; log = logging.getLogger(__name__)
import json
import secrets

import tornado.ioloop
import tornado.web
# from tornado.httputil import HTTPServerRequest


class MSIMPacket:
	def __init__(self, layer=None, ptype=None, payload=None, code=None, sessid=None):
		assert layer != None
		assert code != None

		self.layer = layer
		self.ptype = ptype
		self.payload = payload
		self.code = code
		self.sessid = sessid


def _parse_packet(ptype: str, payload: dict):
	# TODO: validate payload against JSON schema
	ret = MSIMPacket(
		layer=1,  # TODO
		code=0,
		ptype=ptype,
		sessid=None, # TODO
		payload=payload,
	)
	log.warning(ret)
	return ret


def parse_packet_from_tornado(ptype: str, rh: tornado.web.RequestHandler):
	payload = None
	if len(rh.request.body) > 0:
		payload = json.loads(rh.request.body)
	return _parse_packet(ptype, payload)


def handle_packet(p: MSIMPacket):
	# TODO: define some way to return HTTP code
	if p.ptype == 'HELLO':
		return MSIMPacket(
			layer=p.layer,
			code=200,
			payload={
				'highest-supported-layer': 1,
				'servername': 'dev.test',  # TODO
				'federated': False,
				'supported-auth-methods': ['AUTH-PLAIN'],
				'supported-register-methods': ['REGISTER-PLAIN', 'REGISTER-INSTRUCTIONS'],
			},
			sessid=p.sessid,
		)
	elif p.ptype == 'AUTH-PLAIN':
		try:
			user = User.objects.get(login=p.payload['login'], password_plaintext=p.payload['password'])  # TODO: base64
			# TODO: make sure sessid doesn't exist
			sessid = secrets.token_hex(32)
			Session.objects.create(user=user, extid=sessid)
			return MSIMPacket(
				layer=p.layer,
				code=200,
				payload={
					'sessid': sessid,
				},
				sessid=p.sessid,
			)
		except Exception:
			return MSIMPacket(
				layer=p.layer,
				code=403,
				sessid=p.sessid,
			)
	elif p.ptype == 'REGISTER-PLAIN':
		try:
			assert len(User.objects.filter(login=p.payload['login'])) == 0
			user = User.objects.create(login=p.payload['login'], password_plaintext=p.payload['password'])  # TODO: base64
			return MSIMPacket(
				layer=p.layer,
				code=200,
				sessid=p.sessid,
			)
		except Exception:
			return MSIMPacket(
				layer=p.layer,
				code=403,
				sessid=p.sessid,
			)
	elif p.ptype == 'REGISTER-INSTRUCTIONS':
		return MSIMPacket(
			layer=p.layer,
			code=200,
			payload={
				'text': 'Подайте заявление в бумажном виде',
				'url': 'https://example.com/register',
			},
			sessid=p.sessid,
		)
	else:
		raise ValueError(f'Unknown packet type: {p.ptype}')
