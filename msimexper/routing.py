import asyncio

from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
from channels.generic.http import AsyncHttpConsumer


class LongPollConsumer(AsyncHttpConsumer):
	async def handle(self, body):
		await asyncio.sleep(10)
		await self.send_response(200, b"Your response bytes", headers=[
			(b"Content-Type", b"text/plain"),
		])


application = ProtocolTypeRouter({
	"http": URLRouter([
		url(r"^v(?P<layer>\d+)/fetch$", LongPollConsumer),
		# url(r"^longpoll/$", LongPollConsumer),
		# url(r"^notifications/(?P<stream>\w+)/$", LongPollConsumer),
		url(r"", AsgiHandler),
	]),
})
