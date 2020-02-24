from msim.models import Session, User

from asyncio import Queue, wait_for, QueueFull
import logging; log = logging.getLogger(__name__)

# from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


BUFFER_SIZE = 100
POP_TIMEOUT = 15
_queues = {}


async def queue_create(sessid: str) -> bool:
	"""
	Returns True on successful create, False if it already exists.
	"""
	if not sessid in _queues:
		_queues[sessid] = Queue(BUFFER_SIZE)
		return True
	else:
		return False


async def queue_pop(sessid: str, timeout=POP_TIMEOUT):
	assert sessid in _queues, "No such queue"
	return await wait_for(_queues[sessid].get(), timeout)


async def queue_push(sessid: str, x):
	if not sessid in _queues: return
	try:
		_queues[sessid].put_nowait(x)
	except QueueFull:
		# If queue is full, drop it. No mercy for slow clients.
		_queues[sessid] = None


async def queue_push_to_user(username: str, x):
	log.debug('queue_push_to_user')

	@database_sync_to_async
	def inner():
		log.debug('inner')
		user = User.objects.get(login=username)
		log.debug('got user')
		sessions = list(Session.objects.filter(user=user))
		log.debug('Num of sessions: %d', len(sessions))
		return sessions

	sessions = await inner()
	for session in sessions:
		await queue_push(session.extid, x)
