from django.db import models


class User(models.Model):
	login = models.TextField()
	password_plaintext = models.TextField()

	def __str__(self):
		return self.login


class Session(models.Model):
	extid = models.TextField()
	user = models.ForeignKey(User, on_delete=models.PROTECT)
