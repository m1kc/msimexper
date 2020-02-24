from core.server_core import auth
from core.fanout import queue_create, queue_pop

import asyncio
import logging; log = logging.getLogger(__name__)
import json

from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
from channels.generic.http import AsyncHttpConsumer
# from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


class LongPollConsumer(AsyncHttpConsumer):
	async def handle(self, body):
		# TODO: return code 400 on auth issues
		try:
			log.debug('started /fetch')
			log.debug(self.scope['headers'])

			# Extract sessid from request headers
			sessid = None
			for key, value in self.scope['headers']:
				# TODO: fuck this shit, make proper headers object that ignores case
				# (probably someone wrote it already)
				if key.decode('utf-8') == 'x-session':
					sessid = value.decode('utf-8')
			log.debug(sessid)
			assert sessid != None, "No X-Session header"

			# Authenticate user
			#user = auth(sessid)
			user = await database_sync_to_async(auth)(sessid)
			log.debug(user)
			assert user != None, "Auth failed"

			# Get message queue for this sessid. If it was just created, return code 201
			just_created = await queue_create(sessid)
			if just_created:
				await self.send_response(201, b'')
				return
			# Return a message from queue, possibly waiting for it to appear
			try:
				p = await queue_pop(sessid)
				# await asyncio.sleep(10)
				# await self.send_response(200, b"Your response bytes", headers=[
				# 	(b"Content-Type", b"text/plain"),
				# ])
				# ignores p.code?
				await self.send_response(200, json.dumps(p.payload, ensure_ascii=False).encode('utf-8'))
			except asyncio.TimeoutError:
				await self.send_response(204, b'')
		except Exception as ex:
			log.error('LongPollConsumer.handle: %s', ex)


application = ProtocolTypeRouter({
	"http": URLRouter([
		url(r"^v(?P<layer>\d+)/fetch$", LongPollConsumer),
		# url(r"^longpoll/$", LongPollConsumer),
		# url(r"^notifications/(?P<stream>\w+)/$", LongPollConsumer),
		url(r"", AsgiHandler),
	]),
})
