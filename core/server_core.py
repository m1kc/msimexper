from .packet import MSIMPacket
from core import auth_layer1

import logging; log = logging.getLogger(__name__)
import json

import tornado.ioloop
import tornado.web
# from tornado.httputil import HTTPServerRequest


HANDLERS = {}
auth_layer1.register_all(HANDLERS)


def _parse_packet(layer: int, ptype: str, payload: dict):
	# TODO: validate payload against JSON schema
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
	if p.ptype in HANDLERS:
		return HANDLERS[p.ptype](p)
	else:
		return p.response(400)
