#!/usr/bin/env python3
import logging; log = logging.getLogger(__name__)
import json
import os

import tornado.ioloop
import tornado.web
# from tornado.httputil import HTTPServerRequest
import arrow
import django
import django.conf

PORT = 3218
DEBUG = True


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("msimexper server, version 0.1.0\n\nSee API docs for available methods.")


class EverythingHandler(tornado.web.RequestHandler):
	def post(self, layer, ptype):
		from core.server_core import parse_packet_from_tornado, handle_packet
		req = parse_packet_from_tornado(int(layer), ptype, self)
		res = handle_packet(req)
		self.set_status(res.code)
		if res.payload != None:
			self.write(json.dumps(res.payload, ensure_ascii=False))


def make_app():
	return tornado.web.Application([
		(r"/", IndexHandler),
		(r"/v(\d+)/(\S+)", EverythingHandler),
	], debug=DEBUG)


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
