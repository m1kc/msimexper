from django.db import models


class User(models.Model):
	login = models.TextField()
	password_plaintext = models.TextField()

	def __str__(self):
		return self.login


class Session(models.Model):
	extid = models.TextField()
	user = models.ForeignKey(User, on_delete=models.PROTECT)


class Contact(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	handle = models.TextField()
	servername = models.TextField()
	group_path_json = models.TextField()
