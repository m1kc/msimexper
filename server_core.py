from msim.models import Session, User

import logging; log = logging.getLogger(__name__)
from collections import namedtuple
import json
import secrets

import tornado.ioloop
import tornado.web
# from tornado.httputil import HTTPServerRequest


class MSIMPacket(namedtuple('MSIMPacket', ['sessid', 'ptype', 'payload', 'code'])):
	pass


def _parse_packet(ptype: str, payload: dict):
	# TODO: validate payload against JSON schema
	ret = MSIMPacket(
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
		return {
			'highest-supported-layer': 1,
			'servername': 'dev.test',  # TODO
			'federated': False,
			'supported-auth-methods': ['AUTH-PLAIN'],
			'supported-register-methods': ['REGISTER-PLAIN', 'REGISTER-INSTRUCTIONS'],
		}
	elif p.ptype == 'AUTH-PLAIN':
		try:
			user = User.objects.get(login=p.payload['login'], password_plaintext=p.payload['password'])  # TODO: base64
			# TODO: make sure sessid doesn't exist
			sessid = secrets.token_hex(32)
			Session.objects.create(user=user, extid=sessid)
			return {
				'sessid': sessid,
			}
		except Exception:
			return None
	elif p.ptype == 'REGISTER-PLAIN':
		try:
			assert len(User.objects.filter(login=p.payload['login'])) == 0
			user = User.objects.create(login=p.payload['login'], password_plaintext=p.payload['password'])  # TODO: base64
			return None
		except Exception:
			return None
	elif p.ptype == 'REGISTER-INSTRUCTIONS':
		return {
			'text': 'Подайте заявление в бумажном виде',
			'url': 'https://example.com/register',
		}
	else:
		raise ValueError(f'Unknown packet type: {p.ptype}')
