from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, blank=True, null=True)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null= True)
	views = models.BigIntegerField(default=0)

	def publish(self):
		self.published_date = timezone.now()
		self.save()
		
	def approved_comments(self):
		return self.comments.filter(approved_comment=True)
		
	def like_count(self):
		return PostLike.objects.filter(post=self).count()
	
	def deslike_count(self):
		return PostDeslike.objects.filter(post=self).count()
	
	def __str__(self):
		return '{} by {}'.format(self.title,self.author)

class PostLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

	def __str__(self):
		return '{} by {}'.format(self.title,self.author)

class PostDeslike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

	def __str__(self):
		return '{} by {}'.format(self.title,self.author)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

