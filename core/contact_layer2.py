from .packet import MSIMPacket
from msim.models import Session, User

import logging; log = logging.getLogger(__name__)
import secrets
import base64

from django.db import transaction


SERVERNAME = 'localhost'


def register_all(h, s):
	h['CONTACTS-GET'] = handle_contacts_get

	# h['AUTH-PLAIN'] = handle_auth_plain
	# s['AUTH-PLAIN'] = {
	# 	'type': 'object',
	# 	'properties': {
	# 		'login': { 'type': 'string' },
	# 		'password': { 'type': 'string' },
	# 	},
	# 	'required': ['login', 'password'],
	# }


def handle_contacts_get(p: MSIMPacket):
	return p.response(200, payload={
		'data': [{
			'contact': {
				'id': 'm1kc@localhost',
				'name': 'm1kc',
				'group': ['Everybody'],
			},
			'last-seen': '2018-09-09T14:22:31+0300'
		}]
	})
