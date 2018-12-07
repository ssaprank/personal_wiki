"""Model testing for page app"""
from django.test import TestCase
from django.utils import timezone

from ..models import Article
from datetime import timedelta

class ArticleTestCase(TestCase):
	"""Testing the article model"""
	def setUp(self):
		"""Set up test environment for ArticleTestCase"""
		Article.objects.create(title="my_test_title", html="<p>test_page_1</p>", tags="one,two,three")
		Article.objects.create(title="my_test_new", html="<p>following page</p>")

	def test_dateTime_default_values(self):
		"""Check that created and last modified fields are set to current time on article creation"""
		articles = Article.objects.all()
		now = timezone.now()
		for article in articles:
			self.assertTrue(now  - timedelta(minutes=1) <= article.created <= now)
			self.assertTrue(now  - timedelta(minutes=1) <= article.last_modified <= now)
