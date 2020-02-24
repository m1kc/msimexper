from core.server_core import auth

import asyncio
import logging; log = logging.getLogger(__name__)

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

			sessid = None
			for key, value in self.scope['headers']:
				if key.decode('utf-8') == 'x-session':
					sessid = value.decode('utf-8')
			log.debug(sessid)
			assert sessid != None, "No X-Session header"

			#user = auth(sessid)
			user = await database_sync_to_async(auth)(sessid)
			log.debug(user)
			assert user != None, "Auth failed"

			await asyncio.sleep(10)
			await self.send_response(200, b"Your response bytes", headers=[
				(b"Content-Type", b"text/plain"),
			])
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
