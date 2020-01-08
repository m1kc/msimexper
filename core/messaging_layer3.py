from .packet import MSIMRequest
from msim.models import User, Contact, PrivateChat, PrivateChatReference, PrivateChatMessage

import logging; log = logging.getLogger(__name__)
import secrets
import base64
import json

from django.db import transaction


SERVERNAME = 'localhost'


def register_all(h, s):
	h['CHATS-GET'] = handle_chats_get

	h['MESSAGE-SEND'] = handle_message_send
	s['MESSAGE-SEND'] = {
		'type': 'object',
		'properties': {
			'chat_id': { 'type': 'string' },
			'text': { 'type': 'string' },
			'cookie': { 'type': 'string' },
		},
		'required': ['chat_id', 'text', 'cookie'],
	}


def _last_message_id(chat_id):
	last_message_id = None
	last_message = PrivateChatMessage.objects.filter(chat_id=chat_id).order_by('-id')[:1]
	if len(last_message) > 0:
		last_message_id = last_message[0].pk
	return last_message_id


def handle_chats_get(p: MSIMRequest):
	assert p.user != None  # TODO: return proper code

	src = list(
		PrivateChatReference.objects
		.filter(user=p.user)
	)
	ret = []
	for ref in src:
		last_message_id = None
		last_message = PrivateChatMessage.objects.filter(chat=ref.chat).order_by('-id')[:1]
		if len(last_message) > 0:
			last_message_id = last_message[0].pk

		num_unread = 0
		if ref.last_read_msg_id != None:
			num_unread = PrivateChatMessage.objects.filter(chat=ref.chat).filter(pk__gt=ref.last_read_msg_id).count()

		ret.append({
			"id": ref.chat_mid,
			"unread_messages": num_unread,
			"last_message_id": last_message_id,
			"read_till_id": ref.last_read_msg_id,
		})
	return p.response(200, payload={
		'data': ret,
	})


def _get_or_create_chat(user, chat_mid):
	q = list(PrivateChatReference.objects.filter(user=user, chat_mid=chat_mid))
	if len(q) > 0:
		return q[0].chat

	# TODO: no checks at all, fix that!!
	chat = PrivateChat.objects.create(
		author_mid=f'{user.login}@{SERVERNAME}',
		recipient_mid=chat_mid,
	)

	PrivateChatReference.objects.create(
		user=user,
		chat_mid=chat_mid,
		chat=chat,
		last_read_msg_id=None,
	)
	PrivateChatReference.objects.create(
		user=User.objects.get(login=chat_mid.split('@')[0]),
		chat_mid=f'{user.login}@{SERVERNAME}',
		chat=chat,
		last_read_msg_id=None,
	)
	return chat


def handle_message_send(p: MSIMRequest):
	assert p.user != None  # TODO: return proper code

	chat_id = p.payload['chat_id']
	text = p.payload['text']
	cookie = p.payload['cookie']

	chat = _get_or_create_chat(p.user, chat_id)

	existing_msg = PrivateChatMessage.objects.filter(cookie=cookie)
	if len(existing_msg) > 0:
		return p.response(500)  # TODO: return proper code and message id

	msg = PrivateChatMessage.objects.create(
		chat=chat,
		prev_msg_id=_last_message_id(chat.pk),
		cookie=cookie,
		author_mid=f'{p.user.login}@{SERVERNAME}',
		text=text,
	)
	return p.response(200, {
		"cookie": cookie,
		"message_id": msg.pk,
		"time": msg.created,
	})
