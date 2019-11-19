from .packet import MSIMPacket
from msim.models import Session, User

import logging; log = logging.getLogger(__name__)
import secrets
import base64

from django.db import transaction


SERVERNAME = 'localhost'


def register_all(h, s):
	h['HELLO'] = handle_hello

	h['AUTH-PLAIN'] = handle_auth_plain
	s['AUTH-PLAIN'] = {
		'type': 'object',
		'properties': {
			'login': { 'type': 'string' },
			'password': { 'type': 'string' },
		},
		'required': ['login', 'password'],
	}

	h['REGISTER-PLAIN'] = handle_register_plain
	s['REGISTER-PLAIN'] = {
		'type': 'object',
		'properties': {
			'login': { 'type': 'string' },
			'password': { 'type': 'string' },
		},
		'required': ['login', 'password'],
	}

	h['REGISTER-INSTRUCTIONS'] = handle_register_instructions


def handle_hello(p: MSIMPacket):
	return p.response(200, payload={
		'highest-supported-layer': 1,
		'servername': SERVERNAME,
		'federated': False,
		'supported-auth-methods': ['AUTH-PLAIN'],
		'supported-register-methods': ['REGISTER-PLAIN', 'REGISTER-INSTRUCTIONS'],
	})


def handle_auth_plain(p: MSIMPacket):
	try:
		user = User.objects.get(
			login=p.payload['login'],
			password_plaintext=base64.b64decode(p.payload['password']).decode('utf-8'),
		)
		# TODO: make sure sessid doesn't exist
		sessid = secrets.token_hex(32)
		Session.objects.create(user=user, extid=sessid)
		return p.response(200, payload={
			'sessid': sessid,
		})
	except Exception:
		return p.response(403)


def handle_register_plain(p: MSIMPacket):
	with transaction.atomic():
		if User.objects.filter(login=p.payload['login']).exists():
			return p.response(403)
		User.objects.create(
			login=p.payload['login'],
			password_plaintext=base64.b64decode(p.payload['password']).decode('utf-8'),
		)
		return p.response(200)


def handle_register_instructions(p: MSIMPacket):
	return p.response(200, payload={
		'text': 'Подайте заявление в бумажном виде',
		'url': 'https://example.com/register',
	})
