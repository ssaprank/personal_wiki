"""Holds models of the page module"""
from django.db import models
from django.forms import ModelForm, Textarea, TextInput

class Article(models.Model):
	"""Represents an Article"""
	title = models.CharField(max_length=256, unique=True)
	html = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now_add=True)
	work_in_progress = models.BooleanField(blank=True, default=True)

	def __str__(self):
		string = "Title : '%s'\nCreated: %s\n" % (self.title, self.created)
		string += "WIP: " + ("yes" if self.work_in_progress is True else "No")

		return string + "\n\n"

class Image(models.Model):
	title = models.CharField(max_length=100)
	image = models.ImageField(upload_to='images/')
	uploaded_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
	name = models.CharField(max_length=100, unique=True)
	articles = models.ManyToManyField(Article)

class ImageForm(ModelForm):
	class Meta:
		model = Image
		fields = ('image', )

class ArticleForm(ModelForm):
	"""Represents a Form for Article model"""
	class Meta:
		""" Holds Metadata for ArticleForm class """
		model = Article
		widgets = {
			'html': Textarea(attrs={'cols' : '80', 'rows' : '20', 'class' : 'form-control'}),
			'title' : TextInput(attrs={'class' : 'form-control'})
		}
		fields = ['title', 'html', 'work_in_progress']
		labels = {
			'html' : 'Write your Article',
		}
