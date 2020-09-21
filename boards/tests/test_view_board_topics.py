from django.test import TestCase
from django.urls import reverse, resolve

from boards.views import TopicListView

from boards.models import Board


class BoardTopicsTests(TestCase):
    """
    We have to create a mock of Board, because Django doesn't
    use the current database
    """

    def setUp(self):
        self.board = Board.objects.create(
            name='Django',
            description='Django board',
        )

        url = reverse('board_topics', kwargs={'pk': self.board.pk})

        self.response = self.client.get(url)

    def test_board_topics_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})

        response = self.client.get(url)

        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve(f"/boards/{self.board.pk}/")

        self.assertEquals(view.func.view_class, TopicListView)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'board_pk': self.board.pk})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))