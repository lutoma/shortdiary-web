from django.test import TestCase, Client
from django.urls import reverse
from diary.models import DiaryUser, Post
import datetime
import json


class RandomPublicPostViewTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = DiaryUser.objects.get_or_create(username='testuser')[0]
		self.client.force_login(self.user)

	def test_no_posts_exist(self):
		res = self.client.get(reverse('apiv2:posts-random'))
		self.assertEqual(res.status_code, 404)
		self.assertEqual(res.content, b'')

	def test_only_private_posts_exist(self):
		Post.objects.create(text='foobar', public=False, author=self.user,
			date=datetime.date.today(), mood=1)

		res = self.client.get(reverse('apiv2:posts-random'))
		self.assertEqual(res.status_code, 404)
		self.assertEqual(res.content, b'')

	def test_one_post_exists(self):
		Post.objects.create(text='foobar', public=True, author=self.user,
			date=datetime.date.today(), mood=1)

		res = self.client.get(reverse('apiv2:posts-random'))
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.content)
		self.assertEqual(data['public_text'], 'foobar')
		self.assertEqual(data['mood'], 1)

	def test_only_public_text(self):
		Post.objects.create(text='foobar', public=True, author=self.user,
			date=datetime.date.today(), mood=1)

		res = self.client.get(reverse('apiv2:posts-random'))
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.content)
		self.assertTrue('text' not in data)
		self.assertTrue('public_text' in data)

	def test_mention_removed(self):
		Post.objects.create(text='foobar @testnick', public=True, author=self.user,
			date=datetime.date.today(), mood=1)

		res = self.client.get(reverse('apiv2:posts-random'))
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.content)
		self.assertTrue('testnick' not in data['public_text'])
