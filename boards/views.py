from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Board, Post, Topic

from .forms import NewTopicForm, PostForm


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/home.html'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))

        queryset = self.board.topics.order_by('last_updated').annotate(
            replies=Count('posts') - 1
        )

        return queryset


@login_required
def new_topic(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()

            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user,
            )

            return redirect('topic_posts', board_pk=board_pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()

    return render(
        request, 'boards/new_topic.html', {'board': board, 'form': form}
    )


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        session_key = f"viewed_topic_{self.topic.pk}"

        if not self.request.session.get(session_key, False):
            self.topic.views += 1

            self.topic.save()

            self.request.session[session_key] = True

        kwargs['topic'] = self.topic

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(
            Topic,
            board__pk=self.kwargs.get('board_pk'),
            pk=self.kwargs.get('topic_pk'),
        )

        queryset = self.topic.posts.order_by('created_at')

        return queryset


@login_required
def reply_topic(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse(
                'topic_posts',
                kwargs={'board_pk': board_pk, 'topic_pk': topic_pk},
            )
            topic_post_url = f"{topic_url}?page={topic.get_page_count()}#{post.pk}"

            return redirect(topic_post_url)
    else:
        form = PostForm()

    return render(
        request, 'boards/reply_topic.html', {'topic': topic, 'form': form}
    )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'boards/edit_post.html'

    """
    Here we get the variable passed by url to use to find the post 
    and pass the name of the model in the template.
    """
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()

        return redirect(
            'topic_posts',
            board_pk=post.topic.board.pk,
            topic_pk=post.topic.pk,
        )
