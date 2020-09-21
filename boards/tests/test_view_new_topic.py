from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from boards.forms import NewTopicForm

from boards.models import (Board, Topic, Post)

from boards.views import new_topic


class NewTopicTests(TestCase):
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

        self.client.login(username='john', password='123')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'board_pk': 99})

        response = self.client.get(url)

        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve(f'/boards/{self.board.pk}/new/')

        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'board_pk': self.board.pk})

        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})

        response = self.client.get(new_topic_url)

        self.assertContains(response, f'href="{board_topics_url}"')

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})

        response = self.client.get(url)

        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})

        data = {
            'subject': 'Test title',
            'message': 'Test message',
        }

        self.client.post(url, data)

        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """

        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})

        response = self.client.post(url, {})

        form = response.context.get('form')

        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_field(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """

        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})

        data = {
            'subject': '',
            'message': '',
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})

        response = self.client.get(url)

        form = response.context.get('form')

        self.assertIsInstance(form, NewTopicForm)


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            name='Django',
            description='Django board.'
        )

        self.url = reverse('new_topic', kwargs={'board_pk': self.board.pk})

        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')

        self.assertRedirects(self.response, f'{login_url}?next={self.url}')
