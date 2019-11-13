#!/usr/bin/env python3
import logging; log = logging.getLogger(__name__)
from collections import namedtuple
import json
import os

import tornado.ioloop
import tornado.web
# from tornado.httputil import HTTPServerRequest
import arrow
import django
import django.conf

PORT = 3218


class MSIMPacket(namedtuple('MSIMPacket', ['sessid', 'ptype', 'payload'])):
	pass

def parse_packet(ptype: str, rh: tornado.web.RequestHandler):
	payload = None
	if len(rh.request.body) > 0:
		payload = json.loads(rh.request.body)
	# TODO: validate against JSON schema
	ret = MSIMPacket(
		ptype=ptype,
		sessid=None, # TODO
		payload=payload,
	)
	log.warning(ret)
	return ret

def handle_packet(p: MSIMPacket):
	if p.ptype == 'HELLO':
		return {
			'highest-supported-layer': 1,
			# 'servername': 'test.test',  # TODO
			'federated': False,
			'supported-auth-methods': ['AUTH-PLAIN'],
			'supported-register-methods': ['REGISTER-PLAIN', 'REGISTER-INSTRUCTIONS'],
		}
	elif p.ptype == 'AUTH-PLAIN':
		return {
			'sessid': 'a0ac9ceec30b0bd05a498f927e96fa8e',
		}
	elif p.ptype == 'REGISTER-PLAIN':
		return None
	elif p.ptype == 'REGISTER-INSTRUCTIONS':
		return {
			'text': 'Подайте заявление в бумажном виде',
			'url': 'https://example.com/register',
		}
	else:
		raise ValueError(f'Unknown packet type: {p.ptype}')


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("msimexper server, version 0.1.0\n\nSee API docs for available methods.")

class EverythingHandler(tornado.web.RequestHandler):
	def post(self, ptype):
		p = parse_packet(ptype, self)
		ret = handle_packet(p)
		if ret != None:
			self.write(json.dumps(ret, ensure_ascii=False))


def make_app():
	return tornado.web.Application([
		(r"/", IndexHandler),
		(r"/(\S+)", EverythingHandler),
	], debug=True)

if __name__ == "__main__":
	## Initialize Django
	os.environ["DJANGO_SETTINGS_MODULE"] = "msimexper.settings"
	django.setup()
	## Make sure Django actually works
	from django.contrib.auth import get_user_model
	assert get_user_model().objects.all() != None
	## Start up
	app = make_app()
	log.warning(f'[{arrow.now()}] Starting server at port {PORT}')  # TODO: colorful logging
	# TODO: header "Server: msimexper 0.1.0"
	app.listen(PORT)
	try:
		tornado.ioloop.IOLoop.current().start()
	except KeyboardInterrupt:
		pass
