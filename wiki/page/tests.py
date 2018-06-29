from django.test import TestCase
from django.utils import timezone

from .models import Article
from datetime import timedelta

class ArticleTestCase(TestCase):
	def setUp(self):
		Article.objects.create(title="my_test_title", html="<p>test_page_1</p>", tags="one,two,three")
		Article.objects.create(title="my_test_new", html="<p>following page</p>")

	def test_dateTime_default_values(self):
		articles = Article.objects.all()
		now = timezone.now()
		for article in articles:
			self.assertTrue(now  - timedelta(minutes=1) <= article.created <= now)
			self.assertTrue(now  - timedelta(minutes=1) <= article.last_modified <= now)
