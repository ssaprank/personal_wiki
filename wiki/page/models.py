from django.db import models
from django.forms import ModelForm

class Article(models.Model):
	title = models.CharField(max_length = 256, unique=True)
	html = models.TextField()
	tags = models.CharField(max_length = 256)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField()

	def __str__(self):
		return "Title : '%s'" % self.title

class ArticleForm(ModelForm):
	class Meta:
		model = Article
		fields = ['title', 'html', 'tags']
