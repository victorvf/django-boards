from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from boards.models import Board, Post, Topic

from boards.views import PostListView


class TopicPostsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            name='Django',
            description='Django board.',
        )

        self.user = User.objects.create_user(
            username='john',
            email='john@doe.com',
            password='123',
        )

        self.topic = Topic.objects.create(
            subject='Hello, world',
            board=self.board,
            starter=self.user,
        )

        Post.objects.create(
            message='Post created by someone',
            topic=self.topic,
            created_by=self.user,
        )

        self.url = reverse(
            'topic_posts',
            kwargs={'board_pk': self.board.pk, 'topic_pk': self.topic.pk},
        )

        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f'/boards/{self.board.pk}/topics/{self.topic.pk}/')

        self.assertEquals(view.func.view_class, PostListView)
