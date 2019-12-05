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

	h['CONTACTS-ADD'] = handle_contacts_add
	s['CONTACTS-ADD'] = {
		'type': 'object',
		'properties': {
			'id': { 'type': 'string' },
			'name': { 'type': 'string' },
			'group': { 'type': 'array' },
		},
		'required': ['id', 'name', 'group'],
	}

	h['CONTACTS-CHANGE'] = handle_contacts_change
	s['CONTACTS-CHANGE'] = {
		'type': 'object',
		'properties': {
			'id': { 'type': 'string' },
			'name': { 'type': 'string' },
			'group': { 'type': 'array' },
		},
		'required': ['id', 'name', 'group'],
	}

	h['CONTACTS-DELETE'] = handle_contacts_delete
	s['CONTACTS-DELETE'] = {
		'type': 'object',
		'properties': {
			'id': { 'type': 'string' },
		},
		'required': ['id'],
	}


def handle_contacts_get(p: MSIMRequest):
	assert p.user != None  # TODO: return proper code

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


def handle_contacts_add(p: MSIMRequest):
	assert p.user != None  # TODO: return proper code

	cid = p.payload['id']
	name = p.payload['name']
	group = p.payload['group']

	handle, servername = cid.split("@")

	# TODO: make sure servername is this same server
	# TODO: make sure username actually exists

	if Contact.objects.filter(user=p.user, handle=handle, servername=servername).exists():
		return p.response(409)

	Contact.objects.create(
		user=p.user,
		handle=handle,
		servername=servername,
		caption=name,
		group_path_json=json.dumps(group, ensure_ascii=False)
	)
	return p.response(200)


def handle_contacts_change(p: MSIMRequest):
	assert p.user != None  # TODO: return proper code

	cid = p.payload['id']
	name = p.payload['name']
	group = p.payload['group']

	handle, servername = cid.split("@")

	c = Contact.objects.get(user=p.user, handle=handle, servername=servername)
	c.caption = name
	c.group_path_json = json.dumps(group, ensure_ascii=False)
	c.save()
	return p.response(200)


def handle_contacts_delete(p: MSIMRequest):
	assert p.user != None  # TODO: return proper code

	cid = p.payload['id']

	handle, servername = cid.split("@")

	c = Contact.objects.get(user=p.user, handle=handle, servername=servername)
	c.delete()
	return p.response(200)
