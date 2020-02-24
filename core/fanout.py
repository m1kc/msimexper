from asyncio import Queue, wait_for


BUFFER_SIZE = 100
POP_TIMEOUT = 15
_queues = {}


async def queue_create(sessid: str) -> bool:
	"""
	Returns True on successful create, False if it already exists.
	"""
	if not sessid in _queues:
		_queues[sessid] = Queue(BUFFER_SIZE)
		await _queues[sessid].put('test payload')
		return True
	else:
		return False


async def queue_pop(sessid: str, timeout=POP_TIMEOUT):
	assert sessid in _queues, "No such queue"
	return await wait_for(_queues[sessid].get(), timeout)
