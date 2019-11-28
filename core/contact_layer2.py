from .packet import MSIMRequest
from msim.models import Contact

import logging; log = logging.getLogger(__name__)
import secrets
import base64
import json

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


def handle_contacts_get(p: MSIMRequest):
	src = list(Contact.objects.filter(user=p.user))

	ret = []
	for contact in src:
		ret.append({
			'contact': {
				'id': f'{contact.handle}@{contact.servername}',
				'name': contact.caption,
				'group': json.loads(contact.group_path_json),
			},
			'last-seen': '2000-09-09T14:22:31+0300',  # TODO
		})

	return p.response(200, payload={
		'data': ret,
	})
