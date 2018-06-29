from django.db import models
from django.forms import ModelForm, Textarea

class Article(models.Model):
	title = models.CharField(max_length = 256, unique=True)
	html = models.TextField()
	#blank=True  attribute sets required to False
	tags = models.CharField(max_length = 256, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "Title : '%s'" % self.title

class ArticleForm(ModelForm):
	class Meta:
		model = Article
		widgets = {
			'html': Textarea(attrs={'cols' : '80', 'rows' : '50'})
		}
		fields = ['title', 'html', 'tags']
