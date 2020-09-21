from django.urls import path

from .views import (
    BoardListView,
    TopicListView,
    new_topic,
    PostListView,
    reply_topic,
    PostUpdateView,
)

urlpatterns = [
    path('', BoardListView.as_view(), name='home'),
    path('boards/<int:pk>/', TopicListView.as_view(), name='board_topics'),
    path('boards/<int:board_pk>/new/', new_topic, name='new_topic'),
    path(
        'boards/<int:board_pk>/topics/<int:topic_pk>/',
        PostListView.as_view(),
        name='topic_posts',
    ),
    path(
        'boards/<int:board_pk>/topics/<int:topic_pk>/reply/',
        reply_topic,
        name='reply_topic',
    ),
    path(
        'boards/<int:board_pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/',
        PostUpdateView.as_view(),
        name='edit_post',
    ),
]
