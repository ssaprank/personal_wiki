from django.db import models

class Article(models.Model):
	title = models.CharField(max_length = 256)
	text = models.TextField()
	tags = models.CharField(max_length = 256)
	