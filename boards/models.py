import math

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe

from markdown import markdown


class Board(models.Model):
    # choices

    # database fields
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    # manager

    # meta class

    # To string method
    def __str__(self):
        return self.name

    # save method

    # absolute URL method

    # other methods
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(
            topic__board=self
        ).order_by('created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)

    """
    If we don't set a name for it, Django will generate it with the 
    name: (class_name)_set related_name -> Board.topics | User.topics
    """
    board = models.ForeignKey(
        Board,
        related_name='topics',
        on_delete=models.CASCADE
    )
    starter = models.ForeignKey(
        User,
        related_name='topics',
        on_delete=models.CASCADE
    )
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()

        pages = count / 3

        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()

        return count > 6

    def get_page_range(self):
        count = self.get_page_count()

        if self.has_many_pages(count):
            return range(1, 5)

        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:3]


class Post(models.Model):
    message = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    topic = models.ForeignKey(
        Topic,
        related_name='posts',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE
    )

    """
    Prefer not to create a backwards relation
    """
    updated_by = models.ForeignKey(
        User,
        null=True,
        related_name='+',
        on_delete=models.CASCADE
    )

    def __str__(self):
        truncated_message = Truncator(self.message)

        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
