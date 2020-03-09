from .packet import MSIMRequest
from core import auth_layer1, contact_layer2, messaging_layer3
from msim.models import Session, User

import logging; log = logging.getLogger(__name__)
import json

#import tornado.ioloop
#import tornado.web
## from tornado.httputil import HTTPServerRequest
from jsonschema import validate
from jsonschema.exceptions import ValidationError


HANDLERS = {}
SCHEMAS = {}
auth_layer1.register_all(HANDLERS, SCHEMAS)
contact_layer2.register_all(HANDLERS, SCHEMAS)
messaging_layer3.register_all(HANDLERS, SCHEMAS)

LOG_ALL = True


def auth(sessid: str) -> User:
	user = None
	if sessid != None:
		session = Session.objects.get(extid=sessid)
		user = session.user
	return user


def make_request(layer, ptype, payload, sessid):
	user = auth(sessid)

	# TODO: validate here instead of handle_ ?

	return MSIMRequest(layer, ptype, payload, sessid, user)


#def parse_request_from_tornado(layer: int, ptype: str, rh: tornado.web.RequestHandler):
#	payload = None
#	if len(rh.request.body) > 0:
#		payload = json.loads(rh.request.body)
#
#	sessid = None
#	if 'X-Session' in rh.request.headers:
#		sessid = rh.request.headers['X-Session']
#
#	return make_request(layer, ptype, payload, sessid)


def parse_request_django(layer: int, ptype: str, request):
	payload = None
	if len(request.body) > 0:
		payload = json.loads(request.body)

	sessid = None
	if 'X-Session' in request.headers:
		sessid = request.headers['X-Session']

	return make_request(layer, ptype, payload, sessid)


def handle_request(p: MSIMRequest):
	# Validate payload, if any
	# TODO: handle case if no payload but it's required
	if p.payload != None:
		if p.ptype in SCHEMAS:
			try:
				validate(instance=p.payload, schema=SCHEMAS[p.ptype])
				log.warning('Payload validation ok')
			except ValidationError as ex:
				return p.response(400, payload={
					'_msimexper_error': str(ex),
				})
		else:
			log.warning(f"Can't validate packet: no schema for {p.ptype}")
	else:
		log.warning('No payload, skipping validation step')
	# Produce response
	if p.ptype in HANDLERS:
		return HANDLERS[p.ptype](p)
	else:
		return p.response(400)
