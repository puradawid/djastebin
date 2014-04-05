# ./tests/test_db.py

from django.test import TestCase

#import models
from apps.comment.models import Comment
from apps.paste.models import Paste
from django.contrib.auth.models import User

class DatabaseTestCase(TestCase):
	
	comment_title = "This is title of paste"
	username      = "MyUserName"
	password      = "MyFreakedOutPassword1234"
	content       = "This is testing comment content"
	paste_title   = "This is my paste title, blah blag"
	
	def setUp(self):
		paste = Paste.objects.create(title=self.paste_title)
		user = User.objects.create(username=self.username, password=self.password)
		Comment.objects.create(content=self.content, author=user, paste=paste)
	
	# Testing simple reading objects
	def test_db(self):
		comment = Comment.objects.get(content=self.content)
		self.assertEqual(comment.content, self.content)
		self.assertEqual(comment.paste.title, self.paste_title) 

