from django.db import models


class User(models.Model):
	login = models.TextField()  # TODO: index
	password_plaintext = models.TextField()

	def __str__(self):
		return self.login

class Session(models.Model):
	extid = models.TextField()  # TODO: index, maybe PK
	user = models.ForeignKey(User, on_delete=models.PROTECT)  # TODO: index


class Contact(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)  # TODO: index
	handle = models.TextField()
	servername = models.TextField()
	caption = models.TextField()
	group_path_json = models.TextField()


class PrivateChat(models.Model):
	author_mid = models.TextField()
	recipient_mid = models.TextField()

class PrivateChatMessage(models.Model):
	chat = models.ForeignKey(PrivateChat, on_delete=models.PROTECT)
	prev_msg = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True)
	cookie = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	author_mid = models.TextField()
	text = models.TextField()

class PrivateChatReference(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	chat_mid = models.TextField()
	chat = models.ForeignKey(PrivateChat, on_delete=models.PROTECT)
	last_read_msg_id = models.ForeignKey(PrivateChatMessage, on_delete=models.PROTECT, blank=True, null=True)
