from .packet import MSIMPacket
from core import auth_layer1

import logging; log = logging.getLogger(__name__)
import json

import tornado.ioloop
import tornado.web
# from tornado.httputil import HTTPServerRequest
from jsonschema import validate
from jsonschema.exceptions import ValidationError


HANDLERS = {}
SCHEMAS = {}
auth_layer1.register_all(HANDLERS, SCHEMAS)


def _parse_packet(layer: int, ptype: str, payload: dict):
	ret = MSIMPacket(
		layer=layer,
		code=0,
		ptype=ptype,
		sessid=None,  # TODO
		payload=payload,
	)
	log.warning(ret)
	return ret


def parse_packet_from_tornado(layer: int, ptype: str, rh: tornado.web.RequestHandler):
	payload = None
	if len(rh.request.body) > 0:
		payload = json.loads(rh.request.body)
	return _parse_packet(layer, ptype, payload)


def handle_packet(p: MSIMPacket):
	# Validate payload, if any
	if p.payload != None:
		if p.ptype in SCHEMAS:
			try:
				validate(instance=p.payload, schema=SCHEMAS[p.ptype])
				log.warning('Validation ok')
			except ValidationError as ex:
				return p.response(400, payload={
					'_msimexper_error': str(ex),
				})
		else:
			log.warning(f"Can't validate packet: no schema for {p.ptype}")
	# Produce response
	if p.ptype in HANDLERS:
		return HANDLERS[p.ptype](p)
	else:
		return p.response(400)
